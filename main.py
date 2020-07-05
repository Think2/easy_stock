# -*- coding: utf-8 -*-

import time

from stock.stock import Stock 
from data.data import Data
from tools import log

log = log.get_logger()

stock_manager = Stock()

def stock_monitor_run():
    log.info('start to run stock nonitor')
    # 启动列表监控
    stock_manager.run()

def stock_list_setup():
    log.info('start to setup stock list')
    # 检查本地股票列表信息
    stock_data = Data('./file.csv')
    stock_list = stock_data.get_stock_list()
    # 根据列表信息，创建股票对象
    for code in stock_list:
        stock_manager.add_code(code)
    # 返回股票对象列表信息
    return stock_manager.stock_list


if __name__=='__main__':
    log.info('run main')
    sk_list = stock_list_setup()
    stock_monitor_run()
    while True:
        for sk in sk_list:
            log.info(sk.get_data())
            time.sleep(1)






