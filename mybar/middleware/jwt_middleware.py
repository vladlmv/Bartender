import jwt
from django.conf import settings
from django.http import JsonResponse
import logging
import re

logger = logging.getLogger(__name__)

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = [
            re.compile(r'^/api/auth/register/$'),
            re.compile(r'^/api/auth/login/$'),
            re.compile(r'^/api/auth/admins/$'),
            re.compile(r'^/api/auth/admin-login/$'),
            re.compile(r'^/api/auth/register-admin/$'), # <--- УБЕДИТЕСЬ, ЧТО ЭТА СТРОКА ЗДЕСЬ
            re.compile(r'^/api/ingredients/$'), # GET - публичный
            re.compile(r'^/api/ingredients/\d+/$'), # GET - публичный
            re.compile(r'^/api/categories/$'), # GET - публичный
            re.compile(r'^/api/categories/\d+/$'), # GET - публичный
            re.compile(r'^/api/cocktails/$'), # GET - публичный
            re.compile(r'^/api/cocktails/\d+/$'), # GET - публичный
            re.compile(r'^/api/cocktails/by-ingredient/\d+/$'), # GET - публичный
            re.compile(r'^/api/cocktails-ingredients/\d+/$'), # GET - публичный
        ]
        # Список путей, которые требуют прав администратора
        self.admin_required_paths = [
            re.compile(r'^/api/auth/users/$'),
            #re.compile(r'^/api/auth/admins/$'),
            # re.compile(r'^/api/auth/register-admin/$'), # <--- УБЕДИТЕСЬ, ЧТО ЭТОЙ СТРОКИ ЗДЕСЬ НЕТ (она закомментирована или удалена)
            re.compile(r'^/api/ingredients/$'), # POST для создания ингредиента
            re.compile(r'^/api/ingredients/\d+/$'), # DELETE для ингредиента
            re.compile(r'^/api/categories/$'), # POST для создания категории
            re.compile(r'^/api/categories/\d+/$'), # DELETE для категории
            re.compile(r'^/api/cocktails/$'), # POST для создания коктейля
            re.compile(r'^/api/cocktails/\d+/$'), # DELETE для коктейля
            re.compile(r'^/api/cocktails-ingredients/\d+/$'), # POST для добавления ингредиента к коктейлю
            re.compile(r'^/api/cocktails-ingredients/\d+/\d+/$'), # DELETE для ингредиента из коктейля
        ]
        # Список путей, которые требуют любого токена (пользователь или админ)
        self.auth_required_paths = [
            re.compile(r'^/api/user-ingredients/\d+/$'), # GET, POST, DELETE
            re.compile(r'^/api/cocktails/by-ingredients/\d+/$'),
            re.compile(r'^/api/cocktails/missing-ingredients/\d+/$'),
            re.compile(r'^/api/auth/change-password/$'), # ДОБАВЛЕН НОВЫЙ ЭНДПОИНТ
        ]

    def __call__(self, request):
        # Проверяем, является ли путь исключенным из проверки токена
        path = request.path_info
        for pattern in self.exempt_paths:
            if pattern.match(path):
                return self.get_response(request)

        # Проверяем наличие заголовка авторизации
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({"error": "Authorization header missing"}, status=401)

        try:
            token_type, token = auth_header.split(' ')
            if token_type.lower() != 'bearer':
                return JsonResponse({"error": "Invalid token type, must be Bearer"}, status=401)

            # Декодируем токен
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            # Прикрепляем данные пользователя к объекту запроса
            request.user_id = payload.get('user_id')
            request.user_login = payload.get('login')
            request.is_admin = payload.get('is_admin', False)

            # Проверяем, требует ли путь прав администратора
            for pattern in self.admin_required_paths:
                if pattern.match(path):
                    # Для POST и DELETE методов, требующих админ-прав
                    if request.method in ['POST', 'DELETE']:
                        if not request.is_admin:
                            return JsonResponse({"error": "Admin privileges required for this action"}, status=403)
                    # Для GET методов, требующих админ-прав (если таковые будут)
                    # Например, /api/auth/users/ всегда требует админ-прав
                    elif request.method == 'GET' and path == '/api/auth/users/':
                        if not request.is_admin:
                            return JsonResponse({"error": "Admin privileges required"}, status=403)

            # Проверяем, требует ли путь любого токена (пользователь или админ)
            for pattern in self.auth_required_paths:
                if pattern.match(path):
                    if not request.user_id: # Если user_id не установлен, значит токен невалиден или отсутствует
                        return JsonResponse({"error": "Authentication required"}, status=401)
                    break # Токен валиден для этого пути, продолжаем обработку

        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Token has expired"}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "Invalid token"}, status=401)
        except Exception as e:
            logger.error(f"JWT verification error: {str(e)}")
            return JsonResponse({"error": "Unauthorized"}, status=401)

        response = self.get_response(request)
        return response
