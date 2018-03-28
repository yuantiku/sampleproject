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
        self.oss_request_file = None
        self.oss_response_file_prefix = None
        self.oss_stdout = None
        self.oss_stderr = None
        self.oss_bucket = None
        self.oss_access_key_id = None
        self.oss_access_key_secret = None
        self.oss_sts_token = None
        self.oss_stdout = None
        self.oss_endpoint = None
        self.response_check_interval = 100.0

        self.request_file = None
        self.response_file_prefix = None

        self.reload()

    def reload(self):
        if 'YBC_ENV' in os.environ:
            self.is_under_ybc_env = True

        self.request_file = _read_config('YBC_REQUEST_FILE')
        self.response_file_prefix = _read_config('YBC_RESPONSE_FILE_PREFIX')

        self.oss_request_file = _read_config('YBC_OSS_REQUEST_FILE')
        self.oss_response_file_prefix = _read_config('YBC_OSS_RESPONSE_FILE_PREFIX')
        self.oss_stdout = _read_config('YBC_OSS_STDOUT')
        self.oss_stderr = _read_config('YBC_OSS_STDERR')
        self.oss_bucket = _read_config('YBC_OSS_BUCKET')
        self.oss_access_key_id = _read_config('YBC_OSS_ACCESS_KEY_ID')
        self.oss_access_key_secret = _read_config('YBC_OSS_ACCESS_KEY_SECRET')
        self.oss_sts_token = _read_config('YBC_OSS_STS_TOKEN')
        self.oss_stdout = _read_config('YBC_OSS_STDOUT')
        self.oss_endpoint = _read_config('YBC_OSS_ENDPOINT')

        if 'YBC_RESPONSE_CHECK_INTERVAL' in os.environ:
            self.response_check_interval = float(os.environ['YBC_RESPONSE_CHECK_INTERVAL'])


YBC_CONFIG = YbcConfig()
