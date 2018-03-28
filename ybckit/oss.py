import io
import logging
import sys

import oss2
from oss2.exceptions import NotFound

from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


class OssFile(io.TextIOWrapper):
    _bucket = None
    _key = None
    _append = None
    _append_position = None

    def __init__(self, bucket, key, append=False, encoding=None, errors=None, newline=None,
                 line_buffering=False):
        super().__init__(io.StringIO(), encoding, errors, newline, line_buffering)

        self._bucket = bucket
        self._key = key
        self._append = append

    def close(self):
        super().close()

    def detach(self):
        super().detach()

    def fileno(self):
        raise OSError("file at oss server")

    def flush(self):
        pass

    def isatty(self):
        return False

    def read(self, n=None):
        return self._bucket.get_object(self._key, (0, n)).read()

    def readable(self):
        return self._bucket.object_exists(self._key)

    def readline(self, limit=-1):
        return super().readline(limit)

    def seek(self, offset, whence=io.SEEK_SET):
        raise OSError("random access is not implemented by oss file")

    def seekable(self):
        return False

    def tell(self):
        raise OSError("random access is not implemented by oss file")

    def truncate(self, size=None):
        raise OSError("random access is not implemented by oss file")

    def writable(self):
        return True

    def write(self, s):
        logger.debug("writing string %s" % s)
        if self._append:
            if self._append_position is None:
                try:
                    info = self._bucket.head_object(self._key)
                    self._append_position = info.content_length if info.content_length is not None else 0
                except NotFound:
                    self._append_position = 0

            self._append_position = self._bucket.append_object(self._key, self._append_position, s).next_position
        else:
            self._bucket.put_object(self._key, s)

        return len(s)


def init():
    if YBC_CONFIG.oss_sts_token is not None:
        auth = oss2.StsAuth(YBC_CONFIG.oss_access_key_id, YBC_CONFIG.oss_access_key_secret,
                            YBC_CONFIG.oss_access_key_secret)
    else:
        auth = oss2.Auth(YBC_CONFIG.oss_access_key_id, YBC_CONFIG.oss_access_key_secret)

    bucket = oss2.Bucket(auth, YBC_CONFIG.oss_endpoint, YBC_CONFIG.oss_bucket)

    if YBC_CONFIG.oss_stdout is not None:
        sys.stdout = OssFile(bucket=bucket, key=YBC_CONFIG.oss_stdout, append=True)

    if YBC_CONFIG.oss_stderr is not None:
        sys.stderr = OssFile(bucket=bucket, key=YBC_CONFIG.oss_stderr, append=True)
