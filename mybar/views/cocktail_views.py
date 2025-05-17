from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import (
    create_cocktail, get_all_cocktails, get_cocktail, delete_cocktail,
    get_cocktails_by_user_ingredients, get_cocktails_missing_ingredients
)

logger = logging.getLogger(__name__)


@csrf_exempt
def cocktails_handler(request):
    """Handle GET and POST /api/cocktails/"""
    if request.method == 'GET':
        try:
            cocktails = get_all_cocktails()
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            cocktail_id = create_cocktail(
                data["name"],
                data["category_id"],
                data.get("instructions", "")
            )
            return JsonResponse({"cocktail_id": cocktail_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def cocktail_detail_handler(request, cocktail_id):
    """Handle GET and DELETE /api/cocktails/<id>/"""
    if request.method == 'GET':
        try:
            cocktail = get_cocktail(cocktail_id)
            if not cocktail:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"cocktail": cocktail}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            deleted = delete_cocktail(cocktail_id)
            if not deleted:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"message": "Deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def cocktails_by_ingredients_handler(request, user_id):
    """Handle GET /api/cocktails/by-ingredients/"""
    if request.method == 'GET':
        try:
            cocktails = get_cocktails_by_user_ingredients(user_id)
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails by ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def cocktails_missing_ingredients_handler(request, user_id):
    """Handle GET /api/cocktails/missing-ingredients/"""
    if request.method == 'GET':
        try:
            cocktails = get_cocktails_missing_ingredients(user_id)
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails missing ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)