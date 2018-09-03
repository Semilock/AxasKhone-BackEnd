from rest_framework import serializers
from core.user.models import Profile
from rest_framework.fields import CurrentUserDefault
from rest_framework.relations import RelatedField, SlugRelatedField
from rest_framework_jwt.serializers import User
from django.conf import settings

from core.user.models import UserFollow

class UserSerializer(serializers.ModelSerializer):
    is_follow = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('email', 'username', 'is_follow')

    def get_is_follow(self, obj):
        request_user = serializers.PrimaryKeyRelatedField(
            read_only=True,
            default=serializers.CurrentUserDefault()
        )
        return UserFollow.objects.filter(source=obj, destination=obj).exists()


class ProfileSerializerPost(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'main_username', 'user' )

    def update(self, instance, validated_data):
        user_data = validated_data.get('user')
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            pass
        instance.main_username = validated_data.get('main_username')
        instance.fullname = validated_data.get('fullname')
        instance.bio = validated_data.get('bio')
        instance.user.email = serializer.data['email']
        instance.user.username = serializer.data['username']
        instance.save()
        return instance

class ProfileSerializerGet(serializers.ModelSerializer):
    user = UserSerializer()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields =('main_username', 'fullname', 'followers_number', 'following_number', 'bio', 'user', 'profile_picture')

    def get_profile_picture(self, instance):
        if instance.profile_pic=="":
            return ""
        return '%s%s%s' % (settings.SITE_URL,settings.MEDIA_URL, instance.profile_pic)

