from msilib.schema import ListView
from time import timezone
from rest_framework import generics, permissions
from .models import Book, Loan, UserActionLog
from .serializers import BookSerializer, ChangePasswordSerializer, LoanSerializer, UserActionLogSerializer
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import Serializer, CharField
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone
from library.models import Book, Loan
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view

def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirige les utilisateurs normaux

    users = User.objects.all()  # Liste des utilisateurs
    books = Book.objects.all()  # Liste des livres

    return render(request, 'admin_dashboard.html', {
        'users': users,
        'books': books
    })
    
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all().values('id', 'title', 'author', 'genre', 'available')
    return Response(list(books))

@login_required
def user_dashboard(request):
    # Renvoyer uniquement les options de déconnexion et liste des livres
    return render(request, 'user_dashboard.html')
    
def role_based_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')

def home(request):
    # Si l'utilisateur est connecté, on lui affiche un message de bienvenue.
    if request.user.is_authenticated:
        return render(request, 'home.html', {'message': f'Bienvenue, {request.user.username} !'})
    else:
        # Si l'utilisateur n'est pas connecté, on lui propose de se connecter.
        return render(request, 'home.html', {'message': 'Veuillez vous connecter.'})

def api_root(request):
    return JsonResponse({
        "message": "Bienvenue à l'API de gestion de bibliothèque",
        "endpoints": {
            "books": "/api/books/",
            "users": "/api/users/",
            "loans": "/api/loans/"
        }
    })

def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        isbn = request.POST.get('isbn')
        publication_date = request.POST.get('publication_date')
        Book.objects.create(title=title, author=author, genre=genre, isbn=isbn, publication_date=publication_date)
        return redirect('admin_dashboard')
    return render(request, 'add_book.html')

@login_required
def book_list(request):
    books = Book.objects.all()  # Obtenez tous les livres

    if request.method == 'POST':
        # Traitement des livres sélectionnés pour l'emprunt
        selected_books_ids = request.POST.getlist('selected_books')
        selected_books = Book.objects.filter(id__in=selected_books_ids, available=True)

        for book in selected_books:
            Loan.objects.create(
                user=request.user,
                book=book,
                loan_date=timezone.now(),
                due_date=timezone.now() + timezone.timedelta(days=14)
            )
            book.available = False
            book.save()

        return redirect('user_dashboard')

    return render(request, 'book_list.html', {'books': books})

@login_required
def borrow_books(request):
    if request.method == 'POST':
        selected_books_ids = request.POST.getlist('selected_books')
        selected_books = Book.objects.filter(id__in=selected_books_ids, available=True)

        if selected_books.exists():
            for book in selected_books:
                Loan.objects.create(
                    user=request.user,
                    book=book,
                    loan_date=timezone.now(),
                    due_date=timezone.now() + timezone.timedelta(days=14)
                )
                book.available = False
                book.save()

            messages.success(request, 'Vous avez emprunté les livres sélectionnés.')
        else:
            messages.error(request, 'Aucun livre sélectionné ou les livres ne sont plus disponibles.')

        return redirect('user_dashboard')
    
    return redirect('book-list')

def loan_history(request):
    # Récupère les emprunts de l'utilisateur connecté
    loans = Loan.objects.filter(user=request.user).order_by('-borrow_date')
    return render(request, 'loan_history.html', {'loans': loans})

def return_book(request, loan_id):
    loan = Loan.objects.get(id=loan_id, user=request.user)
    if not loan.returned:
        loan.returned = True
        loan.return_date = timezone.now()
        loan.book.available = True
        loan.book.save()
        loan.save()
    return redirect('user_dashboard')

def selected_books(request):
    if request.method == 'POST':
        # Récupérer les IDs des livres sélectionnés
        selected_book_ids = request.POST.getlist('selected_books')
        
        # Récupérer les livres correspondant aux IDs sélectionnés
        books = Book.objects.filter(id__in=selected_book_ids)
        
        # Afficher la page des livres sélectionnés
        return render(request, 'selected_books.html', {'books': books})
    
    return redirect('book-list')  # Si l'utilisateur accède sans POST, il est redirigé

@require_POST
def logout_view(request):
    # Déconnecter l'utilisateur
    logout(request)
    # Rediriger vers la page d'accueil de l'API
    return redirect('/login/')

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/user/dashboard/')  # Rediriger vers le tableau de bord après connexion
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_list(request):
    # Récupérer tous les utilisateurs
    users = User.objects.all()
    # Créer une liste avec les informations des utilisateurs
    user_data = [{"username": user.username, "email": user.email} for user in users]
    # Retourner la réponse en format JSON
    return JsonResponse(user_data, safe=False)

def book_list(request):
    books = Book.objects.all()
    books_data = [{'title': book.title, 'author': book.author, 'genre': book.genre} for book in books]
    return JsonResponse({'books': books_data})


class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # Seuls les utilisateurs authentifiés peuvent accéder à cette vue

    # Ajouter les filtres
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['genre']  # Filtrage par genre exact
    search_fields = ['title', 'author']  # Recherche par titre ou auteur

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@method_decorator(login_required, name='dispatch')
class LoanListCreate(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retourne uniquement les emprunts de l'utilisateur connecté
        return Loan.objects.filter(user=self.request.user)
    
# Création d'un nouvel emprunt
class LoanCreate(generics.CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Attache l'utilisateur connecté à l'emprunt
        serializer.save(user=self.request.user)
        
class LoanList(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    
# Vue pour la liste des emprunts
class LoanList(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        return Response({"loans": [loan.book.title for loan in loans]})
    
class LoanReturn(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        loan = serializer.save()
        # Rendre le livre disponible une fois retourné
        if loan.return_date:
            loan.book.available = True
            loan.returned = True  # Marquer comme retourné
            loan.book.save()

# Création d'un utilisateur
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Détail et mise à jour d'un utilisateur
class UserDetailUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # L'utilisateur doit être authentifié pour accéder à ces actions

class ChangePasswordSerializer(Serializer):
    old_password = CharField(required=True)
    new_password = CharField(required=True)

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Vérifier l'ancien mot de passe
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["L'ancien mot de passe est incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

            # Changer le mot de passe
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"detail": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Seuls les administrateurs peuvent supprimer un utilisateur

# Vue pour lister et créer des utilisateurs
class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Seuls les administrateurs peuvent voir et créer des utilisateurs

# Vue pour récupérer, mettre à jour ou supprimer un utilisateur
class UserDetailUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Seuls les administrateurs peuvent modifier ou supprimer

class CheckOverdueLoans(APIView):
    def get(self, request, *args, **kwargs):
        overdue_loans = Loan.objects.filter(due_date__lt=timezone.now(), returned=False)
        for loan in overdue_loans:
            # Marquer les livres en retard
            loan.book.available = False
            loan.save()
        return Response({"message": "Vérification des livres en retard effectuée."})

class LoanCreate(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        loan = serializer.save(user=self.request.user)
        # Enregistrer l'action d'emprunt dans le journal des actions
        UserActionLog.objects.create(
            user=self.request.user,
            action='BORROW',
            book=loan.book
        )

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
class LoanReturn(generics.UpdateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        loan = serializer.save()
        # Enregistrer le retour du livre dans le journal des actions
        UserActionLog.objects.create(
            user=self.request.user,
            action='RETURN',
            book=loan.book
        )
        
class UserActionLogList(generics.ListAPIView):
    serializer_class = UserActionLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retourner uniquement les actions de l'utilisateur connecté
        return UserActionLog.objects.filter(user=self.request.user).order_by('-timestamp')

class AllUserActionLogList(generics.ListAPIView):
    queryset = UserActionLog.objects.all().order_by('-timestamp')
    serializer_class = UserActionLogSerializer
    permission_classes = [IsAdminUser]
    
class BookListView(ListView):
    model = Book  # Le modèle que cette vue va lister
    template_name = 'books/book_list.html'  # Le fichier HTML à rendre
    context_object_name = 'books'  # Le nom du contexte dans le template pour accéder aux objets

@method_decorator(cache_page(60*15), name='dispatch')
class BookListCreate(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
# Vue pour la liste des livres
class BookList(APIView):
    def get(self, request):
        books = Book.objects.all()
        return Response({"books": [book.title for book in books]})