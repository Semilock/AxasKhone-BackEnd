from rest_framework import serializers
from core.user.models import Profile


class ProfileSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'email', 'username')

class ProfileSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields =( '__all__')