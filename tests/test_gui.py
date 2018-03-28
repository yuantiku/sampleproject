# coding=utf-8
import unittest

import easygui

from ybckit.gui import init as gui_init
from . import ybc_env


class GuiTestCase(unittest.TestCase):

    def setUp(self):
        super(GuiTestCase, self).setUp()
        ybc_env.setup()
        gui_init()

    def tearDown(self):
        super(GuiTestCase, self).tearDown()
        ybc_env.cleanup()

    @unittest.skip('仅限本地运行，需要手动检查 /tmp/request 内容')
    def test_gui(self):
        easygui.buttonbox(msg="hello world!")

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
