# coding=utf-8
import os

import easygui as eg

from . import protocol


def _is_under_ybc_env():
    """
    判断当前环境是否在猿编程环境下
    :return:
    """
    return 'YBC_ENV' in os.environ and os.environ['YBC_ENV'] is not None


def _wrap(method):
    if not _is_under_ybc_env():
        return method

    def wrapped():
        request_id = protocol.send_request(method, locals())

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is not False:
                continue

            return protocol.parse_response(raw_response)

    return wrapped


for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
    globals()[_method] = _wrap(getattr(eg, _method))

if __name__ == '__main__':
    globals()['buttonbox'](msg='hello world')
