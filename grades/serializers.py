from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Grade
        fields = ['id', 'student', 'student_name', 'filiere', 'year', 'subject', 'score', 'created_at']
