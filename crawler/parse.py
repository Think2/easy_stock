# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse

import os
import requests
import re
from bs4 import BeautifulSoup

if __name__=='__main__':
    import sys
    tools_dir = os.path.abspath('../tools')
    sys.path.append(tools_dir)
    import log
    log = log.get_logger()
else:
    from tools import log

class Parser():
    def __init__(self, html, encoding='utf-8'):
        self.html = html
        self.encoding = encoding

    def parse_stock_code(self, re_pattern=''):
        lst = []
        if re_pattern != '':
            pattern = re.compile(re_pattern, re.S)
        else:
            pattern = re.compile('.*?"(\d{6})".*?"(.*?)".*?;', re.S)
        #pattern = re.compile('\d{6}')
        lst = re.findall(pattern, self.html)
        return lst


        
    def get_contents(self, mark, attr='', restr=''):
        lst = []
        if mark=='':
            log.error('need mark rule')
            return ''
        soup = BeautifulSoup(self.html, 'html.parser')
        a = soup.find_all(mark)
        for i in a:
            try:
                href = i.attrs[attr]
                lst.append(re.findall(restr, href)[0])
            except:
                continue
        return lst

