""" pyro.py
Main class
External:
    let g:pyro_macro_path="/some/path/to/macros
"""
import pynvim
from pyro import logger
from pyro import nvimutils
from pyro import nvimui
import threading 
from datetime import datetime
import subprocess
import json


""" Boiler plate code template """
""" TODO: Read from file(slow) or templatify"""
macro_template = ['""" code_template.py', 'Boiler plate template for a python macro',
                  '"""', '', 'import sys', 'import json', '',
                  '# This is the input list[list[line]] to the macro', 'lst = json.loads(sys.argv[1])',
                  '', '# new_lst is the output list', 'new_lst = []',
                  '', '# Iterate through input list', 
                  'for line in lst:', '    modified_line = line[0]', '',
                  '    # You can make modifications to modified_line here',
                  '    # You can append multiple lines to new_list as well',
                  '    # For e.g, new_lst.append([ln1, ln2]) two lines will be appended for one row of input',
                  '',
                  '    new_lst.append([modified_line])',
                  '', '',
                  '# Return Output', 'print(json.dumps(new_lst))']


class Pyro(object):
    """ Pyro main class
    """
    def __init__(self, vim):
        self.vim = vim
        self.cur_buf = self.vim.current.buffer
        self.macro_dir = self.vim.vars["pyro_macro_path"]
        self.vim.chdir(self.macro_dir)

    def get_lines(self, pattern, mode):
        """ Get lines matching pattern from nvimutils
        Args:
            pattern (string): pattern to be matched
            mode (string): "r", "a", "g"
        """
        """ Render format new lines to be used """
        format_spacers = 3
        if mode == "r" or mode == "a":
            idxs, lines = nvimutils.search_pattern(self.vim, self.cur_buf, pattern)
        if mode == "ga" or mode == "gr":
            idxs, lines = nvimutils.all_lines(self.vim, self.cur_buf)
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
        """ TODO: Save search results here """
        with open("/tmp/lines.txt", "w") as f:
            f.write(lines)


    def on_exec(self):
        """ Macro code execution callback
        """
        """ Output is only set on saving the code buffer """
        try:
            self.output = subprocess.check_output(["python3", 
                                        self.code_fl_name,
                                        json.dumps(self.lines)],
                                        stderr=subprocess.STDOUT,
                                        encoding="utf-8")
            self.output = json.loads(self.output)
        except subprocess.CalledProcessError as e:
            self.vim.command("echo '%s'" % e.output)
            return

        lnum = 0
        self.scratchhdl[:] = []
        for (inp, outp) in zip(self.lines, self.output):
            print(inp, lnum)
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, inp)
            nvimutils.highlight_line(self.vim, self.scratchhdl,
                                     "inlines"+str(lnum), lnum, hl_group="PMenu")
            lnum += 1
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, outp)
            nvimutils.highlight_line(self.vim, self.scratchhdl,
                                     "outlines"+str(lnum), lnum, hl_group="PMenuSel")
            lnum += len(outp)
            nvimutils.add_lines(self.vim, self.scratchhdl, lnum, lnum+1, ["",""])
            lnum += 2 


    def on_save(self):
        """ Output scratch buffer commit callback
        Save the results of the macro back to original buffer
        """
        if self.mode == "r" or self.mode == "gr":
            offset = 0
            for idx, l in enumerate(self.output):
                nvimutils.add_lines(self.vim, self.cur_buf,
                                    self.idxs[idx][0]-1+offset, self.idxs[idx][0]+offset, l)
                offset += (len(l) - 1)
        if self.mode == "a" or self.mode == "ga" or self.mode == "g":
            offset = 0
            for idx, l in enumerate(self.output):
                nvimutils.add_lines(self.vim, self.cur_buf,
                                    self.idxs[idx][0]+offset, self.idxs[idx][0]+offset, l)
                offset += len(l)

    def on_buffer_change(self):
        new_buf_id, new_buf_name = nvimutils.cur_buf_detail(self.vim)
        self.vim.command("autocmd BufWritePost <buffer=%s> call rpcnotify(%d, 'pyro_exec_trigger')"\
                         % (new_buf_id, self.vim.channel_id))
        self.code_fl_name = new_buf_name

    def start_pyro(self, pattern, mode="r"):
        """ Pyro initialization function
        Creates split windowed view and registers necessary autocmds and rpc callbacks
        Args:
            pattern (str): Pattern
            opts (str): enum("r", "a", "g")
                        r - "replace" - replaces the line in the original file
                        a - "append" - appends below the line in the original file
                        g - "global" - no patterns required. All lines will be the input
        Todo: chord with vim's built in global command instead
        """
        self.mode = mode
        self.idxs, self.lines, fmtd_lines = self.get_lines(pattern, self.mode)


        datetimenow = datetime.now().strftime("%H_%M_%S") 
        self.code_fl_name = "tmp_" + datetimenow + ".py"
        self.scratch_fl_name = "/tmp/pyro_" + datetimenow + ".txt"
        self.codehdl = nvimutils.create_buf(self.vim, 0)
        self.put_code(macro_template)
        self.vim.request("nvim_buf_set_name", self.codehdl.number, self.code_fl_name)
        self.scratchhdl = nvimutils.create_buf(self.vim, 0)
        self.vim.request("nvim_buf_set_name", self.scratchhdl.number, self.scratch_fl_name)
        self.scratchhdl[:] = []
        self.put_scratch(fmtd_lines)
        nvimui.new_tab_buffer(self.vim, self.codehdl)
        """ On exec """
        self.vim.command("autocmd BufWritePost <buffer=%d> call rpcnotify(%d, 'pyro_exec_trigger')"\
                         % (self.codehdl.number, self.vim.channel_id))
        """ On save """
        self.vim.command("autocmd BufWritePre <buffer=%d> call rpcnotify(%d, 'pyro_save_trigger')"\
                         % (self.scratchhdl.number, self.vim.channel_id))

        self.vim.command("%dbufdo! set filetype=python" % self.codehdl.number)
        nvimui.vsplit_win(self.vim, self.scratchhdl)
        self.vim.command('call feedkeys("\<c-w>w", "n")')
        """ Buffer changed """
        code_winnr = 2 # Make this part of config
        tab_nr = nvimutils.get_tabnum(self.vim)
        self.vim.command("autocmd BufWinEnter * if winnr()==%d && tabpagenr()==%s && bufname()[-2:]=='py'\
                          |  call rpcnotify(%d, 'pyro_buffer_changed')"\
                         % (code_winnr, tab_nr, self.vim.channel_id))


    def put_code(self, code):
        """ Put macro code string into code buffer """
        nvimutils.append_line(self.codehdl, code)

    def put_scratch(self, scratch):
        """ Put scratch string into scratch buffer """
        nvimutils.append_line(self.scratchhdl, scratch)


    """ Auxiliary functions """

    def get_code(self):
        return self.codehdl[:]

    def get_list(self):
        return self.scratchhdl[:]

    def execute_macro(self):
        """ Unused """
        for l in self.get_code():
            eval(l)



