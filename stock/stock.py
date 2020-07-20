# -*- coding: utf-8 -*-

import os
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.dirname(cur_dir)
sys.path.append(cur_dir)
sys.path.append(dst_dir)

import crawler.download as dl

import stockdata as sd
import stocklist as sl



class Stock():
    '''stock api midle SDK, to get some data from ohter api
       1. get prce of (day, minute...)
       2. data analysis 
    '''
    def __init__(self, *stocks):
        self.stock_list = []
        self.sk_list_obj = sl.StockList()
        if len(stocks)>0:
            for code in stocks:
                data = sd.StockData(code)
                self.stock_list.append(data)

    def get_stock_list(self):
        return self.stock_list
    
    def add_code(self, code):
        print('add code: %s' % code)
        data = sd.StockData(code)
        self.stock_list.append(data)

    def del_code(self, code):
        for data in self.stock_list:
            if code==data.code:
                print('del code: %s' % code)
                self.stock_list.remove(data)
                break

    def get_stock_obj(self, code):
        for i in range(0, len(self.stock_list)):
            if self.stock_list[i].code == code:
                return self.stock_list[i]
        return None

    def check_unique_stock_list(self):
        data = self.stock_list
        for i in range(0, len(data)):
            for y in range(i+1, len(data)):
                if data[y].code==data[i].code:
                    print('check unique..del %s' % data[y].code)
                    self.stock_list.remove(data[y])

    def get_hist_data(self, code, start_time, end_time):
        if code in self.stock_list:
            pass
        else:
            return dict()

    def get_real_data(self, code):
        sk = self.get_stock_obj(code)
        if sk is not None:
            return sk.get_data()
     
    def get_all_stock_list_form_network(self):
        return self.sk_list_obj.get_all_stock_list()

    def run(self):
        # 提交列表信息数据给爬虫，实时获取数据
        self.sk_list_obj.run_monitor(self.stock_list)


