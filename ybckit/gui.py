#!/usr/bin/env python
# -*- coding: utf-8 -*-

import easygui as eg


def _wrap(method):
    return method


for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
    globals()[_method] = _wrap(getattr(eg, _method))

if __name__ == '__main__':
    globals()['buttonbox'](msg='hello world')
