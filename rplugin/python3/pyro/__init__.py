""" TODO """
# vim = attach('socket', path='/tmp/nvim')

from pyro import pyro
import pynvim


@pynvim.plugin
class PyroHandlers(object):

    def __init__(self, vim):
        self.vim = vim

    @pynvim.command('Pyro', nargs='*', range='', allow_nested=True, sync=True)
    def pyro_start(self, args, range):
        self.p = pyro.Pyro(self.vim)
        ln = len(args)
        if ln is not 0:
            args = args[0].split("/")
            ln = len(args)
            if ln == 3:
                pattern = args[1]
                modestr = args[2]
            if ln == 2:
                """ mode forced to replace """
                pattern = args[1]
                modestr = "r"
            if ln == 1:
                pattern = ""
                modestr = "gr"
        else:
            pattern = ""
            modestr = "gr"

        self.p.start_pyro(pattern=pattern, mode=modestr)

    @pynvim.rpc_export('pyro_exec_trigger')
    def pyro_exec_trigger(self):
        self.p.on_exec()

    @pynvim.rpc_export('pyro_save_trigger')
    def pyro_save_trigger(self):
        self.p.on_save()

    @pynvim.rpc_export('pyro_buffer_changed')
    def pyro_bufchanged_trigger(self):
        self.p.on_buffer_change()
        pass



