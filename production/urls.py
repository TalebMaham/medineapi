from rest_framework.routers import DefaultRouter
from .views import ProductionViewSet, ProductionDeleteByDateViewSet
from .views import StockViewSet

# Initialisation du routeur
router = DefaultRouter()
router.register(r'productions', ProductionViewSet, basename='productions')
router.register(r'productions-delete-by-date', ProductionDeleteByDateViewSet, basename='productions-delete-by-date')
router.register(r'stock', StockViewSet)


urlpatterns = router.urls