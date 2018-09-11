import json
import requests
from rest_framework import permissions

class VerifiedPermission(permissions.BasePermission):
    """
    Read-only permission for users who
    """

    message = "User email is required to be verified for this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.profile.email_verified


def validate_charfield_input(text, length):
    if len(text) > length:
        return False
    return True


def send_mail(to, subject, body):
    email_api_url = 'http://192.168.10.66:80/api/send/mail'
    headers = {'agent-key': '5pWlxEtieM', 'content-type': 'application/json'}
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
    }
    payload = json.dumps(payload)  # converting to json
    result = requests.post(email_api_url, headers=headers, data=payload)
    return result.status_code
