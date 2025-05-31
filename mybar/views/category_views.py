# mybar/views/category_views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from mybar.crud import create_category, get_all_categories, get_category, delete_category

logger = logging.getLogger(__name__)

@csrf_exempt
def categories_handler(request):
    """Handle GET and POST /api/categories/"""
    if request.method == 'GET':
        try:
            categories = get_all_categories()
            return JsonResponse({"categories": categories}, safe=False, status=200)
        except Exception as e:
            logger.error(f"GET all categories error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'POST':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to create categories"}, status=403)
        try:
            data = json.loads(request.body)
            category_id = create_category(data["name"])
            return JsonResponse({"category_id": category_id}, status=201)
        except ValueError as e:
            logger.error(f"Create category error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
        except Exception as e:
            logger.error(f"Create category error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def category_detail_handler(request, category_id: int):
    """Handle GET and DELETE /api/categories/<int:category_id>/"""
    if request.method == 'GET':
        try:
            category = get_category(category_id)
            if category:
                return JsonResponse(category, safe=False, status=200)
            return JsonResponse({"error": "Category not found"}, status=404)
        except Exception as e:
            logger.error(f"GET category detail error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    elif request.method == 'DELETE':
        # Middleware уже проверил, что пользователь аутентифицирован и является админом
        if not getattr(request, 'is_admin', False):
            return JsonResponse({"error": "Admin privileges required to delete categories"}, status=403)
        try:
            if delete_category(category_id):
                return JsonResponse({"message": "Category deleted successfully"}, status=204)
            return JsonResponse({"error": "Category not found"}, status=404)
        except Exception as e:
            logger.error(f"Delete category error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)
