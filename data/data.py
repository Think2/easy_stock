# -*- coding: utf-8 -*-
'''
# 保存本地股票列表文件名，暂定为csv格式文件
# 数据库对象，包含列表信息和不同自选股列表
# 数据的读取、保存 
# 默认列表数据
'''

import os
import csv
import pandas

class Data():
    def __init__(self, file = ''):
        self.file_name = file

    def is_has_file(self, file):
        if len(file)>0:
            return os.path.exists(file)
        else:
            return False

    def get_file_data(self, file):
        data = []
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row[0].strip())
        return data

    def save_data_to_file(self, data, file=''):
        if file == '':
            file = self.file_name
        with open(file, 'w', newline='') as f:
            writer = csv.writer(f)
            for row in data:
                writer.writerow([row])

    def get_stock_list(self):
        file = self.file_name
        if self.is_has_file(file):
            return self.get_file_data(file)
        else:
            return None 

