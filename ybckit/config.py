# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os

logger = logging.getLogger(__name__)


def _read_config(key):
    return os.environ[key] if key in os.environ else None


class YbcConfig:

    def __init__(self):
        self.is_under_ybc_env = False

        self.request_file = None
        self.response_file_prefix = None

        self.stdout_file = None
        self.stderr_file = None

        self.response_check_interval = 100.0

        self.reload()

    def reload(self):
        if 'YBC_ENV' in os.environ:
            self.is_under_ybc_env = True

        self.request_file = _read_config('YBC_REQUEST_FILE')
        self.response_file_prefix = _read_config('YBC_RESPONSE_FILE_PREFIX')
        self.stdout_file = _read_config('YBC_STDOUT_FILE')
        self.stderr_file = _read_config('YBC_STDERR_FILE')

        if 'YBC_RESPONSE_CHECK_INTERVAL' in os.environ:
            self.response_check_interval = float(os.environ['YBC_RESPONSE_CHECK_INTERVAL'])


YBC_CONFIG = YbcConfig()
