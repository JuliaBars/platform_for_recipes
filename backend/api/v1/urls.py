from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet


from .views import IngredientViewSet, RecipeViewSet, TagViewSet


router = DefaultRouter()

router.register('ingredients', IngredientViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
