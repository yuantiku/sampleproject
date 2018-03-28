import logging
import os

logger = logging.getLogger(__name__)


def _read_config(key):
    return os.environ[key] if key in os.environ else None


class YbcConfig:
    is_under_ybc_env = False

    request_file = None

    response_file_prefix = None

    response_check_interval = 100.0

    oss_endpoint = None

    oss_bucket = None

    oss_access_key_id = None

    oss_access_key_secret = None

    oss_sts_token = None

    oss_stdout = None

    def __init__(self):
        self.reload()

    def reload(self):
        if 'YBC_ENV' in os.environ:
            self.is_under_ybc_env = True

        self.request_file = _read_config('YBC_REQUEST_FILE')
        self.response_file_prefix = _read_config('YBC_RESPONSE_FILE_PREFIX')
        self.oss_bucket = _read_config('YBC_OSS_BUCKET')
        self.oss_access_key_id = _read_config('YBC_OSS_ACCESS_KEY_ID')
        self.oss_access_key_secret = _read_config('YBC_OSS_ACCESS_KEY_SECRET')
        self.oss_sts_token = _read_config('YBC_OSS_STS_TOKEN')
        self.oss_stdout = _read_config('YBC_OSS_STDOUT')
        self.oss_endpoint = _read_config('YBC_OSS_ENDPOINT')

        if self.oss_access_key_id is not None and self.oss_sts_token:
            logger.warning(u'存在 ossAccessKeyId 但是不存在 ossStsToken，请检查是否用了 STS 方式鉴权。直接通过 AK/SK 鉴权有泄漏私钥的风险！')

        if 'YBC_RESPONSE_CHECK_INTERVAL' in os.environ:
            self.response_check_interval = float(os.environ['YBC_RESPONSE_CHECK_INTERVAL'])


YBC_CONFIG = YbcConfig()
