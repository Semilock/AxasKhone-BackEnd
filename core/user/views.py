# TODO: context to all Profile serializers
# TODO:TEST GET , POST PROFILE SERIALIZER
# TODO: email for profile serializer post

import json
import logging
import uuid

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.utils.translation import gettext as _
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from Redis.globals import *
from Redis.globals import queue
from config.const import *
from config.const import bio_max_length
from config.utils import send_mail, VerifiedPermission, now_ms, req_log_message, res_log_message
from config.utils import validate_charfield_input
from core.user.models import Profile, PasswordResetRequests, EmailVerificationRequests
from core.user.models import UserFollow, UserFollowRequest
from .serializers import ProfileSerializer



logger = logging.getLogger(__name__)



@permission_classes((AllowAny,))
class RegisterValidation(APIView):
    # no logging needed
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
            return Response({'error': _('bad_email')},
                            status=HTTP_400_BAD_REQUEST)
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
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)


        email = request.POST.get("email")
        password = request.POST.get("password")
        fullname = request.POST.get("fullname")
        bio = request.POST.get("bio")
        image = request.FILES.get("profile_picture")
        username = request.POST.get("username")

        response = RegisterValidation()
        response = response.post(request)

        if response.status_code == 400:
            log_result = 'Fail: Validation failed'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return (response)

        if username is None or username == "":
            log_result = 'Fail: No username'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("please enter username")}, status=HTTP_400_BAD_REQUEST)
        if not username_pattern.match(username):
            log_result = 'Fail: Invalid username'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("bad username")}, status=HTTP_400_BAD_REQUEST)
        if len(username) < 5:
            log_result = 'Fail: No username'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("bad username")}, status=HTTP_400_BAD_REQUEST)
        if not validate_charfield_input(bio, bio_max_length):
            log_result = 'Fail: No username'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("long bio")}, status=HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if Profile.objects.filter(main_username=username).count() > 0:
            log_result = 'Fail: Username already taken'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
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
            log_result = 'Fail: Email already taken'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'error': _('this email is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user_id=user.id)
        profile.fullname = fullname
        profile.bio = bio
        profile.main_username = username
        profile.profile_picture = image
        profile.save()
        log_result = 'Success: User_{0} registered'.format(user.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')})


@permission_classes((AllowAny,))
class ForgotPassword(APIView):
    """
    View to request password reset.

    * Requires username.
    """

    @staticmethod
    def send_password_reset_email(username, email, password_reset_url):
        subject = "Password reset request for Akkaskhuneh"  # TODO: translate it later
        body = """
               <p>Hello dear {0},</p>
               <p>You can reset your password <a href="{1}">here</a>. Or, ignore this message.</p>
               """.format(username, password_reset_url)  # TODO: translate it later

        return send_mail(email, subject, body)

    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            # logger.info('Forgot password request for user {0}, from {1}.'.format(user.id, client_IP))

        except User.DoesNotExist:
            log_result = 'Fail: Forgot password request for non-existent email {0}'.format(email)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("Wrong_email")},
                                status=HTTP_400_BAD_REQUEST)
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
        #     ForgotPassword.send_password_reset_email(user.profile.main_username,
        #                                              user.email,
        #                                              password_reset_url)
        data = {"type": forgot_password_type,
                "username": user.profile.main_username,
                "email": user.email,
                "url": password_reset_url}
        queue.enqueue(json.dumps(data))

        log_result = 'Success: Reset password email for user_{0} sent to {1}'.format(
            user.id, email)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)

        # if send_mail_response_code == 200:
        return JsonResponse({"status": _("Succeeded. Please check your email.")},
                            status=HTTP_200_OK)
        # else:
        #     return JsonResponse({"error": _("Failure in sending email. Try later")},
        #                         status=send_mail_response_code)


@permission_classes((AllowAny,))
class ResetPassword(APIView):
    """
    View to reset password.

    * Requires valid token in url.
    * For validation should contain 'validation' key in body with value 'true'.
    * For updating password should contain 'new_password'.
    """

    def post(self, request, reset_password_token):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        try:
            password_reset_request = PasswordResetRequests.objects.get(
                hashed_token=PasswordResetRequests.hash_token(reset_password_token)
            )  # may throw DoesNotExist
        except PasswordResetRequests.DoesNotExist:
            log_result = 'Fail: Invalid token'
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return JsonResponse({"error": _("Invalid_request")},
                                status=HTTP_400_BAD_REQUEST)
        if password_reset_request.expired():
            log_result = 'Fail: Expired token'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            password_reset_request.delete()
            return JsonResponse({"error": _("Invalid_request")},  # TODO: error: expired ?
                                status=HTTP_400_BAD_REQUEST)
        if request.data.get('validation') == 'true':
            log_result = 'Success: Token passed validation'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"status": _("succeeded")},
                                status=HTTP_200_OK)

        new_password = request.data.get('new_password')
        user = password_reset_request.user
        try:
            validate_password(new_password)
        except:
            log_result = 'Fail: New password failed validation'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        password_reset_request.delete()
        log_result = 'Success: Password reset for user_{0}'.format(user.id)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)

        # TODOdone: should password_reset_request be disabled ? is deleted
        return JsonResponse({"status": _("succeeded")})


class VerificationRequest(APIView):

    @staticmethod
    def send_verification_email(username, email, email_verification_url):
        # email_api_url = 'http://192.168.10.66:80/api/send/mail'  # TODO: shouldn't be someplace else?
        subject = "Email verification for Akkaskhuneh"  # TODO: translate it later
        body = """
                   <p>Hello dear {0},</p>
                   <p>You can verify your email <a href="{1}">here</a>. Until you do, your access will be limited.</p>
                   """.format(username, email_verification_url)  # TODO: translate it later

        return send_mail(email, subject, body)

    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        user = request.user
        profile = user.profile
        if profile.email_verified:
            log_result = 'Fail: Already verified'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("Already verified")},
                                status=HTTP_400_BAD_REQUEST)
        try:
            EmailVerificationRequests.objects.get(profile=profile).delete()
        except EmailVerificationRequests.DoesNotExist:
            pass
        email_verification_request = EmailVerificationRequests(profile=profile)
        token = uuid.uuid4().hex
        email_verification_request.set_token(token)
        email_verification_request.save()

        host_root = request.build_absolute_uri('/')  # example: http://127.0.0.1:8000/
        email_verification_url = '{0}user/verify_email/{1}/'.format(host_root, token)
        # send_mail_response_code = \
        #     VerificationRequest.send_verification_email(profile.main_username,
        #                                                 user.email,
        #                                                 email_verification_url)
        data = {"type": email_verification_type,
                "username": profile.main_username,
                "email": user.email,
                "url": email_verification_url}
        queue.enqueue(json.dumps(data))
        # queue.enqueue(ForgotPassword.send_password_reset_email, user.profile.main_username,
        #               user.email,
        #               password_reset_url)
        # if send_mail_response_code == 200:
        log_result = 'Success: Verification email sent'
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return JsonResponse({"status": _("Succeeded. Please check your email.")},
                            status=HTTP_200_OK)
        # else:
        #     return JsonResponse({"error": _("Failure in sending email. Try later")},
        #                         status=send_mail_response_code)


@permission_classes((AllowAny,))
class VerifyEmail(APIView):
    def get(self, request, email_verification_token):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)
        verify_template = loader.get_template('email_verified.html')
        try:
            email_verification_request = EmailVerificationRequests.objects.get(
                hashed_token=EmailVerificationRequests.hash_token(email_verification_token)
            )  # may throw DoesNotExist
            if email_verification_request.expired():
                log_result = 'Fail: Token expired'
                log_message = res_log_message(request, log_result, req_time)
                logger.info(log_message)
                return HttpResponse(verify_template.render({'message': 'your token is expired. please try again!'}))

            profile = email_verification_request.profile
            if profile.email_verified:
                log_result = 'Success: Already verified'
                log_message = res_log_message(request, log_result, req_time)
                logger.info(log_message)
                return HttpResponse(verify_template.render({'message': 'your email is already verified!'}))
            profile.email_verified = True
            profile.save()
            email_verification_request.delete()
            log_result = 'Success: Email verified'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return HttpResponse(verify_template.render({'message': 'email successfully verified:)'}))
        except EmailVerificationRequests.DoesNotExist:
            log_result = 'Fail: non-existent token'
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return HttpResponse(verify_template.render({'message': 'invalid request!'}))


class ChangePassword(APIView):
    """"
       this should change the password
       """

    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if old_password is None or old_password == "" or new_password is None or new_password == "":
            log_result = 'Fail: Empty password'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({"error": _("empty_password")},
                            status=HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.check_password(old_password):
            log_result = 'Fail: Wrong old password'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("wrong_old_password!")},
                                status=HTTP_400_BAD_REQUEST)
        try:
            validate_password(new_password)
        except:
            log_result = 'Fail: New password failed validation'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"error": _("weak_password")}, status=HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        log_result = 'Success: Password changed'
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return JsonResponse({"status": _("succeeded")})


class ProfileInfo(APIView):
    """"
    this should show profile of user
    """

    def get(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, context={'request': request}).data

        log_result = 'Success: Profile info sent'
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return JsonResponse(serializer)

    """
          this will let user change profile info
       """

    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        new_username = request.data.get("username")
        new_bio = request.data.get("bio")
        new_email = request.data.get("email")
        new_fullname = request.data.get("fullname")
        new_profile_picture = request.data.get("profile_picture")
        user = request.user
        if Profile.objects.filter(main_username=new_username).count() > 0 \
                and not Profile.objects.get(user=user).main_username == new_username:
            log_result = 'Fail: username already taken'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'error': _('this username is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        elif User.objects.filter(email=new_email).count() > 0 and not user.email == new_email:
            log_result = 'Fail: Email already taken'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response({'error': _('this email is already taken')},
                            status=HTTP_400_BAD_REQUEST)
        if not new_email is None:
            if not email_pattern.match(new_email):
                log_result = 'Fail: Email failed validation'
                log_message = res_log_message(request, log_result, req_time)
                logger.info(log_message)
                return Response({'error': _('bad_email')},
                                status=HTTP_400_BAD_REQUEST)
            user.email = new_email
            user.username = new_email
        profile = Profile.objects.get(user=user)
        if not new_fullname is None:
            profile.fullname = new_fullname
        if not new_bio is None:
            if not validate_charfield_input(new_bio, bio_max_length):
                log_result = 'Fail: bio exceeded max length'
                log_message = res_log_message(request, log_result, req_time)
                logger.info(log_message)
                return JsonResponse({"error": _("long bio")}, status=HTTP_400_BAD_REQUEST)
            profile.bio = new_bio
        if not new_username is None:
            profile.main_username = new_username
        if not new_profile_picture is None:
            profile.profile_picture = new_profile_picture
        user.save()
        profile.save()

        log_result = 'Success: Profile info set'
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return Response({'status': _('succeeded')})


@permission_classes((VerifiedPermission,))
class InviteFriends(APIView):
    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

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

        log_result = 'Success'  # TODO: elaborate?
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return JsonResponse({"contacts": contacts})

@permission_classes((VerifiedPermission,))
class Invite(APIView):
    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        invitee_email = request.data.get('email')
        fullname = request.user.profile.fullname
        username = request.user.profile.main_username
        inviter_name = fullname if fullname is not None and len(fullname) > 0 else username
        # TODO: make a db table for invitations
        # TODO: then don't permit inviting members and only allow single time invitations

        subject = "Invitation to join Akkaskhuneh"
        body = """
        <p>Hello,</p>
        <p>{0} invited you to join Akkaskhuneh</p>
        <p>Don't hesitate. Akkaskhuneh is far better than instagram, etc.</p>
        <p>Hurry!</p>
        """.format(inviter_name)
        # send_mail(invitee_email, subject, body)
        data = {"type": invite_mail_type,
                "email": invitee_email,
                "subject":subject,
                "body":body}
        queue.enqueue(json.dumps(data))
        response = JsonResponse({'Success': _('Invitation email sent')},
                                status=HTTP_200_OK)

        log_result = 'Success: Invitation sent to {0}'.format(invitee_email)
        log_message = res_log_message(request, log_result, req_time)
        logger.info(log_message)
        return response


@permission_classes((VerifiedPermission,))
class Follow(APIView):
    def post(self, request):
        source = request.user.profile
        destination_username = request.data.get('username')
        destination = Profile.objects.filter(main_username=destination_username).first()
        if destination is None:
            return JsonResponse({"error": "user_not_find"}, status=HTTP_400_BAD_REQUEST)
        if UserFollow.objects.filter(source=source, destination=destination).exists():
            UserFollow.objects.get(source=source, destination=destination).delete()
            data = {"type": unfollow_type,
                    "receiver": destination.id,
                    "sender": source.id,
                    "you": True,
                    "object": destination.id,
                    "id": 0
                    }
            queue.enqueue(json.dumps(data))
            return JsonResponse({"status": "unfollowed"})
        if destination.is_public:
            UserFollow.objects.create(source=source, destination=destination)
            data = {"type": follow_type,
                    "receiver": destination.id,
                    "sender": source.id,
                    "you": True,
                    "object": destination.id,
                    "id": 0
                    }
            queue.enqueue(json.dumps(data))
            return JsonResponse({"status": "followed"})
        else:
            if UserFollowRequest.objects.filter(source=source, destination=destination).exists():
                UserFollowRequest.objects.filter(source=source, destination=destination).delete()
                data = {"type": unfollow_type,
                        "receiver": destination.id,
                        "sender": source.id,
                        "you": True,
                        "object": destination.id,
                        "id": 0
                        }
                queue.enqueue(json.dumps(data))
                return JsonResponse({"status": "unfollowed"})
            UserFollowRequest.objects.create(source=source, destination=destination)
            data = {"type": follow_request_type,
                    "receiver": destination.id,
                    "sender": source.id,
                    "you": True,
                    "object": destination.id,
                    "id": 0
                    }
            queue.enqueue(json.dumps(data))
            return JsonResponse({"statuas": "follow_request_sent"})


@permission_classes((VerifiedPermission,))
class Accept(APIView):
    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        destination = request.user.profile
        source_username = request.data.get('username')
        source = Profile.objects.filter(main_username=source_username).first()
        if source is None:
            log_result = 'Fail: User not found'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)

            return JsonResponse({"error": "user_not_find"}, status=HTTP_400_BAD_REQUEST)
        # TODO: log this
        return accept_handler(destination, source)


class PublicPrivate(APIView):
    def post(self, request):
        req_time = now_ms()
        log_message = req_log_message(request, req_time)
        logger.info(log_message)

        profile = request.user.profile
        if profile.is_public:
            profile.is_public = False
            profile.save()

            log_result = 'Success: Profile set to private'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"status": "private"})
        else:
            profile.is_public = True
            profile.save()
            query = UserFollowRequest.objects.filter(destination=profile)
            for q in query:
                accept_handler(source=q.source , destination=profile)

            log_result = 'Success: Profile set to public'
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"status": "public"})


def accept_handler(destination, source):
    if UserFollow.objects.filter(source=source, destination=destination).exists():
        return JsonResponse({"error": "already_followed"}, status=HTTP_400_BAD_REQUEST)
    if (UserFollowRequest.objects.filter(source=source, destination=destination).exists()):
        UserFollowRequest.objects.filter(source=source, destination=destination).delete()
        UserFollow.objects.create(source=source, destination=destination)
        data = {"type": accept_follow_request_type,
                "receiver": source.id,
                "sender": destination.id,
                "you": True,
                "object": source.id,
                "id": 0
                }
        queue.enqueue(json.dumps(data))
        data = {"type": follow_type,
                "receiver": destination.id,
                "sender": source.id,
                "you": True,
                "object": source.id,
                "id": 0
                }
        queue.enqueue(json.dumps(data))
        return JsonResponse({"status": "done"})
    else:
        return JsonResponse({"error": "not_followed"}, status=HTTP_400_BAD_REQUEST)
