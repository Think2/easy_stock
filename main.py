# -*- coding: utf-8 -*-

import time
import re
import urllib.parse
import multiprocessing
from threading import Thread

from crawler.download import Download
from crawler.parse import Parser
from stock.stock import Stock
from data.data import Data
import stock.stock_real_time as srt
import stock.stock_minutes as sm
import stock.stock_day as sd
import stock.stock_update as sup

from tools import log
log = log.get_logger()

stock_manager = Stock()
stock_data = Data('./data_csv/file.csv')

# 腾讯股票列表信息
tencent_url = 'https://stock.gtimg.cn/data/index.php?'
# 股票数据网站
data_url = 'http://www.sse.com.cn/js/common/ssesuggestdata.js'
# 新浪获取股票实时价格
sina_get_stock_url = 'http://hq.sinajs.cn/list='

def get_stock_data(code):
    url = sina_get_stock_url+code
    sk_data = dict()
    req = Download(url)
    text = req.get_html_text()
    if text=='':
        return None
    results = re.findall(r'"(.*?)"', text, re.S)
    datas = results[0]
    data = datas.split(',')
    sk_data.update({'name': data[0]})
    sk_data.update({'open': data[1]})
    sk_data.update({'close': data[2]})
    sk_data.update({'cur_price': data[3]})
    sk_data.update({'high': data[4]})
    sk_data.update({'low': data[5]})
    sk_data.update({'number': data[8]})
    sk_data.update({'money': data[9]})
    sk_data.update({'flush_time': data[30]+' '+data[31]})
    cur = float(data[3])
    close = float(data[2])
    p_change = 100*(cur - close)/close
    p_change = round(p_change, 2) 
    sk_data.update({'p_change': p_change})
    return sk_data


def process_func(url, queue):
    sk_download = Download(url)
    text = sk_download.get_html_text(url)
    pattern = re.compile(r's[h|z]\d{6}', re.S)
    results = re.findall(pattern, text)
    #print(results)
    for data in results:
        #lst.append(data)
        queue.put(data)
    time.sleep(0.1)
    print('%s is ok' % url)

def get_list_from_tencent():
    total = 1
    url = ''
    params = {
        'appn': 'rank',
        't': 'ranka/chr',
        'p': '0',
        'o': '-1',
        'l': '80',
        'v': 'list_data'
    }
    data = urllib.parse.urlencode(params)
    url = tencent_url+data
    sk_download = Download(url)
    text = sk_download.get_html_text(url)
    if text=='':
        print('get text fail..url: %s' % url)
        return None
    total = re.search(r'.*?total:(\d+),', text).group(1)
    print(int(total))

    pool = multiprocessing.Pool(processes=10)
    queue = multiprocessing.Manager().Queue()
    #for index in range(0, 1):
    for index in range(0, int(total)):
        params['p'] = index
        data = urllib.parse.urlencode(params)
        url = tencent_url+data
        print('add %s to pool' % url)
        pool.apply_async(process_func, (url, queue))
    pool.close()
    pool.join()
    lst = []
    print(queue.qsize())
    for i in range(queue.qsize()):
        data = queue.get()
        if data not in lst:
            #lst.append(queue.get())
            lst.append(data)
        #print('[%d] : %s' % (i,queue.get()))
    return lst 

def get_list_from_js():
    sk_download = Download(data_url)
    text = sk_download.get_html_text()
    lst = []
    pattern = re.compile(r'.*?"(\d{6})".*?"(.*?)".*?;', re.S)
    lst = re.findall(pattern, text)
    return lst

def save_stock_list_to_file(file, data):
    print('save data list to %s' % file)
    stock_data.save_data_to_file(data, file)

def get_all_stock_list_from_network():
    lst = get_list_from_tencent()
    #lst = get_list_from_js()
    save_stock_list_to_file('./data_csv/network.csv', lst)
    return lst

def stock_monitor_run(sk_list):
    log.info('start to run stock nonitor')
    # 启动列表监控
    #stock_manager.run()
    '''
    for obj in stock_manager.get_stock_list():
        data = get_stock_data(obj.code)
        if data is None:
            time.sleep(5)
            continue
        sk_obj = stock_manager.get_stock_obj(obj.code) 
        sk_obj.set_data(data)
    '''
    while True:
        if stock_manager.get_real_data_by_skobj(sk_list) is False:
            log.info('get data fail, sleep 5')
            time.sleep(5)
            continue

        if len(sk_list) > 0:
            for sk in sk_list:
                data = sk.get_data()
                log.info(data['name']+':'+str(data['cur_price'])+'  ' + str(data['p_change'])+'  ' + str(data['monitor_price']))
            time.sleep(3)
    log.info('%s run end' % stock_monitor_run.__name__)

def stock_list_setup():
    log.info('start to setup stock list')
    # 检查本地股票列表信息
    stock_list = stock_data.get_stock_list()
    if stock_list is not None:
        # 根据列表信息，创建股票对象
        for data in stock_list:
            stock_manager.add_code(data[0])
            sk_data = stock_manager.get_stock_obj(data[0])
            if len(data)>1:
                sk_data.set_monitor_price(float(data[1]))

    # 返回股票对象列表信息
    return stock_manager.stock_list

def create_thread(func, args=None):
    if args is None:
        t = Thread(target=func)
    else:
        t = Thread(target=func, args=args)
    t.start()
    return t

if __name__=='__main__':
    log.info('run main')
    thread_lst = []
    #get_all_stock_list_from_network()
    sk_list = stock_list_setup()
    #lst = ['sh000001', 'sh601068']
    #print(rt.get_real_time_data(lst))
    #print(sm.get_minutes_data('sh000001', 60))
    #print(sd.get_day_data('sh000001', 'month', 10))
    #sup.update_all_data()
    #exit()
    # if len(sk_list) > 0:
        # while True:
            # stock_monitor_run()
            # for sk in sk_list:
                # data = sk.get_data()
                # log.info(data['name']+':'+data['cur_price']+'  ' + str(data['p_change']))
            # time.sleep(3)
    stock_monitor_run(sk_list)
    exit(1)
    thread_lst.append(create_thread(stock_monitor_run, (sk_list,)))
    print('create thread end')
    for i in thread_lst:
        i.join()
    print('wait end')







