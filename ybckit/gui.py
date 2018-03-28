# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import time

from . import protocol
from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


def _wrap(method_name, method):
    def wrapped(*args, **kwargs):
        if not YBC_CONFIG.is_under_ybc_env:
            return method(*args, **kwargs)

        _locals = locals()
        logger.debug('send client request')
        request_id = protocol.send_request('python.easygui.' + method_name, _locals['args'], _locals['kwargs'])
        logger.debug('got request_id %d' % request_id)

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
                continue

            logger.debug('request %d got response %s' % (request_id, raw_response))
            return protocol.parse_response(raw_response)

    return wrapped


def init():
    import easygui as eg
    for _method in [
        'buttonbox',
        'enterbox',
        'passwordbox',
        'msgbox',
        'diropenbox',
        'fileopenbox',
        'ynbox',
        'ccbox',
        'boolbox',
        'multenterbox',
        'choicebox',
        'textbox',
        'multpasswordbox',
        'integerbox',
        'multchoicebox',
        'codebox'
    ]:
        logger.debug('wrap method %s' % _method)
        setattr(eg, _method, _wrap(_method, getattr(eg, _method)))
