# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
from logging import DEBUG, INFO, basicConfig


def init():
    if 'YBC_DEBUG' in os.environ:
        logging_level = DEBUG
    else:
        logging_level = INFO

    basicConfig(level=logging_level)
