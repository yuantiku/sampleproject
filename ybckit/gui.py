# coding=utf-8
import logging
import time

from . import protocol
from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


def _wrap(method_name, method):
    def wrapped(*args, **kwargs):
        if not YBC_CONFIG.isUnderYbcEnv:
            return method(*args, **kwargs)

        _locals = locals()
        logger.debug("send client request")
        request_id = protocol.send_request("python.easygui." + method_name, _locals['args'], _locals['kwargs'])
        logger.debug("got request_id %d" % request_id)

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(YBC_CONFIG.responseCheckInterval / 1000.0)
                continue

            logger.debug(u"request %d got response %s" % (request_id, raw_response))
            return protocol.parse_response(raw_response)

    return wrapped


def init():
    import easygui as eg
    for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
        logger.debug("wrap method %s" % _method)
        setattr(eg, _method, _wrap(_method, getattr(eg, _method)))
