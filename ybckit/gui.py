# coding=utf-8
import time

from . import protocol


def _wrap(method_name, method):
    def wrapped(*args, **kwargs):
        if not protocol.is_under_ybc_env():
            return method(*args, **kwargs)

        _locals = locals()
        request_id = protocol.send_request("python.easygui." + method_name, _locals['args'], _locals['kwargs'])

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(0.1)
                continue

            return protocol.parse_response(raw_response)

    return wrapped


def init():
    if not protocol.is_under_ybc_env():
        pass

    import easygui as eg
    for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
        setattr(eg, _method, _wrap(_method, getattr(eg, _method)))
