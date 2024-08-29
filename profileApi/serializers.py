from rest_framework import serializers
from . import models


class HelloSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=20)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['id', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = models.UserProfile(email=validated_data['email'], first_name=validated_data['first_name'],
                                  last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ProfileFeedItemSerializers(serializers.ModelSerializer):
    """A serializers for profile feed items """

    class Meta:
        model = models.ProfileFeedItem
        fields = ['id', 'user_profile', 'status_text', 'create_on']
        extra_kwargs = {'user_profile': {'read_only': True}}
