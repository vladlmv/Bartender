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
            logger.error(f"GET categories error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            category_id = create_category(data["name"])
            return JsonResponse({"category_id": category_id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def category_detail_handler(request, category_id):
    """Handle GET and DELETE /api/categories/<id>/"""
    if request.method == 'GET':
        try:
            category = get_category(category_id)
            if not category:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"category": category}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == 'DELETE':
        try:
            deleted = delete_category(category_id)
            if not deleted:
                return JsonResponse({"error": "Not found"}, status=404)
            return JsonResponse({"message": "Deleted"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)