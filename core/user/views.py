# TODO: context to all Profile serializers
# TODO:TEST GET , POST PROFILE SERIALIZER
# TODO: email for profile serializer post

from django.contrib.sites import requests
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from config.const import *
from Redis.globals import *
from apps.notif.models import Notification
from config.const import bio_max_length
from config.utils import validate_charfield_input
from core.user.models import UserFollow, UserFollowRequest

from .serializers import ProfileSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.http import JsonResponse
from core.user.models import Profile, PasswordResetRequests
from django.http import HttpResponse
from django.utils.translation import gettext as _
import uuid
import json
# import requests

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
class RegisterValidation(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or email == "":
            return Response({'error': _('empty_email')},
                            status=HTTP_400_BAD_REQUEST)
        if password is None or password == "":
            return Response({'error': _('empty_password')},
                            status=HTTP_400_BAD_REQUEST)
        if not email_pattern.match(email):
            return Response({'error': _('bad_email')})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None:
            return Response({'error': _('this email is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        try:
            validate_password(password)
        except:
            return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)
        return Response({'status': _('succeeded')})


@permission_classes((AllowAny,))
class Register(APIView):
    def post(self, request):
        """"
        this should take email instead of username
        """
        email = request.POST.get("email")
        password = request.POST.get("password")
        fullname = request.POST.get("fullname")
        bio = request.POST.get("bio")
        image = request.FILES.get("profile_picture")
        username = request.POST.get("username")
        if username is None or username == "":
            return JsonResponse({"error": _("please enter username")}, status=HTTP_400_BAD_REQUEST)
        if not username_pattern.match(username):
            return JsonResponse({"error": _("bad username")}, status=HTTP_400_BAD_REQUEST)
        if len(username) < 5:
            return JsonResponse({"error": _("bad username")}, status=HTTP_400_BAD_REQUEST)
        if not validate_charfield_input(bio, bio_max_length):
            return JsonResponse({"error": _("long bio")}, status=HTTP_400_BAD_REQUEST)
        # if email is None or email == "":
        #     return Response({'error': _('empty_email')},
        #                     status=HTTP_400_BAD_REQUEST)
        # if password is None or password == "":
        #     return Response({'error': _('empty_password')},
        #                     status=HTTP_400_BAD_REQUEST)
        # if not pattern.match(email):
        #     return Response({'error': _('bad_email')})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if Profile.objects.filter(main_username=username).count() > 0:
            return Response({'error': _('this username is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        # try:
        #     validate_password(password)
        # except:
        #     return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)
        if user is None:
            user = User(username=email, email=email)
            user.set_password(password)
            user.save()
        else:
            return Response({'error': _('this email is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user_id=user.id)
        profile.fullname = fullname
        profile.bio = bio
        profile.main_username = username
        profile.profile_picture = image
        profile.save()
        # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # payload = jwt_payload_handler(user)
        # token = jwt_encode_handler(payload)
        # return Response({'token': token})
        return Response({'status': _('succeeded')})


@permission_classes((AllowAny,))
class ForgotPassword(APIView):
    """
    View to request password reset.

    * Requires username.
    """

    # TODO: should be logged

    @staticmethod
    def send_password_reset_email(username, email, password_reset_url):
        email_api_url = 'http://192.168.10.66:80/api/send/mail'  # TODO: shouldn't be someplace else?
        subject = "Password reset request for Akkaskhuneh"  # TODO: translate it later
        body = """
               <p>Hello dear {0},</p>
               <p>You can reset your password <a href="{1}">here. Or, ignore this message.</p>
               """.format(username, password_reset_url)  # TODO: translate it later
        payload = {
            "to": email,
            "body": body,
            "subject": subject
        }
        payload = json.dumps(payload)  # converting to json
        headers = {'agent-key': '5pWlxEtieM', 'content-type': 'application/json'}
        result = requests.post(email_api_url, headers=headers, data=payload)
        return result.status_code

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            try:
                PasswordResetRequests.objects.get(user=user).delete()
            except PasswordResetRequests.DoesNotExist:
                pass
            password_reset_request = PasswordResetRequests(user=user)
            token = uuid.uuid4().hex
            password_reset_request.set_token(token)
            password_reset_request.save()

            host_root = request.build_absolute_uri('/')  # example: http://127.0.0.1:8000/
            password_reset_url = '{0}user/reset_password/{1}/'.format(host_root, token)
            # send_mail_response_code = \
            queue.enqueue(ForgotPassword.send_password_reset_email, user.profile.main_username,
                          user.email,
                          password_reset_url)
            # if send_mail_response_code == 200:
            return JsonResponse({"status": _("Succeeded. Please check your email.")},
                                status=HTTP_200_OK)
            # else:
            #     return JsonResponse({"error": _("Failure in sending email. Try later")},
            #                         status=send_mail_response_code)

        except User.DoesNotExist:
            return JsonResponse({"error": _("Wrong_email")},
                                status=HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny,))
class ResetPassword(APIView):
    """
    View to reset password.

    * Requires valid token in url.
    * For validation should contain 'validation' key in body with value 'true'.
    * For updating password should contain 'new_password'.
    """

    def post(self, request, reset_password_token):
        # test
        # print(reset_password_token)
        # print(request.data.get('validation'))
        # test

        # TODO: should be logged

        try:
            password_reset_request = PasswordResetRequests.objects.get(
                hashed_token=PasswordResetRequests.hash_token(reset_password_token)
            )  # may throw DoesNotExist
            if password_reset_request.expired():
                return JsonResponse({"error": _("Invalid_request")},  # TODO: error: expired ?
                                    status=HTTP_400_BAD_REQUEST)
            if request.data.get('validation') == 'true':
                return JsonResponse({"status": _("succeeded")},
                                    status=HTTP_200_OK)

            new_password = request.data.get('new_password')
            try:
                validate_password(new_password)
            except:
                return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)
            user = password_reset_request.user
            user.set_password(new_password)
            user.save()
            password_reset_request.delete()
            # TODOdone: should password_reset_request be disabled ? is deleted
            return JsonResponse({"status": _("succeeded")})
        except PasswordResetRequests.DoesNotExist:
            return JsonResponse({"error": _("Invalid_request")},
                                status=HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):
    """"
       this should change the password
       """

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password is None or old_password == "" or new_password is None or new_password == "":
            return Response({"error": _("empty_password")},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.check_password(old_password):
            return JsonResponse({"error": _("wrong_old_password!")},
                                status=HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password)
        except:
            return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return JsonResponse({"status": _("succeeded")})


class ProfileInfo(APIView):
    """"
    this should show profile of user
    """

    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={'request': request}).data
        return JsonResponse(serializer)

    """
          this will let user change profile info
       """

    def post(self, request):
        new_username = request.data.get("username")
        new_bio = request.data.get("bio")
        new_email = request.data.get("email")
        new_fullname = request.data.get("fullname")
        new_profile_picture = request.data.get("profile_picture")
        user = request.user
        if Profile.objects.filter(main_username=new_username).count() > 0 \
                and not Profile.objects.get(user=user).main_username == new_username:
            return Response({'error': _('this username is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=new_email).count() > 0 and not user.email == new_email:
            return Response({'error': _('this email is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        if not new_email is None:
            if not email_pattern.match(new_email):
                return Response({'error': _('bad_email')},
                                status=HTTP_400_BAD_REQUEST)
            user.email = new_email
            user.username = new_email
        profile = Profile.objects.get(user=user)
        if not new_fullname is None:
            profile.fullname = new_fullname
        if not new_bio is None:
            if not validate_charfield_input(new_bio, bio_max_length):
                return JsonResponse({"error": _("long bio")}, status=HTTP_400_BAD_REQUEST)
            profile.bio = new_bio
        if not new_username is None:
            profile.main_username = new_username
        if not new_profile_picture is None:
            profile.profile_picture = new_profile_picture
        user.save()
        profile.save()
        return Response({'status': _('succeeded')})


class InviteFriends(APIView):
    def post(self, request):
        contacts = []
        contact_list = request.data.get('contact_list')
        for contact in contact_list:
            serializer = {
                "contact_email": contact["email"], "contact_name": contact["name"]
            }
            contact_user = Profile.objects.filter(user__email=contact["email"]).first()
            if contact_user is not None:
                serializer['user'] = ProfileSerializer(contact_user, context={'request': request}).data
            if contact_user is None:
                serializer['user'] = "not_found"
            contacts.append(serializer)
        return JsonResponse({"contacts": contacts})


class Follow(APIView):
    def post(self, request):
        source = request.user.profile
        destination_username = request.data.get('username')
        destination = Profile.objects.filter(main_username=destination_username).first()
        if destination is None:
            return JsonResponse({"error": "user_not_find"}, status=HTTP_400_BAD_REQUEST)
        if UserFollow.objects.filter(source=source, destination=destination).exists():
            return JsonResponse({"error": "already_followed"}, status=HTTP_400_BAD_REQUEST)
        if destination.is_public:
            queue.enqueue(create_user_follow, destination, source)
            return JsonResponse({"status": "done"})
        else:
            queue.enqueue(create_user_follow_request, destination, source)
            return JsonResponse({"statuas": "follow_request_sent"})


class Accept(APIView):
    def post(self, request):
        destination = request.user.profile
        source_username = request.data.get('username')
        source = Profile.objects.filter(main_username=source_username).first()
        if source is None:
            return JsonResponse({"error": "user_not_find"}, status=HTTP_400_BAD_REQUEST)
        if UserFollow.objects.filter(source=source, destination=destination).exists():
            return JsonResponse({"error": "already_followed"}, status=HTTP_400_BAD_REQUEST)
        if (UserFollowRequest.objects.filter(source=source, destination=destination).exists()):
            queue.enqueue(create_accept_follow_request, destination, source)
            return JsonResponse({"status": "done"})
        else:
            return JsonResponse({"error": "not_followed"}, status=HTTP_400_BAD_REQUEST)


#
# class FollowerList(generics.ListCreateAPIView):
#     def get(self, request):a bit bug debuged!
#         follower_list=[]
#         followers = UserFollow.objects.filter(destination= request.user.profile)
#         for follower in followers:
#             follower_profile = ProfileSerializer(follower.source,  context={'request': request} ).data
#             follower_list.append(follower_profile)
#         return JsonResponse({"follower_list":follower_list})
#
# class FollowingList(APIView):
#     def get(self, request):
#         following_list=[]
#         followings = UserFollow.objects.filter(source= request.user.profile)
#         for following in followings:
#             following_profile = ProfileSerializer(following.destination,  context={'request': request} ).data
#             following_list.append(following_profile)
#         return JsonResponse({"following_list":following_list})


def create_user_follow(destination, source):
    UserFollow.objects.create(source=source, destination=destination)
    notif = Notification(type=follow_type, receiver=destination, sender=source, object=destination)
    notif.you = True
    notif.save()
    # create_follow_notif_for_friends(destination, source)


# def create_follow_notif_for_friends(destination, source):
#     friends = source.followers.list
#     for friend in friends:
#         if not friend==destination:
#             print(friend.main_username)
#             notif = Notification(type=follow_type, receiver=friend, sender=source, object=destination)
#             notif.you = False
#             notif.save()


def create_user_follow_request(destination, source):
    UserFollowRequest.objects.create(source=source, destination=destination)
    notif = Notification(type=follow_request_type, receiver=destination, sender=source, object=destination)
    notif.you = True
    notif.save()


def create_accept_follow_request(destination, source):
    UserFollow.objects.create(source=source, destination=destination)
    notif = Notification(type=accept_follow_request_type, receiver=source, sender=destination, object=source)
    notif.you = True
    notif.save()
    accepting_user = Notification(type=follow_type, you=True, receiver=destination, sender=source, object=source)
    accepting_user.save()
    # create_follow_notif_for_friends(destination, source)

