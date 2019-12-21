""" pyro.py

Main class

"""
import pynvim
from pyro import logger
from pyro import nvimutils
from pyro import nvimui
import threading 
from datetime import datetime
import subprocess
import json


macro_template = ['""" code_template.py', 'Boiler plate template for a python macro',
                  '"""', '', '""" Do not edit """', 'import sys', 'import json', '',
                  '""" This is the input list[list[line]] to the macro """', 'lst = json.loads(sys.argv[1])',
                  '', '""" Insert Macro here, output should be an stdout of list of list """', '','', '""" End Macro """']

class Pyro(object):
    def __init__(self, vim):
        # self.vim = attach('socket', path='/tmp/nvim')
        self.vim = vim
        self.cur_buf = self.vim.current.buffer
        self.macro_dir = self.vim.vars["pyro_macro_path"]
        self.vim.chdir(self.macro_dir)

    def get_lines(self, pattern):
        format_spacers = 3
        idxs, lines = nvimutils.search_pattern(self.vim, self.cur_buf, pattern)
        """ Also append 3 empty lines for formatting purposes """
        formatted_lines = []
        for l in lines:
            formatted_lines.append(l)
            for spc in range(format_spacers):
                formatted_lines.append([""])
        return idxs, lines, formatted_lines


    def save_macro(self):
        """ TODO: Save macro name here """
        with open("/tmp/tmp.py", "w") as f:
            # f.write(code)
            pass

    def save_search(self, lines):
        with open("/tmp/lines.txt", "w") as f:
            f.write(lines)

    def pyro_start(self, args, range):
        self.vim.command("echo hha")
        pass


    def on_save(self):
        output = subprocess.check_output(["python3",
                                    self.codehdl.name,
                                    json.dumps(self.lines)],
                                    encoding="utf-8")
        output = json.loads(output)

        lnum = 0
        self.scratchhdl[:] = []
        for (inp, outp) in zip(self.lines, output):
            print(inp, lnum)
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, inp)
            nvimutils.highlight_line(self.vim, self.scratchhdl,
                                     "inlines"+str(lnum), lnum, hl_group="PMenu")
            lnum += 1
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, outp)
            nvimutils.highlight_line(self.vim, self.scratchhdl,
                                     "outlines"+str(lnum), lnum, hl_group="PMenuSel")
            lnum += 1
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, " ")
            lnum += 1
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, " ")
            lnum += 1

    def start_pyro(self, pattern):
        """ TODO: Change filetype """
        idxs, self.lines, fmtd_lines = self.get_lines(pattern)
        codeflname = "tmp_" + datetime.now().strftime("%H_%M_%S") + ".py"
        self.codehdl = nvimutils.create_buf(self.vim, 0)
        self.put_code(macro_template)
        self.vim.request("nvim_buf_set_name", self.codehdl.number, codeflname)
        self.scratchhdl = nvimutils.create_buf(self.vim, 1)
        self.put_scratch(fmtd_lines)
        nvimui.new_tab_buffer(self.vim, self.codehdl)
        self.vim.command("autocmd BufWritePost <buffer=%d> call rpcnotify(%d, 'pyro_save_trigger')"\
                         % (self.codehdl.number, self.vim.channel_id))
        self.vim.command("%dbufdo! set filetype=python" % self.codehdl.number)
        nvimui.vsplit_win(self.vim, self.scratchhdl)
        #self.vim.run_loop(self.event_cb, None, None)




    def get_code(self):
        return self.codehdl[:]

    def get_list(self):
        return self.scratchhdl[:]

    def put_code(self, code):
        nvimutils.append_line(self.codehdl, code)

    def put_scratch(self, scratch):
        nvimutils.append_line(self.scratchhdl, scratch)

    def execute_macro(self):
        for l in self.get_code():
            eval(l)



