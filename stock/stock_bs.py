import baostock as bs
import pandas as pd
import sys
import os
import multiprocessing
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from datetime import datetime

def all_stock_list():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:'+lg.error_code)
    print('login respond  error_msg:'+lg.error_msg)

    #### 获取证券信息 ####
    rs = bs.query_all_stock(day='2020-07-16')
    print('query_all_stock respond error_code:'+rs.error_code)
    print('query_all_stock respond  error_msg:'+rs.error_msg)
    #### 登出系统 ####
    bs.logout()
    
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data = rs.get_row_data()
        if data[1] != '0':
            #data[0] = data[0].replace('.', '')
            data_list.append(data)
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result

def download_one_data(args, start_date='', end_date='', queue=None):
    #bs.login()
    code = ''
    if isinstance(args, tuple):
        code = args[0]
        start_date = args[1]
        end_date = args[2]
    else:
        code = args
    
    data_list = []
    k_rs = bs.query_history_k_data_plus(code,
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
        start_date=start_date, end_date=end_date,
        frequency="d", adjustflag="2")
    print("Downloading :" + code + ':' + k_rs.error_msg)
    
    while (k_rs.error_code == '0') & k_rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(k_rs.get_row_data())
    result = pd.DataFrame(data_list, columns=k_rs.fields)
    
    if isinstance(queue, list):
        queue.append(result)
        time.sleep(0.1)
    else:
        if queue is not None:
            queue.put(result)
            time.sleep(0.1)
    #bs.logout()
    return result

def download_data(code_list, save_path, start_date, end_date):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    #print('login respond error_code:'+lg.error_code)
    #print('login respond  error_msg:'+lg.error_msg)
    
    data_df_list = []
    
    '''
    # 使用多进程处理
    pool = multiprocessing.Pool(processes=10)
    queue = multiprocessing.Manager().Queue()

    for code in code_list:
        pool.apply_async(download_one_data, (code, start_date, end_date, queue))
    pool.close()
    pool.join()

    print(queue.qsize())
    for i in range(queue.qsize()):
        data = queue.get()
        data_df_list.append(data)
    '''
    '''
    # 使用线程池
    queue = []
    future_list = []
    pool = ThreadPoolExecutor(max_workers=20)
    
    with ThreadPoolExecutor(2) as executor: # 创建 ThreadPoolExecutor 
        for code in code_list:
            future_list.append(pool.submit(download_one_data, (code, start_date, end_date, queue)))
            
    for future in as_completed(future_list):
        result = future.result() # 获取任务结果
        name = save_path+('%s' % result['code'][1]) + '.csv'
        if os.path.exists(name):
            result.to_csv(name, header=None, index=False, mode='a', encoding='gbk')
        else:
            result.to_csv(name, encoding="gbk", index=False)
        data_df_list.append(result)
        #print("%s get result : %s" % (threading.current_thread().getName(), result))
    '''
    
    for code in code_list:
        data = download_one_data(code, start_date, end_date)
        data_df_list.append(data)
    
    #### 登出系统 ####
    bs.logout()
    #print(queue)
    #print(data_df_list)
    return data_df_list

def update_stock_list(code_list, start_date='', end_date=''):
    pass

if __name__ == '__main__':
    # 获取指定日期全部股票的日K线数据
    #df = all_stock_list()
    #df.to_csv('./all_list.csv', encoding="gbk", index=False)
    #exit()
    codes = list(pd.read_csv('all_list_filter.csv', encoding='gbk')['code'])
    df_list = download_data(codes, './bs_data/', '2019-07-01', '2020-07-18')
    for df in df_list:
        base = './bs_data/'
        name = base+('%s' % df['code'][1]) + '.csv'
        df.to_csv(name, encoding="gbk", index=False)
    


