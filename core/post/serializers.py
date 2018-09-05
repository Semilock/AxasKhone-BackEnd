from rest_framework import serializers
from core.user.serializers import ProfileSerializer
from .models import Post, Favorite

class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'profile')

class PostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Post
        partial = True
        fields = ('url', 'image', 'caption', 'pk')
        # read_only_fields = ('pk',)


class FavoriteSerializer(serializers.ModelSerializer):
    posts = PostSerializerGET(many=True)
    class Meta:
        model = Favorite
        fields = ('title', 'pk', 'posts')
        read_only_fields = ('pk','posts')
