import ECY.utils.scope as scope_
import ECY.utils.vim_or_neovim_support as vim_lib

# the class must be named as 'Operate'
class Operate(scope_.Event):
    def __init__(self, source_name):
        scope_.Event.__init__(self, source_name)
        self._dictionary_file_name = None

    def _get_dictionary_file_name(self):
        if self._dictionary_file_name is None:
            self._dictionary_file_name = vim_lib.GetVariableValue('g:dictionary_csv_file_path')
        return self._dictionary_file_name

    def OnBufferEnter(self):
        msg = {}
        msg['DictFileName'] = self._get_dictionary_file_name()
        msg['Frequency'] = vim_lib.GetVariableValue('g:dictionary_frequency_of_filtering_words')
        msg['UseChinese'] = vim_lib.GetVariableValue('g:dictionary_show_chinese_in_preview_windows')
        msg['AdditionalPath'] = vim_lib.GetVariableValue('g:dictionary_additional_dict_path')
        return self._pack(msg, 'OnBufferEnter')
