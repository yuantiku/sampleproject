# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import io
import logging
import sys

import oss2
from oss2.exceptions import NotFound

from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


class OssFile(io.TextIOWrapper):
    bucket = None

    def __init__(self, key, append=False):
        super(OssFile, self).__init__(io.BytesIO())

        self._bucket = OssFile.bucket
        self._key = key
        self._append = append
        self._append_position = None

    def fileno(self):
        raise OSError('file at oss server')

    def isatty(self):
        return False

    def read(self, n=None):
        return self._bucket.get_object(self._key, (0, n)).read()

    def readable(self):
        return self._bucket.object_exists(self._key)

    def readline(self, limit=-1):
        raise NotImplementedError('readline is not implemented by oss file')

    def seek(self, offset, whence=io.SEEK_SET):
        raise OSError('random access is not implemented by oss file')

    def seekable(self):
        return False

    def tell(self):
        raise OSError('random access is not implemented by oss file')

    def truncate(self, size=None):
        raise OSError('random access is not implemented by oss file')

    def writable(self):
        return True

    def remove(self):
        self._bucket.delete_object(self._key)

    def write(self, s):
        logger.debug('writing string %s' % s)
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
        logger.warning('存在 ossAccessKeyId 但是不存在 ossStsToken，请检查是否用了 STS 方式鉴权。直接通过 AK/SK 鉴权有泄漏私钥的风险！')
        auth = oss2.Auth(YBC_CONFIG.oss_access_key_id, YBC_CONFIG.oss_access_key_secret)

    OssFile.bucket = oss2.Bucket(auth, YBC_CONFIG.oss_endpoint, YBC_CONFIG.oss_bucket)

    if YBC_CONFIG.oss_stdout is not None:
        oss_file = OssFile(key=YBC_CONFIG.oss_stdout, append=True)
        oss_file.remove()
        sys.stdout = oss_file

    if YBC_CONFIG.oss_stderr is not None:
        oss_file = OssFile(key=YBC_CONFIG.oss_stderr, append=True)
        oss_file.remove()
        sys.stderr = oss_file
