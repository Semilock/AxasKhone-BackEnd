from rest_framework import serializers
from core.user.models import Profile
from rest_framework.relations import RelatedField, SlugRelatedField
from rest_framework_jwt.serializers import User
from django.conf import settings


class UserSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email' , 'username')

class ProfileSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'main_username')

class ProfileSerializerGet(serializers.ModelSerializer):
    user = UserSerializerPost()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields =('main_username', 'fullname', 'followers_number', 'following_number', 'bio', 'profile_picture', 'user' )

    def get_profile_picture(self, instance):
        return '%s%s' % (settings.SITE_URL, instance.profile_pic.url)