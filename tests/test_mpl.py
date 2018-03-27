# coding=utf-8
import logging
import sys
import unittest

import matplotlib.pyplot as plt
import numpy as np

from ybckit.mpl import init as mpl_init
from . import ybc_env

logger = logging.getLogger()
logger.level = logging.DEBUG
logger.addHandler(logging.StreamHandler(sys.stdout))


class MplTestCase(unittest.TestCase):

    def setUp(self):
        super(MplTestCase, self).setUp()
        ybc_env.setup()
        mpl_init()

    def tearDown(self):
        super(MplTestCase, self).tearDown()
        ybc_env.cleanup()

    @unittest.skip(u"仅限本地运行，需要手动检查 /tmp/request 内容")
    def test_show(self):
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        plt.plot(t, s)

        plt.xlabel('time (s)')
        plt.ylabel('voltage (mV)')
        plt.title('About as simple as it gets, folks')
        plt.grid(True)
        plt.show()

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
