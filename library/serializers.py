from datetime import timezone
from rest_framework import serializers
from .models import Book, Loan, UserActionLog
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        
    def validate_isbn(self, value):
        """Validation de l'ISBN (doit être de 13 caractères)."""
        if len(value) != 13:
            raise serializers.ValidationError("L'ISBN doit contenir exactement 13 caractères.")
        return value
    
    def validate_published_date(self, value):
        """S'assure que la date de publication n'est pas dans le futur."""
        if value > timezone.now().date():
            raise serializers.ValidationError("La date de publication ne peut pas être dans le futur.")
        return value

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'
        
    def validate(self, data):
        """S'assure que la date de retour est après la date d'emprunt."""
        if data['return_date'] and data['return_date'] < data['loan_date']:
            raise serializers.ValidationError("La date de retour ne peut pas être avant la date d'emprunt.")
        return data
        # S'assurer que le livre est disponible
        if not data['book'].available:
            raise serializers.ValidationError("Ce livre n'est pas disponible.")
        # S'assurer que la date de retour est après la date d'emprunt
        if data['return_date'] and data['return_date'] < data['loan_date']:
            raise serializers.ValidationError("La date de retour ne peut pas être avant la date d'emprunt.")
        return data
    
    def create(self, validated_data):
        # Rendre le livre indisponible une fois emprunté
        book = validated_data['book']
        book.available = False
        book.save()
        return super().create(validated_data)

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password], help_text="Saisissez un mot de passe fort.")  # Le mot de passe est optionnel pour les mises à jour
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(), message="Cet email est déjà utilisé.")])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']  # Exposition des champs nécessaires
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):
        """Créer un nouvel utilisateur avec un mot de passe haché."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

    def update(self, instance, validated_data):
        """Mettre à jour les informations de l'utilisateur. Le mot de passe est géré séparément."""
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        # Si un nouveau mot de passe est fourni, on le hache et l'attribue à l'utilisateur
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)

        instance.save()
        return instance

    def validate_email(self, value):
        """Validation pour vérifier que l'email est unique."""
        if self.instance:  # Si on met à jour l'utilisateur
            if User.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Cet email est déjà utilisé.")
        else:  # Lors de la création d'un utilisateur
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

class UserActionLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActionLog
        fields = ['user', 'action', 'book', 'comment', 'rating', 'timestamp']
        read_only_fields = ['user', 'timestamp']  # Ces champs seront définis automatiquement