import logging
from django.utils.timezone import now
from rest_framework import status
from config.utils import req_log_message, res_log_message, now_ms

logger = logging.getLogger(__name__)


class LoggingMixin(object):
    # log only when one of the following methods is being performed
    allowed_logging_methods = ('post', 'put', 'patch', 'delete',
                               'get', )

    def finalize_response(self, request, response, *args, **kwargs):
        # regular finalize response
        response = super().finalize_response(request, response, *args, **kwargs)
        # do not log, if method not found
        if request.method.lower() not in self.allowed_logging_methods:
            return response
        status_code = response.status_code

        # time_delta = now() - self.request.info['date']
        # response_time_ms = time_delta.total_seconds() * 1000

        # log_kwargs = {
        #     'view': self.get_view_name(),
        #     'action': self.action,
        #     'method': request.method.lower(),
        #     'status_code': status_code,
        #     'response_time_ms': round(response_time_ms, 2),
        #     'request_path': request.path,
        # }

        req_time = self.request.info['req_time']
        if status.is_server_error(status_code):
            log_result = 'Fail: status_{0}'.format(status_code)
            log_message = res_log_message(request, log_result, req_time)
            logger.error(log_message)
        elif status.is_client_error(status_code):
            log_result = 'Fail: status_{0}'.format(status_code)
            log_message = res_log_message(request, log_result, req_time)
            logger.warning(log_message)
        elif status_code == 200 or status_code == 201:
            log_result = 'Success: status_{0}'.format(status_code)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)
        else:
            log_result = 'Fail: status_{0}'.format(status_code)
            log_message = res_log_message(request, log_result, req_time)
            logger.info(log_message)

        return response