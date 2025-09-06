from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'student', 'request_type', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'student', 'status', 'created_at']


class AdminRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'student', 'request_type', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'student', 'created_at']
