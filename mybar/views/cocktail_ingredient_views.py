# mybar/views/cocktail_ingredient_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import add_cocktail_ingredient, get_cocktail_ingredients, delete_cocktail_ingredient

logger = logging.getLogger(__name__)

@csrf_exempt
def cocktail_ingredients_handler(request, cocktail_id: int):
    """Handle GET and POST /api/cocktails-ingredients/<int:cocktail_id>/"""
    if request.method == 'GET':
        try:
            ingredients = get_cocktail_ingredients(cocktail_id)
            return JsonResponse({"cocktail_ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktail ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'POST':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to add ingredients to cocktails"}, status=403)
        try:
            data = json.loads(request.body)
            ingredient_id = data.get("ingredient_id")
            if not ingredient_id:
                return JsonResponse({"error": "ingredient_id is required"}, status=400)

            ci_id = add_cocktail_ingredient(cocktail_id, ingredient_id)
            return JsonResponse({"cocktail_ingredient_id": ci_id}, status=201)
        except ValueError as e:
            logger.error(f"Add cocktail ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Add cocktail ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def cocktail_ingredient_detail_handler(request, cocktail_id: int, ingredient_id: int):
    """Handle DELETE /api/cocktails-ingredients/<int:cocktail_id>/<int:ingredient_id>/"""
    if request.method == 'DELETE':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to delete ingredients from cocktails"}, status=403)
        try:
            if delete_cocktail_ingredient(cocktail_id, ingredient_id):
                return JsonResponse({"message": "Cocktail ingredient deleted successfully"}, status=204)
            return JsonResponse({"error": "Cocktail ingredient not found or already deleted"}, status=404)
        except Exception as e:
            logger.error(f"Delete cocktail ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
