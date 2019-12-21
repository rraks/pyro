"""pyrotest.py
Pyro function tests
This file must be executed from the root of the project
Note: Run tmp session ./tmp_session.sh and then run these


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
import time

class SimpleTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        ex_text_fl = 'test/rplugin/pyro/example.txt'
        self.ex_text_buf = []
        with open(ex_text_fl, 'r') as f:
            self.ex_text_buf = f.read().splitlines()

        vim = attach('socket', path='/tmp/nvim')
        self.p = pyro.Pyro(vim)

    def pyro_simple(self):
        self.p.vim.command("Pyro/random")
        time.sleep(0.1)
        self.p.vim.command('call feedkeys("\<c-w>w", "n")')
        time.sleep(0.1)
        self.p.vim.command("w")
        time.sleep(0.1)
        self.p.vim.command("wa")


if __name__ == '__main__':
    unittest.main()




