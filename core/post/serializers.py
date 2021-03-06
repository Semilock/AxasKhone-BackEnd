# TODO: Test post with tags work correct

from django.conf import settings
from rest_framework import serializers

from config.utils import show_time_passed
from core.user.serializers import ProfileSerializer
from .models import Post, Favorite, Tag, Comment, Like


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('text', 'number')
        read_only_fields = ('pk',)
        many = True


class LikeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Like
        fields = ('profile',)


class CommentSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('text', 'profile', 'created_at', 'time')
        read_only_fields = ('created_at',)

    def get_username(self, obj):
        return obj.profile.main_username

    def get_user_picture(self, obj):
        if obj.profile.profile_picture == "":
            return ""
        return '%s%s%s' % (settings.SITE_URL, settings.MEDIA_URL, obj.profile.profile_picture)

    def get_time(self, obj):
        return show_time_passed(obj.created_at)


class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()
    tags = TagSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    like_number = serializers.SerializerMethodField()
    comment_number = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
        'image', 'caption', 'pk', 'profile', 'location', 'tags', 'is_liked', 'like_number', 'comment_number',
        'created_at', 'time')

        read_only_fields = ('pk', 'created_at')

    def get_is_liked(self, obj):
        return Like.objects.filter(profile=self.context.get('request').user.profile, post=obj).exists()

    def get_like_number(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_comment_number(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_time(self, obj):
        return show_time_passed(obj.created_at)


class PostSerializerNOTIF(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('image', 'caption', 'pk', 'location', 'tags')

    def get_image(self, instance):
        return '%s%s%s' % (settings.SITE_URL, settings.MEDIA_URL, instance.image)


# TODO: update should change'tags'
class PostSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('image', 'caption', 'location', 'pk', 'tag_string')

    def create(self, validated_data):
        tag_string = validated_data.get('tag_string')
        post = Post.objects.create(**validated_data)
        if tag_string == None:
            return post
        tag_list = tag_string.split()
        for tag in tag_list:
            t, _ = Tag.objects.get_or_create(text=tag)
            t.number += 1
            t.save()
            post.tags.add(t)
        return post


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('title', 'pk')
        read_only_fields = ('pk',)
