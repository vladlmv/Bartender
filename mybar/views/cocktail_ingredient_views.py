from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import (
    add_cocktail_ingredient,
    get_cocktail_ingredients,
    delete_cocktail_ingredient
)

logger = logging.getLogger(__name__)


@csrf_exempt
def cocktail_ingredients_handler(request, cocktail_id):
    """Handle GET and POST /api/cocktails-ingredients/<cocktail_id>/"""
    if request.method == 'GET':
        try:
            ingredients = get_cocktail_ingredients(cocktail_id)
            return JsonResponse({"ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktail ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            ci_id = add_cocktail_ingredient(cocktail_id, data["ingredient_id"])
            return JsonResponse({"cocktail_ingredient_id": ci_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def cocktail_ingredient_detail_handler(request, cocktail_id, ingredient_id):
    """Handle DELETE /api/cocktails-ingredients/<cocktail_id>/<ingredient_id>/"""
    if request.method == 'DELETE':
        try:
            delete_cocktail_ingredient(cocktail_id, ingredient_id)
            return JsonResponse({"message": "Deleted"})
        except Exception as e:
            # Если это исключение "не найдено"
            if 'not found' in str(e).lower():
                return JsonResponse({"error": "Not found"}, status=404)
            logger.error(f"DELETE error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)