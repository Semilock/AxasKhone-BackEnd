#TODO: Test post with tags work correctly
from django.conf import settings
from rest_framework import serializers
from core.user.serializers import ProfileSerializer
from .models import Post, Favorite, Tag, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('text' ,)
        read_only_fields = ('pk',)

    def create(self, validated_data):
        tag, created = Tag.objects.get_or_create(**validated_data)
        # if not created:
        #     raise exceptions.ValidationError(validated_data['name'] + " already exists.")
        return tag


class LikeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_picture = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('username','user_picture')

    def get_username(self, obj):
        return obj.profile.main_username
    def get_user_picture(self, obj):
        if obj.profile.profile_picture=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, obj.profile.profile_picture)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_picture = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('text', 'username','user_picture')

    def get_username(self, obj):
        return obj.profile.main_username
    def get_user_picture(self, obj):
        if obj.profile.profile_picture=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, obj.profile.profile_picture)


class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'pk', 'profile', 'location', 'tags')

        read_only_fields = ('pk',)

    # def get_tag_text(self,obj):
    #     return obj.tags.text

#TODO: update should change'tags'
class PostSerializerPOST(serializers.ModelSerializer):
    # tags = TagSerializer(many=True)
    class Meta:
        model = Post
        fields = ('url', 'image', 'caption','location', 'pk','tag_string')

    # def create(self, validated_data):
    #     tags_data = validated_data.pop('tags', [])
    #     post = Post.objects.create(**validated_data)
    #     for tag in tags_data:
    #         t, _ = Tag.objects.get_or_create(text=tag["text"])
    #         post.tags.add(t)
    #     return post

    def create(self, validated_data):
        tag_string = validated_data.get('tag_string')
        post = Post.objects.create(**validated_data)
        if tag_string ==None:
            return post
        tag_list=tag_string.split()
        for tag in tag_list:
            t, _ = Tag.objects.get_or_create(text=tag)
            post.tags.add(t)
        return post


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('title', 'pk')
        read_only_fields = ('pk',)