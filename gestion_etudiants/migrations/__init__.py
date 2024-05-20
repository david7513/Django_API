from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from gestion_etudiants.models import Student

UserModel = get_user_model()

ADMIN_ID = 'admin-oc'
ADMIN_PASSWORD = 'password-oc'
