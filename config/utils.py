import json
import datetime

import requests
from django.utils.timezone import utc
from rest_framework import permissions
import time

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

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

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

def now_ms():
    """

    :return: now in millisecond
    """
    return int(round(time.time() * 1000))


def req_log_message(request, req_time):
    client_IP = request.META.get('REMOTE_ADDR')
    client_url = request.path
    client_user = '' if str(request.user) == 'AnonymousUser' else ':user_{0:d}'.format(request.user.id)
    log_message = '{0}{1} > {2} {3}'.format(client_IP, client_user, request.method, client_url)
    return log_message


def res_log_message(request, log_result, req_time):
    client_IP = request.META.get('REMOTE_ADDR')
    client_user = '' if str(request.user) == 'AnonymousUser' else ':user_{0:d}'.format(request.user.id)
    client_url = request.path
    # log_result = 'Validation failed.'
    response_time = now_ms() - req_time
    log_message = '{0}{1} < {2} {3} {4} {5}ms'.format(client_IP, client_user, request.method,
                                                   client_url, log_result, response_time)
    return log_message


def show_time_passed(time):
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        diff = int((now - time).total_seconds())
        if diff < 60:
            return str(diff) + " s"
        elif diff < 3600:
            return str(int(diff / 60)) + " m"
        elif diff < 3600 * 24:
            return str(int(diff / 3600)) + " h"
        elif diff < 7 * 3600 * 24:
            return str(int(diff / (3600 * 24))) + " d"
        else:
            return str(int(diff) / (7 * 24 * 3600)) + "w"
