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

    basicConfig(format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
                level=logging_level,
                handlers=[
                    FileHandler("/tmp/ybckit.log"),
                    StreamHandler(sys.stdout)
                ])
