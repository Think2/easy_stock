# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse

import os
import requests
import re
from bs4 import BeautifulSoup

import os
import sys
dst_dir = os.path.abspath('.')
sys.path.append(dst_dir)
from tools import log
log = log.get_logger()


headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

class Download():

    def __init__(self, url, data=None, params=None, encoding='utf-8'):
        self.response = None
        self.url = url
        self.params = params
        self.encoding = encoding
        #if data is not None:
        #    self.data = bytes(urllib.parse.urlencode(data)) 
        self.data = data
        self.request = urllib.request.Request(self.url, self.data, headers=headers)
    
    def get_html_text(self, set_url=''):
        url = ''
        if set_url != '':
            url = set_url 
        else:
            url = self.url
        try:

            #self.response = urllib.request.urlopen(self.request, timeout=5)
            #return self.response.read().decode(self.encoding)
            req = requests.get(url, params=self.params, headers=headers)
            if req.encoding == 'ISO-8859-1':
                encodings = requests.utils.get_encodings_from_content(req.text)
                if encodings:
                    encoding = encodings[0]
                else:
                    encoding = req.apparent_encoding
            else:
                encoding = req.encoding
            if req.encoding is None:
                encoding = self.encoding
            #print('use encoding: %s' % encoding)
            #return req.content.decode(encoding, 'ignore').encode('utf-8', 'ignore') 
            #print(req.content.decode(encoding, 'ignore'))
            return req.content.decode(encoding, 'ignore')
        except (Exception, ConnectionError) as e:
            log.error(e)
            log.error('get rul %s fail, code : %d' % (self.url, self.get_response_code()))
            return ''

    def get_response_code(self):
        if self.response is not None:
            return self.response.getcode()
        else:
            log.error('not get response')
            return 404


if __name__ == '__main__':
    test = Download('https://www.baidu.com')
    data = test.get_html_text()
    print(data)

