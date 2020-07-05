# -*- coding: utf-8 -*-
from .stock import StockData

class Stock():
    '''stock api midle SDK, to get some data from ohter api
       1. get prce of (day, minute...)
       2. data analysis 
    '''
    def __init__(self, *stocks):
        self.stock_list = []
        if len(stocks)>0:
            for code in stocks:
                data = StockData(code)
                self.stock_list.append(data)
    
    def add_code(self, code):
        data = StockData(code)
        self.stock_list.append(data)

    def del_code(self, code):
        for data in self.stock_list:
            if code==data.code:
                self.stock_list.remove(data)
                break

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
        if code in self.stock_list:
            pass
        else:
            return dict()





