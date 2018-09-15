import logging
from django.utils.timezone import now
from rest_framework import status
from config.utils import req_log_message, res_log_message, now_ms

logger = logging.getLogger(__name__)

# TODO: edit this
# class LoggingMixin(object):
#     # log only when one of the following methods is being performed
#     allowed_logging_methods = ('post', 'put', 'patch', 'delete',
#                                'get', )
#
#     def finalize_response(self, request, response, *args, **kwargs):
#         # regular finalize response
#         response = super().finalize_response(request, response, *args, **kwargs)
#         # do not log, if method not found
#         if request.method.lower() not in self.allowed_logging_methods:
#             return response
#         status_code = response.status_code
#
#         time_delta = now() - self.request.info['date']
#         response_time_ms = time_delta.total_seconds() * 1000
#
#         log_kwargs = {
#             'view': self.get_view_name(),
#             'action': self.action,
#             'method': request.method.lower(),
#             'status_code': status_code,
#             'response_time_ms': round(response_time_ms, 2),
#             'request_path': request.path,
#         }
#         if status.is_server_error(status_code):
#             logger.error('error', extra=log_kwargs)
#         elif status.is_client_error(status_code):
#             logger.warning('warning', extra=log_kwargs)
#         else:
#             logger.info('info', extra=log_kwargs)
#         return response