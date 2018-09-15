from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView, status
from django.utils.translation import gettext as _
from apps.notif.models import Notification
from core.user.models import Profile, UserFollow
from Redis.globals import *
from core.user.views import ForgotPassword, VerificationRequest


@permission_classes((AllowAny,))
class RedisActions(APIView):
    def post(self, request):
        if str(request.META.get("REMOTE_ADDR")) == "127.0.0.1":
            type = request.data.get("type")
            if type == forgot_password_type:
                return self.forgot_pass_mail(request)
            if type == email_verification_type:
                return self.verify_email(request)
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
            return Response(status=status.HTTP_200_OK)
        else:
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

    def forgot_pass_mail(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        url = request.data.get("url")
        send_mail_response_code = \
            ForgotPassword.send_password_reset_email(username,
                                                     email,
                                                     url)
        if send_mail_response_code == 200:
            return JsonResponse({"status": _("Succeeded. Please check your email.")},
                                status=HTTP_200_OK)
        else:
            return JsonResponse({"error": _("Failure in sending email. Try later")},
                                status=send_mail_response_code)

    def verify_email(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        url = request.data.get("url")
        send_mail_response_code = \
            VerificationRequest.send_verification_email(username,
                                                        email,
                                                        url)
        if send_mail_response_code == 200:
            return JsonResponse({"status": _("Succeeded. Please check your email.")},
                                status=HTTP_200_OK)
        else:
            return JsonResponse({"error": _("Failure in sending email. Try later")},
                                status=send_mail_response_code)
