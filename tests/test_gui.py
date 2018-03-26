import unittest

import easygui as egui
from ybckit import gui


class GuiTestCase(unittest.TestCase):
    def test_gui_method(self):
        for _method in ['buttonbox', 'enterbox', 'passwordbox', 'msgbox', 'diropenbox', 'fileopenbox']:
            self.assertEqual(getattr(gui, _method), getattr(egui, _method))


if __name__ == '__main__':
    unittest.main()
