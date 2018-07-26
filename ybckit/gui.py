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
    import ybc_box as yb
    import easygui as eg

    method_list = [
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
    ]

    logger.debug('wrap methods %s' % method_list)

    for _method in method_list:
        setattr(eg, _method, _wrap(_method, getattr(eg, _method)))

    def _buttonbox(msg='', choices=[], title=''):
        return eg.buttonbox(msg, title, choices)

    def _choicebox(msg='', choices=[], title=''):
        return eg.choicebox(msg, title, choices)

    def _enterbox(msg='', title=''):
        return eg.enterbox(msg, title)

    def _fileopenbox(msg='', title=''):
        return eg.fileopenbox(msg, title)[0]

    def _indexbox(msg='', choices=[], title=''):
        return eg.indexbox(msg, title, choices)

    def _msgbox(msg='', image=None):
        return eg.msgbox(msg, image=image)

    def _multchoicebox(msg='', choices=[], title=''):
        return eg.multchoicebox(msg, title, choices)

    def _multpasswordbox(msg='', title=''):
        return eg.multchoicebox(msg, title)

    def _passwordbox(msg='', title=''):
        return eg.passwordbox(msg, title)

    def _textbox(msg='', text='', title='', codebox=False):
        return eg.textbox(msg, title, text, codebox)

    def _ynbox(msg='', choices=[], title=''):
        return eg.ynbox(msg, title, choices)

    def _codebox(msg='', title='', text=''):
        return eg.codebox(msg, title, text)

    setattr(yb, 'ynbox', _ynbox)
    setattr(yb, 'textbox', _textbox)
    setattr(yb, 'passwordbox', _passwordbox)
    setattr(yb, 'multpasswordbox', _multpasswordbox)
    setattr(yb, 'multchoicebox', _multchoicebox)
    setattr(yb, 'msgbox', _msgbox)
    setattr(yb, 'indexbox', _indexbox)
    setattr(yb, 'fileopenbox', _fileopenbox)
    setattr(yb, 'enterbox', _enterbox)
    setattr(yb, 'choicebox', _choicebox)
    setattr(yb, 'buttonbox', _buttonbox)
    setattr(yb, 'codebox', _codebox)
