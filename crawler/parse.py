# -*- coding:utf-8 -*-
import urllib.request
import urllib.parse

import os
import requests
import re
from bs4 import BeautifulSoup

from ..tools import log
log = log.get_logger()


class Parser():
    def __init__(self, html, encoding='utf-8'):
        self.html = html
        self.encoding = encoding

    def get_contents(self, mark, attr='', restr=''):
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

