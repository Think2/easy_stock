# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse

import os
import requests
import re
from bs4 import BeautifulSoup

from ..tools import log
log = log.get_logger()

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

class Download():

    def __init__(self, url, data=None, encoding='utf-8'):
        self.response = None
        self.url = url
        self.encoding = encoding
        #if data is not None:
        #    self.data = bytes(urllib.parse.urlencode(data)) 
        self.data = data
        self.request = urllib.request.Request(self.url, self.data, headers=headers)

    def get_html_text(self):
        try:
            self.response = self.request.urlopen(self.url, timeout=5)
            return self.response.read().encoding.('utf-8')
        except:
            log.error('get rul %s fail' % self.url)
            return ''

    def get_response_code(self):
        if self.response is not None:
            return self.response.getcode()
        else:
            log.error('not get response')
            return 404


