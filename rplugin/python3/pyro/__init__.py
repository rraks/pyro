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
        self.p.start_pyro(args[0].strip("/"))
        pass

    @pynvim.rpc_export('pyro_save_trigger')  # type: ignore
    def pyro_save_trigger(self):
        self.p.on_save()
        pass

