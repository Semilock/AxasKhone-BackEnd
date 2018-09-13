#TODO: Test post with tags work correct
import datetime

from django.conf import settings
from django.utils.timezone import utc
from rest_framework import serializers
from core.user.serializers import ProfileSerializer
from .models import Post, Favorite, Tag, Comment, Like


class TagSerializer(serializers.ModelSerializer):
    # number = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields=('text', 'number')
        read_only_fields = ('pk',)
        many=True

    # def get_number(self, obj):
    #     return Tag.objects.filter(text=obj.text).count()

    # def create(self, validated_data):
    #     tag, created = Tag.objects.get_or_create(**validated_data)
    #     tag.number += 1
    #     tag.save()
    #     return tag


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
        fields = ('text', 'username','user_picture', 'created_at')
        read_only_fields = ('created_at',)

    def get_username(self, obj):
        return obj.profile.main_username
    def get_user_picture(self, obj):
        if obj.profile.profile_picture=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, obj.profile.profile_picture)


class PostSerializerGET(serializers.ModelSerializer):
    profile = ProfileSerializer()
    tags = TagSerializer(many=True)
    is_liked = serializers.SerializerMethodField()
    like_number = serializers.SerializerMethodField()
    comment_number = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('url', 'image', 'caption', 'pk', 'profile', 'location', 'tags', 'is_liked', 'like_number', 'comment_number', 'created_at', 'time')

        read_only_fields = ('pk', 'created_at')

    def get_is_liked(self, obj):
        return Like.objects.filter(profile=self.context.get('request').user.profile, post=obj).exists()

    def get_like_number(self, obj):
        return Like.objects.filter(post=obj).count()

    def get_comment_number(self, obj):
        return Comment.objects.filter(post=obj).count()
    def get_time(self,obj):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = int((now - obj.created_at).total_seconds())
        if diff<60:
            return str(diff)+" s"
        elif diff<3600:
            return str(int(diff/60))+" m"
        elif diff<3600*24:
            return str(int(diff/3600))+" h"
        elif diff<7*3600*24:
            return str(int(diff/(3600*24))) + " d"
        else:
            return str(int(diff)/(7*24*3600))+ "w"

class PostSerializerNOTIF(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('image', 'caption', 'pk','location', 'tags')

    def get_image(self,instance):
        return '%s%s%s' % (settings.SITE_URL, settings.MEDIA_URL, instance.image)



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
            t.number +=1
            t.save()
            post.tags.add(t)
        return post


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('title', 'pk')
        read_only_fields = ('pk',)