from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import create_ingredient, get_all_ingredients, delete_ingredient

logger = logging.getLogger(__name__)


@csrf_exempt
def ingredients_handler(request):
    """Handle GET and POST /api/ingredients/"""
    if request.method == 'GET':
        try:
            ingredients = get_all_ingredients()
            return JsonResponse({"ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredient_id = create_ingredient(data["name"])
            return JsonResponse({"ingredient_id": ingredient_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def ingredient_detail_handler(request, ingredient_id):
    """Handle DELETE /api/ingredients/<id>/"""
    if request.method == 'DELETE':
        try:
            deleted = delete_ingredient(ingredient_id)
            if not deleted:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"message": "Deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)