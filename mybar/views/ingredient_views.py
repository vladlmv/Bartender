# mybar/views/ingredient_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import create_ingredient, get_all_ingredients, delete_ingredient, get_ingredient_by_id

logger = logging.getLogger(__name__)

@csrf_exempt
def ingredients_handler(request):
    """Handle GET and POST /api/ingredients/"""
    if request.method == 'GET':
        try:
            ingredients = get_all_ingredients()
            return JsonResponse({"ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET all ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'POST':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        # (если путь /api/ingredients/ POST требует админ-прав, как указано в middleware)
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to create ingredients"}, status=403)
        try:
            data = json.loads(request.body)
            ingredient_id = create_ingredient(data["name"])
            return JsonResponse({"ingredient_id": ingredient_id}, status=201)
        except ValueError as e:
            logger.error(f"Create ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Create ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def ingredient_detail_handler(request, ingredient_id: int):
    """Handle GET and DELETE /api/ingredients/<int:ingredient_id>/"""
    if request.method == 'GET':
        try:
            ingredient = get_ingredient_by_id(ingredient_id)
            if ingredient:
                return JsonResponse(ingredient, safe=False, status=200)
            return JsonResponse({"error": "Ingredient not found"}, status=404)
        except Exception as e:
            logger.error(f"GET ingredient detail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'DELETE':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to delete ingredients"}, status=403)
        try:
            if delete_ingredient(ingredient_id):
                return JsonResponse({"message": "Ingredient deleted successfully"}, status=204)
            return JsonResponse({"error": "Ingredient not found"}, status=404)
        except Exception as e:
            logger.error(f"Delete ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
