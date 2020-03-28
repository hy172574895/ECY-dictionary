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
        self._items_lists_cache = []
        self._use_chinese = True

    def GetInfo(self):
        return {'Name': self._name, 'WhiteList': ['all'],
                'Regex': r'[\w]', 'TriggerKey': []}


    def OnBufferEnter(self, version):
        # Check ~/plugin_for_ECY/example1/client/dictionary.py
        # What client send what server get as a single dict variable.
        if self._dict_file_name is not None:
            return None
        self._dict_file_name = version['DictFileName']
        try:
            self._use_chinese = version['UseChinese']
            self._generate_csv(self._dict_file_name)
            self._generate_txt(version['AdditionalPath'])
            g_logger.debug(len(self._items_lists_cache))
        except:
            g_logger.exception('')
        return None

    def _generate_txt(self, path_lists):
        for item in path_lists:
            try:
                f = open(item, 'r', encoding='utf-8')
                txt = f.read()
                items_list = list(set(re.findall(r'\w+', txt)))
                for word in items_list:
                    temp = {'abbr': '', 'word': '', 'kind': 'Dict', 'menu': '',
                            'info': '','user_data': ''}
                    temp['abbr'] = word
                    temp['word'] = word
                    self._items_lists_cache.append(temp)
                f.close()
                g_logger.debug('loaded a txt:' + item)
            except:
                txt = ''
                g_logger.exception('')

    def _generate_csv(self, csv_path, only_word=True, frequency=0):
        # frequency = 1000 means about 40000 word
        f = open(self._dict_file_name, 'r', encoding='utf-8')
        g_logger.debug('loaded a csv:' + self._dict_file_name)
        self._csv__dict_cache = csv.DictReader(f)
        for item in self._csv__dict_cache:
            if not int(item['frq']) > frequency:
                continue
            if only_word and item['word'].find(' ') != -1:
                continue
            self._items_lists_cache.append(self._format(item))
        self._csv__dict_cache = ''
        f.close()

    def _format(self, word_info):
        word = {'abbr': '', 'word': '', 'kind': 'Dict', 'menu': '', 'info': '',
                'user_data': ''}
        word['abbr'] = word_info['word']
        word['word'] = word_info['word']
        if self._use_chinese:
            word['info'] = self._format_info_chinese(word_info)
        else:
            word['info'] = self._format_info_english(word_info)
        return word

    def _format_info_english(self, word_info):
        temp = []
        if word_info['phonetic'] != '':
            temp.append('/' + word_info['phonetic'] + '/')
        level = ''
        if word_info['collins']:
            level += 'collins;'
        if word_info['oxford']:
            level += 'oxford'
        if level != '':
            temp.append(level)
        if word_info['tag'] != '':
            temp.append("tag:" + word_info['tag'])
        if word_info['exchange'] != '':
            temp.append("exchange:" + word_info['exchange'])
        temp.append('--------------------')
        temp.extend(word_info['definition'].split("\\n"))
        return temp

    def _format_info_chinese(self, word_info):
        """ return lists
        """
        temp = []
        if word_info['phonetic'] != '':
            temp.append('/' + word_info['phonetic'] + '/')
        level = ''
        if word_info['collins']:
            level += '柯林斯星级;'
        if word_info['oxford']:
            level += '牛津三千'
        if level != '':
            temp.append(level)
        if word_info['tag'] != '':
            temp.append("分类:" + word_info['tag'])
        if word_info['exchange'] != '':
            temp.append("变化:" + word_info['exchange'])
        temp.append('--------------------')
        temp.extend(word_info['translation'].split("\\n"))
        return temp

    def DoCompletion(self, version):
        if self._dict_file_name is None:
            g_logger.debug('have no init.')
            return None
        # must contain 'VersionID' and 'Server_name'
        return_ = {'ID': version['VersionID'], 'Lists': self._items_lists_cache}
        return return_

    def OnDocumentHelp(self, version):
        current_word = version['CursorWord']
        g_logger.debug(current_word)
        results = {'ID': version['VersionID']}
        lists = [current_word]
        for item in self._items_lists_cache:
            if item['word'] == current_word:
                lists.extend(item['info'])
                results['Results'] = lists
                return results
        lists.append('没有对应翻译')
        results['Results'] = lists
        return results
