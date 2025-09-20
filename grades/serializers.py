from rest_framework import serializers
from .models import Grade
from django.contrib.auth import get_user_model

User = get_user_model()

class GradeSerializer(serializers.ModelSerializer):
    student_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = [
            'id',
            'student',
            'student_full_name',
            'filiere',
            'year',
            'subject',
            'score',
            'created_at',
        ]

    def get_student_full_name(self, obj):
        """Retourne 'Nom Prénom (username)'"""
        if isinstance(obj.student, User):
            return f"{obj.student.last_name} {obj.student.first_name} ({obj.student.username})"
        return str(obj.student)
