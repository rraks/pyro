""" nvimutils.py
Neovim abstraction functions
"""


def append_line(buf, linearr):
    """Append lines
    Args: 
        buf (obj): Nvim buffer
        linearr (Array[string]): Line contents
    Returns:
        suc (bool): True if success
    """
    for l in linearr:
        buf.append(l)
    return True


def clear_line(buf, linenum):
    """Clear a line
    Args: 
        buf (obj): Nvim buffer
        linenum (int): Line Number
    Returns:
        suc (bool): True if success
    """
    buf[linenum] = []
    return True


def clear_buf(buf):
    """ (!!) Clear the entire buffer
    Args: 
        buf (obj): Nvim buffer
    """
    buf[:] = []


def search_pattern(vim, buf, pattern):
    """ Search for a pattern
    Args: 
        vim (obj): nvim socket handler
    Returns: 
        lines (list): List of position indices and string row
    Note:
        Indexing is 0 based end exclusive for the nvim_ call, whereas 1 indexed
        for the eval call
    """
    lines = []
    idxs = []
    while True:
        l = vim.eval("searchpos('%s', 'w')" % pattern)
        if l in idxs:
            break
        """ Nvim api lines are 0 indexed """
        lines.append(vim.request("nvim_buf_get_lines", buf, l[0]-1, l[0], 0))
        idxs.append(l)
    return idxs, lines


def highlight_line(vim, namespace, line_num, hl_group="PMenu"):
    """ highlight line
    Args: 
        vim (obj): nvim socket handler
        namespace (str): Namespace to which this highlight belongs
        line_num (int): line_num
        hl_group (str): Highlight group, see :highlight for groups
    Returns: 
        hl_hdl (obj): Handler for this line

    TODO: Make highlight generic
    TODO: Make buf a parameter, currently 0
    """
    """ Creates or gets existing namespace """
    nid = vim.request("nvim_create_namespace", namespace)
    return vim.request("nvim_buf_add_highlight", 0, nid, "PMenu",
                       line_num, 0, -1)


def clear_highlight(vim, namespace):
    """ clear highlight
    Args: 
        vim (obj): nvim socket handler
        namespace (str): Namespace to which this highlight belongs
    """ 

    """ Creates or gets existing namespace """
    nid = vim.request("nvim_create_namespace", namespace)
    return vim.request("nvim_buf_clear_namespace", 0, nid, 0, -1)



def add_lines(vim, buf, start, end, lines):
    """ Add lines
    Args: 
        vim (obj): nvim socket handler
        start (int): start (0 indexed)
        end (int): end (0 indexed exclusive)
        lines (List): Lines array
    """ 
    for l in lines:
        """ Nvim lines are 0 indexed """
        vim.request("nvim_buf_set_lines", buf, start-1, end, 0, [l])


def create_buf(vim, scratch=0):
    """ Create buf
    Args: 
        vim (obj): nvim socket handler
        scratch (int): 0 if non-scratch
    """ 
    buf = vim.request("nvim_create_buf", 1, scratch)
    return buf
