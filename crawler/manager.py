# -*- coding: utf-8 -*-

import os
import requests
import re
from bs4 import BeautifulSoup

from ..tools import log
log = log.get_logger()


class CrawlerManager():
    def __init__(self, stock_objs):
        self.sk_objs = stock_objs

    # 增加未爬取的url
    def add_new_urls(self, url):
        pass

    # 判断是否还有未爬取的url
    def has_new_urls(self):
        pass

    # 获取未爬取的url
    def get_new_urls(self):
        pass

    # 获取未爬取剩余url数量
    def new_urls_size(self):
        pass

    # 获取已经爬取剩余url数量
    def old_urls_size(self):
        pass

    def run(self):
        pass



if __name__ == '__main__':
    main()
