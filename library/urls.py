from django.urls import path
from .views import AllUserActionLogList, BookListCreate, BookDetail, ChangePasswordView, CheckOverdueLoans, LoanReturn, UserActionLogList, UserCreate, UserDetailUpdate, UserListCreate, LoanListCreate, LoanCreate, LoanList
from django.contrib.auth import views as auth_views
from .views import LoanList
from . import views  # Importer vos vues

urlpatterns = [
    path('books/', BookListCreate.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('users/', UserListCreate.as_view(), name='user-list'),
    path('loans/', LoanListCreate.as_view(), name='loan-list'),
    path('loans/', LoanList.as_view(), name='loan-list'),
    path('loans/create/', LoanCreate.as_view(), name='loan-create'),
    path('loans/<int:pk>/return/', LoanReturn.as_view(), name='loan-return'),
    path('users/', UserCreate.as_view(), name='user-create'),
    path('users/<int:pk>/', UserDetailUpdate.as_view(), name='user-detail-update'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('users/', UserListCreate.as_view(), name='user-list-create'),  # Pour lister et créer des utilisateurs
    path('users/<int:pk>/', UserDetailUpdate.as_view(), name='user-detail-update'),  # Pour récupérer, mettre à jour ou supprimer un utilisateur
    path('loans/check-overdue/', CheckOverdueLoans.as_view(), name='check-overdue-loans'),
    # Route pour voir l'historique des actions d'un utilisateur
    path('user/actions/', UserActionLogList.as_view(), name='user-action-log'),
    path('admin/actions/', AllUserActionLogList.as_view(), name='all-user-action-log'),
    path('', views.home, name='home'),  # Route pour la page d'accueil
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Route pour la page de connexion
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Route pour la déconnexion
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('role-redirect/', views.role_based_redirect, name='role_redirect'),
    path('admin/books/add/', views.add_book, name='add_book'),
    path('user/borrow/', views.borrow_books, name='borrow_books'),
    path('user/loans/', views.loan_history, name='loan_history'),
    path('selected_books/', views.selected_books, name='selected_books'),
    path('api/books/', views.book_list, name='book-list'),
    path('api/users/', views.user_list, name='user-list'),
    path('api/loans/', views.LoanList.as_view(), name='loan-list'),
    path('users/', views.user_list, name='user-list'),  # Ajout de l'URL pour la liste des utilisateurs
    path('login/', views.login_view, name='login'),  # Page de connexion
    path('logout/', views.logout_view, name='logout'),  # Page de déconnexion si elle est définie
    path('api/books/', views.book_list, name='book-list'),
    path('api/users/', views.user_list, name='user-list'),
    path('api/loans/', views.LoanList.as_view(), name='loan-list'),
    path('api/loans/', LoanList.as_view(), name='loan-list'),

]
