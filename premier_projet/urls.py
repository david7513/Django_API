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
from django.urls import path
from rest_framework.routers import DefaultRouter
from gestion_etudiants.views import StudentViewSet

# Créer un routeur
router = DefaultRouter()

# Enregistrer StudentViewSet avec le routeur, en spécifiant le préfixe et le basename
router.register(r'students', StudentViewSet, basename='student')

# Définir les URLs personnalisées en utilisant le routeur
urlpatterns = [
    # Liste tous les étudiants (GET) et crée un nouvel étudiant (POST)
    path('students/', StudentViewSet.as_view({'get': 'list', 'post': 'create'}), name='student-list'),
    # Récupère, met à jour ou supprime un étudiant spécifique par ID (GET, PUT, DELETE)
    path('students/<int:pk>/', StudentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='student-detail'),
]

# Ajouter les URLs générées par le routeur au urlpatterns
urlpatterns += router.urls

