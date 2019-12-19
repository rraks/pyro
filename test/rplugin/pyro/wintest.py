"""wintest.py
Window tests
This file must be executed from the root of the project
"""
import sys
import unittest
sys.path.insert(1, 'rplugin/python3')
# from pyro import Pyro
# from pynvim import nvimutils
from pyro import pyro
from pyro import nvimutils
from pyro import nvimui

class SimpleTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        ex_text_fl = 'test/rplugin/pyro/example.txt'
        self.ex_text_buf = []
        with open(ex_text_fl, 'r') as f:
            self.ex_text_buf = f.read().splitlines()

        self.p = pyro.Pyro()

        """ Clear buffer """
        nvimutils.clear_buf(self.p.cur_buf)

    def append_few_lines(self, buf):
        for l in self.ex_text_buf:
            nvimutils.append_line(buf, l)

    def cur_buf_in_win(self):
        self.append_few_lines()
        nvimui.set_buf_in_win(self.p.vim, self.p.cur_buf)
        nvimui.set_buf_in_win(self.p.vim, 1)


    def open_window(self):
        self.append_few_lines(self.p.cur_buf)
        nvimui.open_win(self.p.vim, self.p.cur_buf)

    def split_window(self):
        tabid = nvimui.new_tab(self.p.vim)
        print(tabid)


if __name__ == '__main__':
    unittest.main()




