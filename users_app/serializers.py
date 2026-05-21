from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration including password confirmation."""

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        """Ensure password and confirmed_password match."""
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        """Create a new user after removing the confirmation field."""
        validated_data.pop('confirmed_password')
        user = User.objects.create_user(**validated_data)
        return user
