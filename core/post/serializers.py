from rest_framework import serializers

from core.user.serializers import ProfileSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'profile')

class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'profile')

class PostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption')