from rest_framework import serializers
from user import models


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.EmailField
    fullname = serializers.CharField(max_length=200)
    bio = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return models.Profile(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.bio = validated_data.get('bio', instance.bio)
        return instance
    #todo:checkForBio