from rest_framework import serializers
from core.user.models import Profile
from rest_framework.relations import RelatedField, SlugRelatedField
from rest_framework_jwt.serializers import User


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
    class Meta:
        model = Profile
        fields =('main_username', 'fullname', 'followers_number', 'following_number', 'bio', 'profile_pic', 'user' )