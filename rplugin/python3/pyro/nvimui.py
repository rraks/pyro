""" nvimui.py
Neovim UI functions
"""
term_config = {}


def buf_in_win(vim, buf):
    vim.request("nvim_win_get_buf", 0)


def set_buf_in_win(vim, buf):
    vim.request("nvim_win_set_buf", 0, buf)

def open_win(vim, buf):
    vim.request("nvim_open_win", buf, 1, {"relative": "win", "win": 1, "anchor": "NW", "width": 100, "height": 5, "row": 5, "col": 5})


def new_tab_buffer(vim, bufhdl=None):
    if bufhdl != None:
        vim.command("tab sb %d" % bufhdl.number)
    else:
        vim.command("tabnew")
    return

def vsplit_win(vim, bufhdl=None):
    if bufhdl != None:
        vim.command("vertical sb %d" % bufhdl.number)
    else:
        vim.command("vsplit")
    return

