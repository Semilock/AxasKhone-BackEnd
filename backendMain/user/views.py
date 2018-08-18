from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from backendMain import serializers


def profile_info(request):
    token = request.POST.get('token')
    user = token.user
    profile = user.profile
    serializer = serializers.ProfileSerializer(profile)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


