from rest_framework import serializers
from .models import Post, Favorite


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        partial = True
        fields = ('url', 'image', 'caption', 'pk')
        # read_only_fields = ('pk',)


class FavoriteSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    class Meta:
        model = Favorite
        fields = ('title', 'pk', 'posts')
        read_only_fields = ('pk','posts')

