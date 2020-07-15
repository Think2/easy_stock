# -*- coding: utf-8 -*-
from .stockdata import StockData
from .stocklist import StockList

import os
import sys
dst_dir = os.path.abspath('.')
sys.path.append(dst_dir)
from crawler.download import Download

import json  # python自带的json数据库
from random import randint  # python自带的随机数库
import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


def calculate_price(stock_code):

    return df
    
    