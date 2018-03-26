# coding=utf-8
import os

import easygui as eg
import time

from . import protocol


def _is_under_ybc_env():
    """
    判断当前环境是否在猿编程环境下
    :return:
    """
    return 'YBC_ENV' in os.environ and os.environ['YBC_ENV'] is not None


def _wrap(methodName, method):
    if not _is_under_ybc_env():
        return method

    def wrapped(*args, **kwargs):
        _locals = locals()
        request_id = protocol.send_request(methodName, _locals['args'], _locals['kwargs'])

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(0.1)
                continue

            return protocol.parse_response(raw_response)

    return wrapped


for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
    globals()[_method] = _wrap(_method, getattr(eg, _method))

if __name__ == '__main__':
    globals()['buttonbox'](msg='hello world')
