from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
# from users.views import CustomUserViewSet


router = DefaultRouter()

# router.register('ingredients', IngredientViewSet)
# router.register('tags', TagViewSet)
# router.register('recipes', RecipeViewSet)
# router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
