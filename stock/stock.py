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
        self.get_data_func=None
    
    def add_code(self, code):
        self.stock_list.append(code)

    def del_code(self, code):
        self.stock_list.remove(code)

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





