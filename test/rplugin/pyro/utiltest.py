"""utiltest.py
Utility tests
This file must be executed from the root of the project
"""
import sys
import unittest
sys.path.insert(1, 'rplugin/python3')
# from pyro import Pyro
# from pynvim import nvimutils
from pyro import pyro
from pyro import nvimutils
from pynvim import attach

class SimpleTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        ex_text_fl = 'test/rplugin/pyro/example.txt'
        self.ex_text_buf = []
        with open(ex_text_fl, 'r') as f:
            self.ex_text_buf = f.read().splitlines()

        vim = attach('socket', path='/tmp/nvim')
        self.p = pyro.Pyro(vim)

        """ Clear buffer """
        nvimutils.clear_buf(self.p.cur_buf)

    def append_few_lines(self, bufhdl):
        nvimutils.append_line(bufhdl, self.ex_text_buf)


    def search_pattern(self):
        self.append_few_lines(self.p.cur_buf)
        idxs, lines = nvimutils.search_pattern(self.p.vim, self.p.cur_buf, "random")
        print(idxs)
        print(lines)

    def search_highlight_pattern(self):
        self.search_pattern()
        hdl = nvimutils.highlight_line(self.p.vim, self.p.cur_buf, "test", 3)

    def clear_highlight_pattern(self):
        self.search_pattern()
        hdl = nvimutils.clear_highlight(self.p.vim, self.p.cur_buf, "test")

    def add_lines(self):
        self.append_few_lines(self.p.cur_buf)
        nvimutils.add_lines(self.p.vim, 1, 1, ["some exaple text is now replaced"])

    def create_new_buf(self):
        self.append_few_lines(self.p.cur_buf)
        bufhdl = nvimutils.create_buf(self.p.vim)
        self.append_few_lines(bufhdl)
        print(bufhdl)


    def pyro_get_lines(self):
        self.append_few_lines(self.p.cur_buf)
        pattern = "random"
        lines = self.p.get_lines(pattern)
        print(lines)

if __name__ == '__main__':
    unittest.main()




