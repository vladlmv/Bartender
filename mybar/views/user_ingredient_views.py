# mybar/views/user_ingredient_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import add_user_ingredient, get_user_ingredients, delete_user_ingredient

logger = logging.getLogger(__name__)


@csrf_exempt
def user_ingredients_handler(request, user_id: int):
    """Handle GET, POST, DELETE /api/user-ingredients/<int:user_id>/"""
    # Проверяем, что user_id в URL соответствует user_id из токена
    # Или что пользователь является админом
    if not (getattr(request, 'user_id', None) == user_id or getattr(request, 'is_admin', False)):
        return JsonResponse({"error": "Access denied for this user's ingredients"}, status=403)

    if request.method == 'GET':
        try:
            ingredients = get_user_ingredients(user_id)
            return JsonResponse({"user_ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET user ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredient_id = data.get("ingredient_id")
            if not ingredient_id:
                return JsonResponse({"error": "ingredient_id is required"}, status=400)

            user_ingredient_id = add_user_ingredient(user_id, ingredient_id)
            return JsonResponse({"user_ingredient_id": user_ingredient_id}, status=201)
        except ValueError as e:
            logger.error(f"Add user ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Add user ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            ingredient_id = data.get("ingredient_id")
            if not ingredient_id:
                return JsonResponse({"error": "ingredient_id is required"}, status=400)

            if delete_user_ingredient(user_id, ingredient_id):
                return JsonResponse({"message": "User ingredient deleted successfully"}, status=204)
            return JsonResponse({"error": "User ingredient not found or already deleted"}, status=404)
        except Exception as e:
            logger.error(f"Delete user ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
