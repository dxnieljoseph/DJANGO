"""
URL configuration for library_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from library import views  # Assurez-vous que le module "library" existe
from library.views import home
from library.views import api_root
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views


schema_view = get_schema_view(
   openapi.Info(
      title="Library Management API",
      default_version='v1',
      description="API pour la gestion d'une bibliothèque",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('api/', api_root, name='api-root'),  # Point d'accès pour /api/
    path('api/books/', include('library.urls')),  # Vos autres points d'accès
    path('api/', include('library.urls')),
    path('', lambda request: HttpResponseRedirect('/api/')),
    path('', home, name='home'),  # Page d'accueil
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('login/', auth_views.LoginView.as_view(), name='login'),  # URL pour la connexion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL pour se déconnecter
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Redirection après déconnexion
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('role-redirect/', views.role_based_redirect, name='role_redirect'),
    path('admin/books/add/', views.add_book, name='add_book'),
    path('user/', include('library.urls')),  # Inclure les URLs de l'application 'library'
    # Routes utilisateur
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('login/', views.login_view, name='login'),  # Route de connexion
    path('logout/', views.logout_view, name='logout'),  # Route de déconnexion
    # Routes pour l'API
    path('api/books/', views.BookList.as_view(), name='book-list'),  # Liste des livres
    path('api/loans/', views.LoanList.as_view(), name='loan-list'),  # Liste des emprunts
    
    # Route d'administration
    path('admin/', admin.site.urls),

    # Routes pour l'API
    path('api/books/', views.BookList.as_view(), name='book-list'),  # Liste des livres
    path('api/loans/', views.LoanList.as_view(), name='loan-list'),  # Liste des emprunts
]
