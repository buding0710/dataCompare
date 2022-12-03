#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/3 16:59
# @Author  : ningzijing
# @Site    : 
# @File    : data_compare.py
# @Software: PyCharm
import configparser
import csv
import datetime
import os

import pandas as pd
import xlrd
import xlwt
from xlutils.copy import copy


class CompareMatchingData():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        self.data = config.items('matching')
        #print(self.data)#[('csv1', '{"table":"matching1.csv:matching2.csv","header":"0:0"}')]

    def get_pairwise(self):
        for i in range(len(self.data)):
            filetype = self.data[i][0]
            dict = eval(self.data[i][1])  # eval()函数，可以把字符串里面的格式给提取出来
            files = dict['table'].split(':')
            headers = dict['header'].split(':')

            h1 = eval(headers[0]) if headers[0] == 'None' else int(headers[0])  # 三元表达式,eval将字符串'None'提取为数据类型None
            h2 = eval(headers[1]) if headers[1] == 'None' else int(headers[1])  # 三元表达式,eval将字符串'None'提取为数据类型None

            if 'txt' in filetype:
                self.compare_for_txt(files[0],h1,files[1],h2)
            elif 'csv' in filetype:
                self.compare_for_csv(files[0],h1,files[1],h2)
            elif 'xls' in filetype:
                self.compare_for_xls(files[0],h1,files[1],h2)
            else:
                pass

    def compare_for_csv(self,file1,header1,file2,header2):
        # 读取两个表
        dt1 = pd.read_csv(file1,encoding='gbk',header=header1)
        dt2 = pd.read_csv(file2,encoding='gbk',header=header2)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'matching_compare_result' + now + '.csv'

        for i in range(dt1.shape[1]):#列循环
            for j in range(dt1.shape[0]):#行循环
                # print(dt1.iloc[j,i],dt2.iloc[j,i])
                value1= str(dt1.iloc[j,i]).strip()#忽略前后空格
                value2= str(dt2.iloc[j,i]).strip()
                if value1 == value2:
                    continue
                else:
                    # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                    datalist = []
                    datalist.append(file1)
                    datalist.append("列%d,行%d" %(i,j))
                    datalist.append(value1)
                    datalist.append(file2)
                    datalist.append("列%d,行%d" %(i,j))
                    datalist.append(value2)
                    print(datalist)
                    with open(result_name, "a") as file:
                        writer = csv.writer(file)
                        writer.writerow(datalist)

    def compare_for_txt(self,file1,header1,file2,header2):
         # 读取两个表
        dt1 = pd.read_csv(file1, sep='|', header=header1)
        dt2 = pd.read_csv(file2, sep='|', header=header2)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'matching_compare_result' + now + '.txt'
        for i in range(dt1.shape[1]):#列循环
            for j in range(dt1.shape[0]):#行循环
                # print(dt1.iloc[j,i],dt2.iloc[j,i])
                value1= str(dt1.iloc[j,i]).strip()
                value2= str(dt2.iloc[j,i]).strip()
                if value1 == value2:
                    continue
                else:
                    # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                    with open(result_name, "a") as file:
                        print(file1 + '|' + "列%d,行%d" %(i,j) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(i,j) + '|' + value2 + '\n')
                        file.write(file1 + '|' + "列%d,行%d" %(i,j) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(i,j) + '|' + value2 + '\n')

    def compare_for_xls(self,file1,header1,file2,header2):
        # 读取两个表
        dt1 = pd.read_excel(file1,header=header1)#header表示第i行为列标签，并忽略其之前的数据
        dt2 = pd.read_excel(file2,header=header2)

        # 导入xlwt模块
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'matching_compare_result' + now + '.xls'
        workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
        sheet1 = workbook.add_sheet(now,cell_overwrite_ok=True)  # 新建sheet
        workbook.save(result_name)

        for i in range(dt1.shape[1]):  # 列循环
            for j in range(dt1.shape[0]):  # 行循环
                # print(dt1.iloc[j,i],dt2.iloc[j,i])
                value1= str(dt1.iloc[j,i]).strip()
                value2= str(dt2.iloc[j,i]).strip()
                if value1 == value2:
                    continue
                else:
                    data = xlrd.open_workbook(result_name, formatting_info=True)
                    excel = copy(wb=data)  # 完成xlrd对象向xlwt对象转换
                    excel_table = excel.get_sheet(0)  # 获得要操作的页
                    table = data.sheets()[0]
                    nrows = table.nrows  # 获得行数
                    # ncols = table.ncols  # 获得列数
                    print(file1 + '|' + "列%d,行%d" %(i,j) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(i,j) + '|' +
                        value2 + '\n')
                    excel_table.write(nrows+1, 0, file1)  # 第1行第1列数据
                    excel_table.write(nrows+1, 1, "列%d,行%d" %(i,j))  # 第1行第2列数据
                    excel_table.write(nrows+1, 2, value1)
                    excel_table.write(nrows+1, 3, file2)
                    excel_table.write(nrows+1, 4, "列%d,行%d" %(i,j))
                    excel_table.write(nrows+1, 5, value2)
                    excel.save(result_name)



