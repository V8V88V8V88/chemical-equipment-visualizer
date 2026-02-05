from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for individual equipment records."""
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetListSerializer(serializers.ModelSerializer):
    """Serializer for dataset list view."""
    equipment_count = serializers.IntegerField(source='equipment.count', read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'equipment_count']


class DatasetDetailSerializer(serializers.ModelSerializer):
    """Serializer for dataset detail view with equipment list."""
    equipment = EquipmentSerializer(many=True, read_only=True)

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'uploaded_at', 'file', 'equipment']


class SummarySerializer(serializers.Serializer):
    """Serializer for dataset summary statistics."""
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    type_distribution = serializers.DictField(child=serializers.IntegerField())


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
