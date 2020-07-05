# -*- coding: utf-8 -*-
import time

class StockData():
    def __init__(self, code, name=''):
        self.code = code  #代码
        self.name = name  #名字
        self.open = 0     #开盘价
        self.close = 0    #收盘价
        self.high = 0     #最高价
        self.low = 0      #最低价
        self.volume = 0   #成交量
        self.turnover = 0   #换手率
        self.p_change = 0.0   #涨跌幅

        self.is_flush = 0   #数据是否为最新
        self.flush_time = 0 #数据刷新时间

    def get_data(self):
        d = dict()
        d.update({'code':self.code})
        d.update({'name':self.name})
        d.update({'open':self.open})
        d.update({'close':self.close})
        d.update({'high':self.high})
        d.update({'low':self.low})
        d.update({'volume':self.volume})
        d.update({'turnover':self.turnover})
        d.update({'change':self.change})
        return d 

    def is_data_flush(self):
        return self.is_flush

    def get_flush_time(self):
        return self.flush_time

    def set_flush_time(self, time=''):
        if time =='':
            self.flush_time = time.strftime('%Y-%m-%d %H-%M-%S')
        else:
            self.flush_time = time
        return self.flush_time 

