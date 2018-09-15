import logging

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.views import status

from Redis.globals import *
from apps.notif.models import Notification
from config.utils import now_ms, req_log_message, res_log_message
from core.user.models import Profile, UserFollow
from core.user.views import ForgotPassword, VerificationRequest

logger = logging.getLogger(__name__)

@permission_classes((AllowAny,))
class RedisActions(APIView):
    def post(self, request):
        req_time = now_ms()
        logger.info(req_log_message(request, req_time))
        if str(request.META.get("REMOTE_ADDR")) == "127.0.0.1":
            type = request.data.get("type")
            if type == forgot_password_type:
                return self.forgot_pass_mail(request, req_time)
            if type == email_verification_type:
                return self.verify_email(request, req_time)
            receiver = request.data.get("receiver")
            sender = request.data.get("sender")
            object = request.data.get("object")
            you = request.data.get("you")
            id = request.data.get("id")
            if type != comment_type and \
                    Notification.objects.filter(type=type,
                                                receiver=Profile.objects.get(id=receiver),
                                                sender=Profile.objects.get(id=sender),
                                                object=Profile.objects.get(id=object),
                                                you=True).exists():
                return Response(status=status.HTTP_200_OK)
            if type==unfollow_type:
                Notification.objects.filter(type=follow_request_type,
                                            receiver=Profile.objects.get(id=receiver),
                                            sender=Profile.objects.get(id=sender),
                                            object=Profile.objects.get(id=object),
                                            ).delete()
                return Response(status=status.HTTP_200_OK)

            if type == follow_type:
                self.delete_follow_request_notif(object, receiver, sender)
            notif = Notification(type=type,
                                 receiver=Profile.objects.get(id=receiver),
                                 sender=Profile.objects.get(id=sender),
                                 object=Profile.objects.get(id=object),
                                 you=you)
            notif.save()
            if id > 0:
                notif.data = id
                notif.save()
            if type == follow_type:
                self.create_notif_for_all_followers(object, sender, type)
            log_result = 'user(id={0}) notif successfully handled from redis queue'.format(sender.id)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return Response(status=status.HTTP_200_OK)
        else:
            log_result = 'try to send request to internal api of redis'
            log_message = res_log_message(request, log_result, req_time)
            logger.error(log_message)
            return Response(status=status.HTTP_403_FORBIDDEN)

    def delete_follow_request_notif(self, object, receiver, sender):
        if Notification.objects.filter(type=follow_request_type,
                                       receiver=Profile.objects.get(id=receiver),
                                       sender=Profile.objects.get(id=sender),
                                       you=True).exists():
            Notification.objects.get(type=follow_request_type,
                                     receiver=Profile.objects.get(id=receiver),
                                     sender=Profile.objects.get(id=sender),
                                     you=True).delete()

    def create_notif_for_all_followers(self, object, sender, type):
        user_followers = UserFollow.objects.filter(destination=sender)
        for f in user_followers:
            if not (Notification.objects.filter(type=type,
                                                receiver=f.source,
                                                sender=Profile.objects.get(id=sender),
                                                you=True).exists()):
                notif = Notification(type=type,
                                     receiver=f.source,
                                     sender=Profile.objects.get(id=sender),
                                     object=Profile.objects.get(id=object),
                                     you=False)
                notif.save()

    def forgot_pass_mail(self, request, req_time):
        username = request.data.get("username")
        email = request.data.get("email")
        url = request.data.get("url")
        send_mail_response_code = \
            ForgotPassword.send_password_reset_email(username,
                                                     email,
                                                     url)
        if send_mail_response_code == 200:
            log_result = 'forgot password mail successfully sent to user(id={0})'.format(User.objects.get(profile__main_username=username))
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"status": _("Succeeded. Please check your email.")},
                                status=HTTP_200_OK)
        else:
            log_result = 'fail to send forgot password mail to user(id={0})'.format(User.objects.get(profile__main_username=username))
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return JsonResponse({"error": _("Failure in sending email. Try later")},
                                status=send_mail_response_code)

    def verify_email(self, request, req_time):
        username = request.data.get("username")
        email = request.data.get("email")
        url = request.data.get("url")
        send_mail_response_code = \
            VerificationRequest.send_verification_email(username,
                                                        email,
                                                        url)
        if send_mail_response_code == 200:
            log_result = 'verification mail successfully sent to user(id={0})'.format(
                User.objects.get(profile__main_username=username))
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
            return JsonResponse({"status": _("Succeeded. Please check your email.")},
                                status=HTTP_200_OK)
        else:
            log_result = 'fail to send verification mail to user(id={0})'.format(
                User.objects.get(profile__main_username=username))
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
            return JsonResponse({"error": _("Failure in sending email. Try later")},
                                status=send_mail_response_code)
