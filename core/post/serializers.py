from rest_framework import serializers
from .models import Post, Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('title')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        partial = True
        fields = ('url', 'image', 'caption', 'pk')

