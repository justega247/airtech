from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Flight

User = get_user_model()


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class FLightSerializers(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
