from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import register_user, verify_user, verify_admin, get_all_users

logger = logging.getLogger(__name__)

@csrf_exempt
def register_handler(request):
    """Handle POST /api/auth/register/"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = register_user(
                data["login"],
                data["password"]
            )
            return JsonResponse({"user_id": user_id}, status=201)
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
                return JsonResponse({"user_id": user_id}, status=200)
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def admin_login_handler(request):
    """Handle POST /api/auth/admin-login/"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            admin_id = verify_admin(data["login"], data["password"])
            if admin_id:
                return JsonResponse({"admin_id": admin_id}, status=200)
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Admin login error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def get_all_users_handler(request):
    """Handle GET /api/auth/users/ (admin only)"""
    if request.method == 'GET':
        try:
            # В реальном приложении здесь должна быть проверка JWT-токена и прав администратора
            users = get_all_users()
            return JsonResponse({"users": users}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET all users error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)