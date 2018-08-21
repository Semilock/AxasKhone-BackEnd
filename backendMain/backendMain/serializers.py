from django.contrib.auth.models import User
from rest_framework import serializers
from user import models
from user.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('fullname', 'bio', 'email', 'username')