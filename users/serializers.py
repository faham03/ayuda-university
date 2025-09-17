from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        # On inclut "role" uniquement en lecture
        fields = ['id', 'username', 'email', 'password', 'role']
        read_only_fields = ['id', 'role']  # le client ne peut PAS choisir le rôle

    def create(self, validated_data):
        # Crée l'utilisateur
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # Forcer le rôle "student"
        user.role = "student"
        user.save()
        return user
