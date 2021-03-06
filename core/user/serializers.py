from rest_framework import serializers
from core.user.models import Profile
from rest_framework_jwt.serializers import User
from django.conf import settings

from core.user.models import UserFollow, UserFollowRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

class ProfileSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    is_requested = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    follower_number = serializers.SerializerMethodField()
    following_number = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    requested_me = serializers.SerializerMethodField()

    # user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'main_username', 'is_following', 'is_public', 'email', 'follower_number', 'following_number', 'profile_picture', 'requested_me', 'is_requested' )

    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            pass
        instance.main_username = validated_data.get('main_username')
        instance.fullname = validated_data.get('fullname')
        instance.bio = validated_data.get('bio')
        instance.user.email = serializer.data['email']
        instance.user.username = serializer.data['email']
        instance.profile_picture = serializer.data['profile_picture']
        instance.save()
        return instance

    def get_requested_me(self, obj):
        return UserFollowRequest.objects.filter(source=obj, destination=self.context.get('request').user.profile).exists()

    def get_is_requested(self, obj):
        return UserFollowRequest.objects.filter(source=self.context.get('request').user.profile, destination=obj).exists()

    def get_is_following(self, obj):
        return UserFollow.objects.filter(source=self.context.get('request').user.profile, destination=obj).exists()

    def get_follower_number(self, obj):
        return UserFollow.objects.filter(destination=obj.user.profile).count()

    def get_following_number(self, obj):
        return UserFollow.objects.filter(source=obj.user.profile).count()

    def get_email(self, obj):
        return obj.user.email

    def get_profile_picture(self, instance):
        if instance.profile_picture=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, instance.profile_picture)


class ProfileSerializerNotif(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ('username','profile_picture')

    def get_username(self, obj):
        return obj.main_username
    def get_profile_picture(self, obj):
        if obj.profile_picture=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, obj.profile_picture)

