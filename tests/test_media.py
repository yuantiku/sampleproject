# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import sys
import unittest

from ybckit.media import init as media_init
from . import ybc_env

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class MplTestCase(unittest.TestCase):

    def setUp(self):
        super(MplTestCase, self).setUp()
        ybc_env.setup()
        media_init()

    def tearDown(self):
        super(MplTestCase, self).tearDown()
        ybc_env.cleanup()

    @unittest.skip('仅限本地运行，需要手动检查 /tmp/request 内容')
    def test_record(self):
        media.record('foo', seconds=10, chunk=2048)


if __name__ == '__main__':
    unittest.main()
