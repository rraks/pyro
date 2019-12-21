"""pyrotest.py
Pyro function tests
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

    def importTest(self):
        pass


    def append_few_lines(self, bufhdl):
        nvimutils.append_line(bufhdl, self.ex_text_buf)

    def read_buf_hdl(self):
        self.p.start()
        nvimutils.append_line(self.p.bufhdl, ["Testin hell"])
        code = self.p.get_code()
        # nvimui.open_win(self.p.vim, self.p.bufhdl)
        print(code)
        print(self.p.bufhdl.name)
        print(self.p.bufhdl.number)


    def pyro_start(self):
        self.p.start("random")
        input()
        code = self.p.get_code()
        self.p.execute_macro()
        # self.p.save_macro(code)


if __name__ == '__main__':
    unittest.main()




