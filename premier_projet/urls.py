"""
URL configuration for premier_projet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from gestion_etudiants.views import StudentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Créer un routeur par défaut
router = DefaultRouter()

# Enregistrer le StudentViewSet avec le routeur
router.register(r'students', StudentViewSet, basename='student')

# Inclure les URLs générées par le routeur dans urlpatterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='obtain_tokens'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/', include(router.urls)),
    path('', include(router.urls)),
    path('students/<str:name>/', StudentViewSet.as_view({'get': 'search_by_name'}), name='student-search-by-name'),# Inclure les URLs générées par le routeur
]

