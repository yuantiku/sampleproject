# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
from logging import DEBUG, INFO, WARNING, basicConfig, FileHandler, StreamHandler


def init():
    if 'YBC_DEBUG' in os.environ:
        logging_level = DEBUG
    else:
        logging_level = INFO

    if 'YBC_ENV' in os.environ:
        logging_level = WARNING

    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(logging_level)

    file_handler = FileHandler("/tmp/ybckit.log")
    file_handler.setLevel(DEBUG)

    basicConfig(format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                handlers=[
                    file_handler,
                    console_handler,
                ])
