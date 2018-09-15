from config.utils import req_log_message, res_log_message, now_ms
import logging

logger = logging.getLogger(__name__)


def request_info_log_middleware(get_response):
    def middleware(request):
        info = {
            'req_time': now_ms(),
            'user_id':
                request.user.id if request.user.is_authenticated else None
        }
        request.info = info

        log_message = req_log_message(request, info['req_time'])
        logger.info(log_message)

        response = get_response(request)
        return response
    return middleware