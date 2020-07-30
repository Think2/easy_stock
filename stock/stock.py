# -*- coding: utf-8 -*-

import os
import sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.dirname(cur_dir)
sys.path.append(cur_dir)
sys.path.append(dst_dir)

import time
import datetime
import pandas as pd
import crawler.download as dl

import stockdata as sd
import stock_bs as sb
import stock_real_time as srt

from tools import log
log = log.get_logger()

data_path = dst_dir+os.sep+'data_csv'+os.sep
bs_data_dir = dst_dir+os.sep+'data_csv'+os.sep+'bs_data'+os.sep

data_dir = bs_data_dir 

class Stock():
    '''stock api midle SDK, to get some data from ohter api
       1. get prce of (day, minute...)
       2. data analysis 
    '''
    def __init__(self, stocks=[]):
        self.stock_list = []
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

    def get_hist_data(self, codes, start_time, end_time):
        if len(codes)>0: 
            df = sb.download_data(codes, start_time, end_time)
            return df
        else:
            df = pd.DataFrame()
            return df 

    def get_real_data(self, codes):
        df = srt.get_real_time_data(codes)
        for code in df['code']:
            data = df[df['code']==code]
            sk = self.get_stock_obj(code)
            if sk is not None:
                sk.set_data(data)
        return sk.get_data()

    def get_real_data_by_skobj(self, skobjs):
        codes = []
        for sk in skobjs:
            codes.append(sk.code)
        df = srt.get_real_time_data(codes)
        if df is None:
            return False 
        for code in df['code']:
            data = df[df['code']==code]
            data = data.reset_index().T.to_dict()[0]
            sk = self.get_stock_obj(code)
            if sk is not None:
                sk.set_data(data)
        return True 
     
    def get_all_stock_list_form_network(self):
        df = sb.all_stock_list()
        return df

    def update_stock_list_to_file(self, filename=''):
        df = self.get_all_stock_list_form_network()
        if filename=='':
            filename = data_path + 'bs_stock_list.csv'
        if df.empty is False:
            log.info('save to' + filename)
            df.to_csv(filename, encoding="gbk", index=False)

    def update_stock_data_to_file(self, file_list=''):
        #codes = self.stock_list
        if file_list!='':
            filename  = file_list
        else:
            filename = 'all_list_filter.csv'

        test_file = data_dir+'sh.000001.csv'
        if os.path.exists(test_file):
            print('get test file')
            dates = pd.read_csv(test_file, encoding='gbk')['date']
            dates = list(dates)
            last_date = dates[-1]
            year = int(last_date.split('-')[0])
            month = int(last_date.split('-')[1])
            day = int(last_date.split('-')[2])
            date = datetime.datetime(year, month, day) + datetime.timedelta(days=1)
            last_date = date.strftime('%Y-%m-%d')
        else:
            last_date = '2019-01-01'
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        codes = list(pd.read_csv(filename, encoding='gbk')['code'])
        print(last_date)
        print(now_date)
        if last_date==now_date:
            print('data is update to new')
            return None

        df_list = sb.download_data(codes, last_date, now_date)
        
        if os.path.exists(data_dir) is False:
            print('create dir:'+ data_dir)
            os.mkdir(data_dir)

        for df in df_list:
            try:
                if df.empty==True:
                    print('skip...')
                    continue
                #base = dst_dir + '/data_csv/bs_data/'
                base = data_dir
                name = base+('%s' % df['code'][0]) + '.csv'
                if os.path.exists(name):
                    #print('append')
                    df.to_csv(name, encoding="gbk", mode='a', index=False, header=False)
                else:
                    #print('create')
                    df.to_csv(name, encoding="gbk", index=False)
            except (Exception, KeyError, IndexError) as e:
                log.error(e)
                log.error('write data fail, code:'+df['code'][1])
                continue

    def run(self):
        # 提交列表信息数据给爬虫，实时获取数据
        pass


if __name__ == '__main__':
    lst = ['sh000001', 'sh601068']
    sk = Stock(lst)
    #sk.update_stock_data_to_file('test.csv')
    #sk.update_stock_data_to_file()
    sk.update_stock_list_to_file()

