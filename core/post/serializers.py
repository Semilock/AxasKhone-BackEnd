from rest_framework import serializers
from core.user.serializers import ProfileSerializer
from .models import Post, Favorite


class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'pk', 'profile')
        # read_only_fields = ('pk',)


class PostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'pk')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('title', 'pk')
        read_only_fields = ('pk',)
