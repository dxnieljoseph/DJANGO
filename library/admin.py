from django.contrib import admin
from .models import Book  # Assurez-vous d'importer le modèle Book

# Enregistrer le modèle Book dans l'administration
admin.site.register(Book)
