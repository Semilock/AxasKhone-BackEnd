from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from backendMain import serializers


from django.contrib.auth.models import User
from django.http import JsonResponse
from user.models import Token
from uuid import uuid4


def profile_info(request):
    token = request.POST.get('token')
    user = token.user
    profile = user.profile
    serializer = serializers.ProfileSerializer(profile)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def login(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')

        print ("username" , username)
        print ("password" , password)

        user= User.objects.get(username= username)
        #return JsonResponse({"username" : user.username})

        if( not user.check_password(password)):
            return JsonResponse({"error" : "bad_password" ,})
        token = Token(user= user.profile , value=  str(uuid4()))
       # print("token" , token.value)
        return JsonResponse({"Token": token.value ,"username": username})

    except User.DoesNotExist:
        return JsonResponse({"error" : "bad_username"})

