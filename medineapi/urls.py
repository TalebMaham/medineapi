from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # URLs pour l'administration Django
    path('api/', include('production.urls')),  # Inclure les URLs de l'application production
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Obtenir un token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rafraîchir le token
]
