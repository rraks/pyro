""" pyro.py

Main class

"""
from pyro import logger
from pynvim import attach
from pyro import nvimutils
from pyro import nvimui
import threading 

"""
autocmd BufWritePost <buffer=<bufid> :call rpcnotify(<channel>, <eventname>)>
"""

class Pyro():
    def __init__(self):
        self.vim = attach('socket', path='/tmp/nvim')
        self.cur_buf = self.vim.current.buffer
        self.macro_dir = self.vim.vars["pyro_macro_path"]
        self.vim.chdir(self.macro_dir)
        # self.vim.command("autocmd BufWritePost <buffer=%d> call rpcnotify(%d, 'saved')"\
        #                  % (self.cur_buf.number, self.vim.channel_id))

    def get_lines(self, pattern):
        format_spacers = 3
        idxs, lines = nvimutils.search_pattern(self.vim, self.cur_buf, pattern)
        """ Also append 3 empty lines for formatting purposes """
        formatted_lines = []
        for l in lines:
            formatted_lines.append(l)
            for spc in range(format_spacers):
                formatted_lines.append([""])
        return lines, formatted_lines


    def save_macro(self):
        """ TODO: Save macro name here """
        with open("/tmp/tmp.py", "w") as f:
            # f.write(code)
            pass

    def save_search(self, lines):
        with open("/tmp/lines.txt", "w") as f:
            f.write(lines)

    def start(self, pattern):
        """ Flow
            - [x] Create tmp buffer
            - [ ] Save with some name in pyro_macro_dir
            - [ ] Make a tabview from the buffer
            - [ ] Split tab window into scratch for RO output and WR input (code)
            - [ ] Command to execute code
            - [ ] Set filetype to python
        """
        self.lines, fmtd_lines = self.get_lines(pattern)
        self.codehdl = nvimutils.create_buf(self.vim, 0)
        self.scratchhdl = nvimutils.create_buf(self.vim, 1)
        self.put_scratch(fmtd_lines)
        nvimui.new_tab_buffer(self.vim, self.codehdl)
        nvimui.vsplit_win(self.vim, self.scratchhdl)
        self.vim.command("autocmd BufWritePost <buffer=%d> :echo 'It worked'" % (self.codehdl.number))
        while(True):
            event = self.vim.next_message()
            print("Block released")
            self.vim.command("echo 'Triggered'")


    def get_code(self):
        return self.codehdl[:]

    def get_list(self):
        return self.scratchhdl[:]

    def put_code(self, code):
        nvimutils.append_line(self.codehdl, code)

    def put_scratch(self, scratch):
        print(scratch)
        nvimutils.append_line(self.scratchhdl, scratch)

    def execute_macro(self):
        for l in self.get_code():
            eval(l)



