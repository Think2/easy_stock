# -*- coding: utf-8 -*-
from stockdata import StockData
from stocklist import StockList

import os
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.dirname(cur_dir)
sys.path.append(cur_dir)
sys.path.append(dst_dir)

from crawler.download import Download

import pandas as pd
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# 腾讯股票列表信息
tencent_url = 'https://stock.gtimg.cn/data/index.php?'
# 股票数据网站
data_url = 'http://www.sse.com.cn/js/common/ssesuggestdata.js'
# 新浪获取股票实时价格
sina_get_stock_url = 'http://hq.sinajs.cn/list='


def get_real_time_data(codes):
    # =====抓取数据
    url = sina_get_stock_url + ','.join(codes)
    #url = sina_get_stock_url + ','.join(['sh000001', 'sh601068'])
    #print(url)
    req = Download(url)
    content = req.get_html_text()
    #print(content)
    # =====将数据转换成DataFrame
    content = content.strip()  # 去掉文本前后的空格、回车等
    data_line = content.split('\n')  # 每行是一个股票的数据
    data_line = [i.replace('var hq_str_', '').split(',') for i in data_line]
    df = pd.DataFrame(data_line, dtype='float')
    # =====对DataFrame进行整理
    df[0] = df[0].str.split('="')
    df['code'] = df[0].str[0].str.strip()
    df['name'] = df[0].str[-1].str.strip()
    df['cur_price'] = df[3]
    df['date'] = df[30] + ' ' + df[31]  # 股票市场的K线，是普遍以当跟K线结束时间来命名的
    df['date'] = pd.to_datetime(df['date'])
    rename_dict = {1: 'open', 2: 'preclose', 3: 'close', 4: 'high', 5: 'low', 6: 'buy1', 7: 'sell1',
               8: 'amount', 9: 'volume', 32: 'status'}
    # 其中amount单位是股，volume单位是元
    df.rename(columns=rename_dict, inplace=True)
    df['status'] = df['status'].astype(str).str.strip('";')
    df = df[['code', 'name', 'date', 'open', 'high', 'low', 'close', 'preclose', 'amount', 'volume',
             'buy1', 'sell1', 'status']]
    return df

if __name__=='__main__':
    print('test get real time data')
    codes = ['sh000001', 'sh601608']
    df = get_real_time_data(codes)
    print(df)
    
    
