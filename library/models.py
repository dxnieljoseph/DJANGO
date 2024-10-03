from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()  # Assurez-vous que ce champ est bien un DateField
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField()
    returned = models.BooleanField(default=False)  # Nouveau champ pour indiquer si le livre a été retourné

    def __str__(self):
        return f'{self.user} borrowed {self.book}'
    
class UserActionLog(models.Model):
    ACTION_CHOICES = [
        ('BORROW', 'Borrowed a book'),
        ('RETURN', 'Returned a book'),
        ('COMMENT', 'Commented on a book'),
        ('RATE', 'Rated a book'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.SET_NULL)  # Certaines actions peuvent être liées à un livre
    comment = models.TextField(null=True, blank=True)  # Pour les actions de commentaire
    rating = models.PositiveIntegerField(null=True, blank=True)  # Pour les actions de notation
    timestamp = models.DateTimeField(default=timezone.now)  # Date et heure de l'action

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.timestamp}"