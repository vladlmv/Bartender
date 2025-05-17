from django.urls import path
from mybar.views import auth_views, ingredient_views, category_views, cocktail_views, cocktail_ingredient_views, \
    user_ingredient_views

urlpatterns = [
    # Auth routes
    path('api/auth/register/', auth_views.register_handler),
    path('api/auth/login/', auth_views.login_handler),
    path('api/auth/admin-login/', auth_views.admin_login_handler),

    # Ingredient routes
    path('api/ingredients/', ingredient_views.ingredients_handler),  # GET and POST
    path('api/ingredients/<int:ingredient_id>/', ingredient_views.ingredient_detail_handler),  # DELETE

    # User Ingredient routes
    path('api/user-ingredients/<int:user_id>/', user_ingredient_views.user_ingredients_handler),  # GET, POST, DELETE

    # Category routes
    path('api/categories/', category_views.categories_handler),  # GET and POST
    path('api/categories/<int:category_id>/', category_views.category_detail_handler),  # GET and DELETE

    # Cocktail routes
    path('api/cocktails/', cocktail_views.cocktails_handler),  # GET and POST
    path('api/cocktails/<int:cocktail_id>/', cocktail_views.cocktail_detail_handler),  # GET and DELETE
    path('api/cocktails/by-ingredients/<int:user_id>/', cocktail_views.cocktails_by_ingredients_handler),
    path('api/cocktails/missing-ingredients/<int:user_id>/', cocktail_views.cocktails_missing_ingredients_handler),

    # Cocktail Ingredient routes
    path('api/cocktails-ingredients/<int:cocktail_id>/', cocktail_ingredient_views.cocktail_ingredients_handler),
    # GET and POST
    path('api/cocktails-ingredients/<int:cocktail_id>/<int:ingredient_id>/',
         cocktail_ingredient_views.cocktail_ingredient_detail_handler),  # DELETE
]