# mybar/views/auth_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import register_user, verify_user, verify_admin, get_all_users, add_admin, update_user_password, get_user_hashed_password # ДОБАВЬТЕ add_admin, update_user_password, get_user_hashed_password
import jwt # Импортируем PyJWT
from django.conf import settings # Для доступа к SECRET_KEY
import datetime # Для установки срока действия токена
from passlib.context import CryptContext # Для проверки старого пароля

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Инициализация для проверки пароля

logger = logging.getLogger(__name__)

# Срок действия токена в часах (например, 24 часа)
JWT_EXPIRATION_HOURS = 24

@csrf_exempt
def register_handler(request):
    """Handle POST /api/auth/register/"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_data = register_user( # Изменено для получения user_data (id и login)
                data["login"],
                data["password"]
            )
            # При успешной регистрации также генерируем токен
            payload = {
                'user_id': user_data['id'],
                'login': user_data['login'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return JsonResponse({"user_id": user_data['id'], "token": token}, status=201)
        except ValueError as e: # Специально для "User already exists"
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=409) # 409 Conflict
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def login_handler(request):
    """Handle POST /api/auth/login/"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = verify_user(data["login"], data["password"])
            if user_id:
                # Генерируем JWT-токен при успешной аутентификации
                payload = {
                    'user_id': user_id,
                    'login': data["login"], # Добавляем логин в токен
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return JsonResponse({"user_id": user_id, "token": token}, status=200)
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt # НОВЫЙ ОБРАБОТЧИК ДЛЯ РЕГИСТРАЦИИ АДМИНА
def register_admin_handler(request):
    """Handle POST /api/auth/register-admin/ (admin only)"""
    if request.method == 'POST':
        try:
            # Проверяем, является ли пользователь администратором
            #if not getattr(request, 'is_admin', False):
                #return JsonResponse({"error": "Admin privileges required"}, status=403)

            data = json.loads(request.body)
            login = data.get("login")
            password = data.get("password")

            if not login or not password:
                return JsonResponse({"error": "Login and password are required"}, status=400)

            admin_id = add_admin(login, password)
            return JsonResponse({"admin_id": admin_id, "message": "Admin registered successfully"}, status=201)
        except ValueError as e: # Для ошибки "Admin with login already exists"
            logger.warning(f"Admin registration error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=409) # 409 Conflict
        except Exception as e:
            logger.error(f"Admin registration error: {str(e)}")
            return JsonResponse({"error": "Failed to register admin"}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def admin_login_handler(request):
    """Handle POST /api/auth/admin-login/"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            admin_id = verify_admin(data["login"], data["password"])
            if admin_id:
                # Генерируем JWT-токен для админа (с пометкой 'is_admin')
                payload = {
                    'user_id': admin_id,
                    'login': data["login"],
                    'is_admin': True, # Добавляем флаг админа
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXPIRATION_HOURS)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return JsonResponse({"admin_id": admin_id, "token": token}, status=200)
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Admin login error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def change_password_handler(request):
    """Handle POST /api/auth/change-password/"""
    if request.method == 'POST':
        try:
            # Middleware должен был установить request.user_id и request.user_login
            user_id = getattr(request, 'user_id', None)
            user_login = getattr(request, 'user_login', None)

            if not user_id or not user_login:
                return JsonResponse({"error": "Authentication required"}, status=401)

            data = json.loads(request.body)
            old_password = data.get("old_password")
            new_password = data.get("new_password")

            if not old_password or not new_password:
                return JsonResponse({"error": "Old password and new password are required"}, status=400)

            # Проверяем старый пароль
            # Получаем хэшированный пароль из базы данных для текущего пользователя
            stored_hashed_password = get_user_hashed_password(user_id)

            if not stored_hashed_password or not pwd_context.verify(old_password, stored_hashed_password):
                return JsonResponse({"error": "Invalid old password"}, status=401)

            # Обновляем пароль
            success = update_user_password(user_id, new_password)

            if success:
                return JsonResponse({"message": "Password changed successfully"}, status=200)
            else:
                return JsonResponse({"error": "Failed to change password"}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Change password error: {str(e)}")
            return JsonResponse({"error": "An internal error occurred"}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


# --- Обновление get_all_users_handler для использования JWT (без декоратора) ---
@csrf_exempt
# @jwt_required # УДАЛИТЕ ЭТОТ ДЕКОРАТОР
def get_all_users_handler(request):
    """Handle GET /api/auth/users/ (admin only)"""
    if request.method == 'GET':
        try:
            # Проверка, является ли пользователь администратором
            # request.is_admin будет установлен middleware
            if not getattr(request, 'is_admin', False): # Используем getattr на случай, если middleware не сработал
                return JsonResponse({"error": "Admin privileges required"}, status=403) # 403 Forbidden

            users = get_all_users()
            return JsonResponse({"users": users}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET all users error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)
