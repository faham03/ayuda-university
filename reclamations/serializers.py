from rest_framework import serializers
from .models import Reclamation

class ReclamationSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Reclamation
        fields = ['id', 'student', 'grade', 'message', 'status', 'created_at', 'updated_at']
        read_only_fields = ['status', 'created_at', 'updated_at']
