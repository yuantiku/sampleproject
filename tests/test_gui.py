import unittest

from ybckit import gui
from . import ybc_env


class GuiTestCase(unittest.TestCase):

    def setUp(self):
        super(GuiTestCase, self).setUp()
        ybc_env.setup()

    def tearDown(self):
        super(GuiTestCase, self).tearDown()
        ybc_env.cleanup()

    @unittest.skip
    def test_gui(self):
        gui.buttonbox(msg="hello world!")

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
