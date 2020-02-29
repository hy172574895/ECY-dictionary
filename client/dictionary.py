import lib.scope as scope_
import lib.vim_or_neovim_support as vim_lib

# the class must be named as 'Operate'
class Operate(scope_.Event):
    def __init__(self, source_name):
        scope_.Event.__init__(self, source_name)
        self._dictionary_file_name = None

    def _get_dictionary_file_name(self):
        if self._dictionary_file_name is None:
            self._dictionary_file_name = vim_lib.GetVariableValue('g:my_plugin_dictionary_file_path')
        return self._dictionary_file_name

    def OnBufferEnter(self):
        msg = {}
        msg['DictFileName'] = self._get_dictionary_file_name()
        return self._pack(msg, 'OnBufferEnter')
