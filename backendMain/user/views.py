from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from rest_framework.compat import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from backendMain.serializers import ProfileSerializerGet
from .models import create_user_profile
from rest_framework_jwt.settings import api_settings
from backendMain import serializers
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from user.models import Profile
from uuid import uuid4


def profile_info(request):
    token = request.POST.get('token')
    user = token.user
    profile = user.profile
    serializer = serializers.ProfileSerializerPost(profile)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def login(request):
#
#     try:
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = User.objects.get(username=username)
#         if not user.check_password(password):
#             return JsonResponse({
#                 "error": "wrong_password",
#             })
#
#         #token = Token(value=str(uuid4()), profile=user.profile)
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#         payload = jwt_payload_handler(user)
#         token = jwt_encode_handler(payload)
#         return Response({'token': token})
#
#         token.save()
#         return JsonResponse({
#             "token": token.value,
#         })
#     except User.DoesNotExist:
#         return JsonResponse({
#             "error": "wrong_username",
#         })
#

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register(request):
    ##we should check empty fields! work on it!
    """"
    this should take email instead of username
    """
    email = request.data.get("email")
    password = request.data.get("password")
    if email is None or email == "" or password is None or password == "":
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = None
    if user is None:
        user = User(username=email, email=email)
        user.set_password(password)
        user.save()
    else:
        return Response({'error': 'this email is already taken'},
                        status=HTTP_404_NOT_FOUND)
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return Response({'token': token})


@csrf_exempt
@api_view(["POST"])
def change_password(request):
    # we should check empty fields! work on it!
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')
    if old_password is None or new_password is None:
        return Response({'error': 'Please provide both old and new password'},
                        status=HTTP_400_BAD_REQUEST)
    user = request.user
    if (not user.check_password(old_password)):
        error = {"error": "wrong_old_password!"}
        return JsonResponse(error)
    user.set_password(new_password)
    user.save()

    return JsonResponse({"change_password": "done"})


@csrf_exempt
@api_view(["GET"])
def profile_info(request):
    # more details for profile should return
    """"
    this should show profile of user
    """
    user = request.user
    profile = Profile.objects.get(user=user)
    serializer = ProfileSerializerGet(profile)
    return JsonResponse(serializer.data)


def register_complement(request):  # argahvan is working on it
    if not request.user:
        return Response({'status': 'failed'})
    else:
        fullname = request.data.get("fullname")
        username = request.data.get("username")
        bio = request.data.get("bio")
        request.user.profile.fullname(fullname)
        request.user.username(username)
        request.profile.bio(bio)
        request.user.profile.save()
        request.user.save()
        return Response({'status': 'succeeded'})


class UsersViewApi(APIView):
    def get(self, request):
        return JsonResponse({'user': request.user.username})

    def post(self, request):
        return JsonResponse({'user': request.user.username})


class RegisterComplementView(APIView):
    def post(self, request):
        if not request.user:
            return Response({'status': 'failed'})
        else:
            fullname = request.data.get('fullname')
            email = request.data.get("email")
            bio = request.data.get("bio")
            profile = Profile.objects.get(user=request.user)
            profile.fullname = fullname
            request.user.email = email
            profile.bio = bio
            profile.save()
            request.user.save()
            return Response({'status': 'succeeded'})
