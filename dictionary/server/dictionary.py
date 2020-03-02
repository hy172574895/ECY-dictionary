import re
import logging
global g_logger
g_logger = logging.getLogger('ECY_server')

import utils.interface as scope_

# the class must be named as 'Operate'
class Operate(scope_.Source_interface):
    def __init__(self):
        # must same as the same defined in Client side.
        self._name = 'dictionary'
        self._dict_file_name = None
        self._dict_cache = None
        self._dict_file_cache = ''

    def GetInfo(self):
        return {'Name': self._name, 'WhiteList': ['all'],
                'Regex': r'[\w]', 'TriggerKey': []}


    def OnBufferEnter(self, version):
        # Check ~/plugin_for_ECY/example1/client/dictionary.py
        # What client send what server get as a single dict variable.
        dict_file_name_temp = version['DictFileName']
        g_logger.debug(dict_file_name_temp)
        if not dict_file_name_temp == self._dict_file_name:
            # read that file into cache
            try:
                temp = open(dict_file_name_temp, 'r')
                self._dict_file_cache = str(temp.read())
                temp.close()
            except:
                g_logger.exception('')
                return None
            self._dict_cache = list(set(re.findall(r'\w+', self._dict_file_cache)))
            g_logger.debug('updated a file cache.')
        self._dict_file_name = dict_file_name_temp
        return None

    def DoCompletion(self, version):
        if self._dict_file_name is None:
            g_logger.debug('have no init.')
            # Means we do nothing.
            return None
        # must contain 'VersionID' and 'Server_name'
        return_ = {'ID': version['VersionID'], 'Server_name': self._name}
        results_list = []
        for item in self._dict_cache:
            results_format = {'abbr': '', 'word': '', 'kind': '',
                    'menu': '', 'info': [],'user_data':''}
            results_format['abbr'] = item
            results_format['word'] = item
            results_format['kind'] = 'Dict'
            results_list.append(results_format)
        return_['Lists'] = results_list
        return return_
