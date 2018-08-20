from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.compat import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .models import create_user_profile
from rest_framework_jwt.settings import api_settings
from backendMain import serializers

from django.contrib.auth.models import User
from django.http import JsonResponse
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


# def login(request):
#     try:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         print("username", username)
#         print("password", password)
#         user = User.objects.get(username=username)
#         # return JsonResponse({"username" : user.username})
#
#         if (not user.check_password(password)):
#             error = {"password": "پسورد اشتباه است"}
#             return JsonResponse(error)
#         token = Token(user=user.profile, value=str(uuid4()))
#         print("token", token.value)
#         return JsonResponse({"Token": token.value, "username": username})
#
#     except User.DoesNotExist:
#         error = {"username": "یوزرنیم اشتباه است"}
#         return JsonResponse(error)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    """"
    this should take email instead of password
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        user = User(username=username)
        user.set_password(password)
        user.save()
    else:
        return Response({'error': 'this username is already taken'},
                        status=HTTP_404_NOT_FOUND)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response({'token': token})


def register_complement(request):  # argahvan is working on it
    if not request.user:
        return Response({'status': 'failed'})
    else:
        fullname = request.data.get("fullname")
        email = request.data.get("email")
        bio = request.data.get("bio")
        request.user.profile.fullname(fullname)
        request.user.email(email)
        request.profile.bio(bio)
        request.user.profile.save()
        request.user.save()
        return Response({'status': 'succeeded'})
