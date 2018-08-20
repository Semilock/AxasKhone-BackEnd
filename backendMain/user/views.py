from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from backendMain import serializers


from django.contrib.auth.models import User
from django.http import JsonResponse
from user.models import Token
from user.models import Profile
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

        #print ("username" , username)
        #print ("password" , password)
        user= User.objects.get(username= username)
        #return JsonResponse({"username" : user.username})

        if( not user.check_password(password)):
            error = {"password": "پسورد اشتباه است"}
            return JsonResponse(error)
        token = Token(user= user.profile , value=  str(uuid4()))
        token.save()
        user.save()
        #print("token" , token.value)
        return JsonResponse({"Token": token.value,"username": username})

    except User.DoesNotExist:
        error = {"username" : "یوزرنیم اشتباه است"}
        return JsonResponse(error)

def change_password(request):
    try:
        token_value = request.POST.get('token')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        token = Token.objects.get(value = token_value)
        profile= Profile.objects.get(token = token)
        user = User.objects.get(profile = profile)
        if(not user.check_password(old_password)):
            error = {"password" : "پسورد قبلی اشتباه است!"}
            return JsonResponse (error)


        user.set_password(new_password)
        user.save()
        return JsonResponse({"password": "پسورد تغییر یافت"})
    except Token.DoesNotExist :
        error = {"token": "bad_token"}
        return JsonResponse(error)

