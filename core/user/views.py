import re
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from .serializers import ProfileSerializerGet
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from core.user.models import Profile
from django.http import HttpResponse
from django.utils.translation import gettext as _
# from uuid import uuid4

from django.contrib.auth.password_validation import validate_password


# @permission_classes((AllowAny,))
# class Login(APIView):
#     """
#     user should login
#     """
#     def post(self, request):
#         try:
#             email = request.data.get('email')
#             password = request.data.get('password')
#             user = User.objects.get(email=email)
#             if email is None or email=="":
#                 return Response({"error": "empty_email"},
#                             status=HTTP_400_BAD_REQUEST)
#             if password is None or password=="":
#                 return Response({"error": "empty_password"},
#                                 status=HTTP_400_BAD_REQUEST)
#             if not user.check_password(password):
#                 return JsonResponse({
#                     "error": "wrong_information"
#                 }, status=HTTP_404_NOT_FOUND)
#
#             jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#             jwtencode_handler = api_settings.JWT_ENCODE_HANDLER
#             payload = jwt_payload_handler(user)
#             token = jwt_encode_handler(payload)
#             return Response({'token': token})
#
#             return JsonResponse({
#                 "token": token.value,
#             })
#             return Response({'status': 'succeeded'})
#         except User.DoesNotExist:
#             if email is None or email=="":
#                 return Response({"error": "empty_email"},
#                             status=HTTP_400_BAD_REQUEST)
#             return JsonResponse({"error": "wrong_information"},
#                                 status=HTTP_404_NOT_FOUND)


@permission_classes((AllowAny,))
class Register(APIView):
    def post(self, request):
        """"
        this should take email instead of username
        """
        pattern = re.compile("[^@]+@[^@]+\.[^@]+")
        email = request.data.get("email")
        password = request.data.get("password")
        fullname = request.data.get("fullname")
        bio = request.data.get("bio")
        image = request.data.get("image")
        username = request.data.get("username")
        if email is None or email == "":
            return Response({'error': _('empty_email')},
                            status=HTTP_400_BAD_REQUEST)
        if password is None or password == "":
            return Response({'error': _('empty_password')},
                            status=HTTP_400_BAD_REQUEST)
        if not pattern.match(email):
            return Response({'error': _('bad_email')})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if Profile.objects.filter(main_username=username).count() > 0:
            return Response({'error': _('this username is already taken')},
                            status=HTTP_404_NOT_FOUND)
        try:
            validate_password(password)
        except :
            return JsonResponse({"error" : _("weak_password")} , status = HTTP_400_BAD_REQUEST)
        if user is None:
            user = User(username=email, email=email)
            user.set_password(password)
            user.save()
        else:
            return Response({'error': _('this email is already taken')},
                            status=HTTP_404_NOT_FOUND)
        profile = Profile.objects.get(user_id=user.id)
        profile.fullname = fullname
        profile.bio = bio
        profile.main_username = username
        profile.profile_pic = image
        profile.save()
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        # return Response({'token': token})
        return Response({'status': _('succeeded')})

class ChangePassword(APIView):
    """"
       this should change the password
       """
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password is None or old_password == "" or new_password is None or new_password== "":
            return Response({"error": _("empty_password")},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse ( {"error": _("wrong_old_password!")},
                     status = HTTP_404_NOT_FOUND)
        try:
            validate_password(new_password)
        except:
            return JsonResponse({"error" : _("weak_password")} , status = HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return JsonResponse({"status": _("succeeded")})


class ProfileInfo(APIView):
    #TODO: more details for profile should return + profile pic
    """"
    this should show profile of user
    """
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializerGet(profile)
        return JsonResponse(serializer.data)

    """
          this will let user change profile info
       """

    def post(self, request):
        if not request.user:
            return Response({'status': 'failed'})
        new_username = request.data.get("username")
        new_bio = request.data.get("bio")
        new_email = request.data.get("email")
        new_fullname = request.data.get("fullname")
        #       todo add profile picture field for update
        # todo check validation
        user = request.user
        user.email = new_email
        user.username = new_email
        profile = Profile.objects.get(user=user)
        profile.fullname = new_fullname
        profile.bio = new_bio
        profile.main_username = new_username
        user.save()
        profile.save()
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
            username = request.data.get("username")
            bio = request.data.get("bio")
            profile = Profile.objects.get(user=request.user)
            profile.fullname = fullname
            profile.bio = bio
            profile.main_username=username
            profile.save()
            request.user.save()
            return Response({'status': 'succeeded'})