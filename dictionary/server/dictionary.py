import re
import csv
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
        self._csv__dict_cache = None
        self._items_lists_cache = None

    def GetInfo(self):
        return {'Name': self._name, 'WhiteList': ['all'],
                'Regex': r'[\w]', 'TriggerKey': []}


    def OnBufferEnter(self, version):
        # Check ~/plugin_for_ECY/example1/client/dictionary.py
        # What client send what server get as a single dict variable.
        if self._dict_file_name is not None:
            return None
        self._dict_file_name = version['DictFileName']
        g_logger.debug(self._dict_file_name)
        try:
            f = open(self._dict_file_name, 'r', encoding='utf-8')
            self._csv__dict_cache = csv.DictReader(f)
            self._generate()
            f.close()
            g_logger.debug('updated a file cache.')
        except:
            g_logger.exception('')
        return None

    def _generate(self, only_word=True, frequency=1000):
        # frequency = 1000 means about 40000 word
        self._items_lists_cache = []
        for item in self._csv__dict_cache:
            word = {'abbr': '', 'word': '', 'kind': 'Dict', 'menu': '', 'info': '',
                    'user_data': ''}
            if not int(item['frq']) > frequency:
                continue
            if only_word and item['word'].find(' ') != -1:
                continue
            word['abbr'] = item['word']
            word['word'] = item['word']
            temp = []
            if item['phonetic'] != '':
                temp.append('/' + item['phonetic'] + '/')
            level = ''
            if item['collins']:
                level += '柯林斯星级;'
            if item['oxford']:
                level += '牛津三千'
            if level != '':
                temp.append(level)
            if item['tag'] != '':
                temp.append("分类:" + item['tag'])
            if item['exchange'] != '':
                temp.append("变化:" + item['exchange'])
            temp.append('--------------------')
            temp.extend(item['translation'].split("\\n"))
            word['info'] = temp
            self._items_lists_cache.append(word)
        self._csv__dict_cache = ''

    def DoCompletion(self, version):
        if self._dict_file_name is None:
            g_logger.debug('have no init.')
            return None
        # must contain 'VersionID' and 'Server_name'
        return_ = {'ID': version['VersionID'], 'Lists': self._items_lists_cache}
        return return_
