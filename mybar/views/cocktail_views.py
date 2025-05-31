# mybar/views/cocktail_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import (
    create_cocktail, get_all_cocktails, get_cocktail, delete_cocktail,
    get_cocktails_by_user_ingredients, get_cocktails_missing_ingredients,
    get_cocktails_by_ingredient
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
            logger.error(f"GET all cocktails error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'POST':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to create cocktails"}, status=403)
        try:
            data = json.loads(request.body)
            cocktail_id = create_cocktail(data["name"], data["category_id"], data["instructions"])
            return JsonResponse({"cocktail_id": cocktail_id}, status=201)
        except ValueError as e:
            logger.error(f"Create cocktail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Create cocktail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def cocktail_detail_handler(request, cocktail_id: int):
    """Handle GET and DELETE /api/cocktails/<int:cocktail_id>/"""
    if request.method == 'GET':
        try:
            cocktail = get_cocktail(cocktail_id)
            if cocktail:
                return JsonResponse(cocktail, safe=False, status=200)
            return JsonResponse({"error": "Cocktail not found"}, status=404)
        except Exception as e:
            logger.error(f"GET cocktail detail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'DELETE':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to delete cocktails"}, status=403)
        try:
            if delete_cocktail(cocktail_id):
                return JsonResponse({"message": "Cocktail deleted successfully"}, status=204)
            return JsonResponse({"error": "Cocktail not found"}, status=404)
        except Exception as e:
            logger.error(f"Delete cocktail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def cocktails_by_ingredients_handler(request, user_id: int):
    """Handle GET /api/cocktails/by-ingredients/<int:user_id>/"""
    if request.method == 'GET':
        # Проверяем, что user_id в URL соответствует user_id из токена
        # Или что пользователь является админом
        if not (getattr(request, 'user_id', None) == user_id or getattr(request, 'is_admin', False)):
            return JsonResponse({"error": "Access denied for this user's ingredients"}, status=403)
        try:
            cocktails = get_cocktails_by_user_ingredients(user_id)
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails by user ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def cocktails_missing_ingredients_handler(request, user_id: int):
    """Handle GET /api/cocktails/missing-ingredients/<int:user_id>/"""
    if request.method == 'GET':
        # Проверяем, что user_id в URL соответствует user_id из токена
        # Или что пользователь является админом
        if not (getattr(request, 'user_id', None) == user_id or getattr(request, 'is_admin', False)):
            return JsonResponse({"error": "Access denied for this user's missing ingredients"}, status=403)
        try:
            cocktails = get_cocktails_missing_ingredients(user_id)
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails missing ingredients error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def cocktails_by_single_ingredient_handler(request, ingredient_id: int):
    """Handle GET /api/cocktails/by-ingredient/<int:ingredient_id>/"""
    if request.method == 'GET':
        try:
            cocktails = get_cocktails_by_ingredient(ingredient_id)
            return JsonResponse({"cocktails": cocktails}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET cocktails by single ingredient error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)
