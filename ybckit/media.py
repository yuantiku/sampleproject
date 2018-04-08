import logging
import time

from . import protocol
from .config import YBC_CONFIG
from .oss import OssFile

logger = logging.getLogger(__name__)


def record():
    request_id = protocol.send_request("python.ybckit.record", args=(), kwargs={})

    while True:
        raw_response = protocol.get_raw_response(request_id)
        if raw_response is False:
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        logger.debug('request %d done' % request_id)
        file_key = protocol.parse_response(raw_response)
        oss_file = OssFile(file_key)
        return oss_file.read()


def snap():
    request_id = protocol.send_request("python.ybckit.snap", args=(), kwargs={})

    while True:
        raw_response = protocol.get_raw_response(request_id)
        if raw_response is False:
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        logger.debug('request %d done' % request_id)
        file_key = protocol.parse_response(raw_response)
        oss_file = OssFile(file_key)
        return oss_file.read()
