from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import add_user_ingredient, get_user_ingredients, delete_user_ingredient

logger = logging.getLogger(__name__)


@csrf_exempt
def user_ingredients_handler(request, user_id):
    """Handle GET, POST, DELETE /api/user-ingredients/"""
    if request.method == 'GET':
        try:
            ingredients = get_user_ingredients(user_id)
            return JsonResponse({"ingredients": ingredients}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET user ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_ingredient_id = add_user_ingredient(user_id, data["ingredient_id"])
            return JsonResponse({"user_ingredient_id": user_ingredient_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            deleted = delete_user_ingredient(user_id, data["ingredient_id"])
            if not deleted:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"message": "Deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)