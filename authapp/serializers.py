from rest_framework import serializers
from users.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type']
