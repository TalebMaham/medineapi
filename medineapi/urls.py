from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # URLs pour l'administration Django
    path('api/', include('production.urls')),  # Inclure les URLs de l'application production
]
