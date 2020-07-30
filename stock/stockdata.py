# -*- coding: utf-8 -*-
import time

class StockData():
    def __init__(self, code, name=''):
        self.code = code  #代码
        self.name = name  #名字
        self.cur_price = 0.0  #当前价格
        self.open = 0     #开盘价
        self.close = 0    #收盘价
        self.preclose = 0.0 #昨收盘价
        self.high = 0     #最高价
        self.low = 0      #最低价
        self.volume = 0   #成交量
        self.amount = 0   #成交金额
        self.turnover = 0   #换手率
        self.p_change = 0.0   #涨跌幅

        self.is_flush = 0   #数据是否为最新
        self.flush_time = 0 #数据刷新时间
        self.monitor_price = []

    def get_data(self):
        d = dict()
        d.update({'code':self.code})
        d.update({'name':self.name})
        d.update({'cur_price':self.cur_price})
        d.update({'open':self.open})
        d.update({'close':self.close})
        d.update({'preclose':self.preclose})
        d.update({'high':self.high})
        d.update({'low':self.low})
        d.update({'volume':self.volume})
        d.update({'amount':self.amount})
        d.update({'turnover':self.turnover})
        d.update({'p_change':self.p_change})
        d.update({'monitor_price':self.monitor_price})
        return d 

    def set_data(self, kw):
        #print(kw)
        if 'name' in kw:
            self.name = kw['name']
        if 'cur_price' in kw:
            self.cur_price = kw['cur_price']
        if 'close' in kw:
            self.cur_price = kw['close']
        if 'open' in kw:
            self.open = kw['open']
        if 'close' in kw:
            self.close = kw['close']
        if 'preclose' in kw:
            self.preclose = kw['preclose']
        if 'high' in kw:
            self.high = kw['high']
        if 'low' in kw:
            self.low = kw['low']
        if 'volume' in kw:
            self.volume = kw['volume']
        if 'amount' in kw:
            self.amount = kw['amount']
        if 'turnover' in kw:
            self.turnover = kw['turnover']
        if 'p_change' in kw:
            self.p_change = kw['p_change']
        else:
            #p_change = 100*(self.cur_price - self.close)/self.close
            p_change = 100*(self.cur_price - self.preclose)/self.preclose
            p_change = round(p_change, 2) 
            self.p_change = p_change
        if 'flush_time' in kw:
            self.flush_time = kw['flush_time']

    def set_monitor_price(self, price):
        if self.cur_price < 0.001:
            self.monitor_price = [price, price]
            return None

        if self.cur_price < price:
            self.monitor_price = [0, price]
        else:
            self.monitor_price = [price, 0] 

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

