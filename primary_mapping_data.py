#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/12 16:08
# @Author  : ningzijing
# @Site    : 
# @File    : primary_mapping_data.py
# @Software: PyCharm

import configparser
import csv
import os
import datetime

import pandas as pd
import xlrd
import xlwt
from xlutils.copy import copy


class ComparePrimaryMappingData():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini", encoding="utf-8")
        self.data = config.items('primary_mapping')
        # print(self.data)#[('csv1', 'mapping1.csv:0,1,2,3,4,5,6,7,8,9,10,11;mapping2.csv:11,10,9,8,7,6,5,4,3,2,1,0'), ('csv2', 'mapping3.csv:0,1,2,3,4,5,6,7,8,9,10,11;mapping4.csv:11,10,9,8,7,6,5,4,3,2,1,0'), ('txt3', 'mapping1.txt:0,1,2,3,4,5,6,7,8,9,10,11;mapping2.txt:11,10,9,8,7,6,5,4,3,2,1,0'), ('txt4', 'mapping3.txt:0,1,2,3,4,5,6,7,8,9,10,11;mapping4.txt:11,10,9,8,7,6,5,4,3,2,1,0'), ('xls5', 'mapping1.xls:0,1,2,3,4,5,6,7,8,9,10,11;mapping2.xls:11,10,9,8,7,6,5,4,3,2,1,0'), ('xls6', 'mapping3.xls:0,1,2,3,4,5,6,7,8,9,10,11;mapping4.xls:11,10,9,8,7,6,5,4,3,2,1,0')]

    def get_pairwise(self):
        for i in range(len(self.data)):
            filetype = self.data[i][0]
            dict = eval(self.data[i][1])  # eval()函数，可以把字符串里面的格式给提取出来
            files = dict['table'].split(':')
            headers = dict['header'].split(':')
            primary = dict['primary'].split(':')
            indexs = dict['index'].split(':')

            h1 = eval(headers[0]) if headers[0] == 'None' else int(headers[0])  # 三元表达式,eval将字符串'None'提取为数据类型None
            h2 = eval(headers[1]) if headers[1] == 'None' else int(headers[1])  # 三元表达式,eval将字符串'None'提取为数据类型None

            if 'txt' in filetype:
                self.compare_for_txt(files[0],h1,primary[0],indexs[0].split(','),files[1],h2,primary[1],indexs[1].split(','))
            elif 'csv' in filetype:
                self.compare_for_csv(files[0],h1,primary[0],indexs[0].split(','),files[1],h2,primary[1],indexs[1].split(','))
            elif 'xls' in filetype:
                self.compare_for_xls(files[0],h1,primary[0],indexs[0].split(','),files[1],h2,primary[1],indexs[1].split(','))
            else:
                pass

    def compare_for_csv(self,file1,header1,primary1,index1,file2,header2,primary2,index2):
        # 读取两个表
        dt1 = pd.read_csv(file1,encoding='gbk',header=header1)
        dt2 = pd.read_csv(file2,encoding='gbk',header=header2)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'mapping_compare_result' + now + '.csv'

        for i in range(dt1.shape[0]):  # 表1行循环
            p1 = str(dt1.iloc[i, int(primary1)]).strip()#获取表1主键
            for j in range(dt2.shape[0]): # 表2 行循环
                p2 = str(dt2.iloc[j, int(primary2)]).strip()#获取表2主键
                if p1 == p2:#在表2主键列寻找与表1相等的值
                    flag = 0 #如果相等，将flag置为0
                    for k in range(len(index1)):  # 映射列循环
                        in1 = int(index1[k])  # 映射关系列
                        in2 = int(index2[k])  # 映射关系列
                        # print(dt1.iloc[j,in1],dt2.iloc[j,in2])
                        value1 = str(dt1.iloc[i, in1]).strip()  # 获取对比单元格的值，忽略前后空格
                        value2 = str(dt2.iloc[j, in2]).strip()
                        if value1 == value2:
                            continue
                        else:
                            # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                            datalist2 = []
                            datalist2.append(file1)
                            datalist2.append("主键：%s" % p1)
                            datalist2.append("列%d,行%d" % (in1, i))
                            datalist2.append(value1)
                            datalist2.append(file2)
                            datalist2.append("列%d,行%d" % (in2, j))
                            datalist2.append(value2)
                            print(datalist2)
                            with open(result_name, "a") as file:
                                writer = csv.writer(file)
                                writer.writerow(datalist2)
                    break
                else:
                    # 如果表一的主键在表二找不到，则将flag置为1，需要输出该信息
                    flag = 1

            if flag == 1:
                # flag == 1,需要输出表一的主键在表二找不到的信息
                # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                datalist1 = []
                datalist1.append(file1)
                datalist1.append("主键：%s" % p1)
                datalist1.append("列%d,行%d" % (int(primary1), i))
                datalist1.append("在表%s列%d找不到" % (file2,int(primary2)))
                print(datalist1)
                with open(result_name, "a") as file:
                    writer = csv.writer(file)
                    writer.writerow(datalist1)

    def compare_for_txt(self,file1,header1,primary1,index1,file2,header2,primary2,index2):
         # 读取两个表
        dt1 = pd.read_csv(file1, sep='|', header=header1)
        dt2 = pd.read_csv(file2, sep='|', header=header2)

        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'mapping_compare_result' + now + '.txt'

        for i in range(dt1.shape[0]):#表1行循环
            p1 = str(dt1.iloc[i, int(primary1)]).strip()  # 获取表1主键
            for j in range(dt2.shape[0]):#表2行循环
                p2 = str(dt2.iloc[j, int(primary2)]).strip()  # 获取表2主键
                if p1 == p2:#在表2主键列寻找与表1相等的值
                    flag = 0 #如果相等，将flag置为0
                    for k in range(len(index1)):  # 映射列循环
                        in1 = int(index1[k])#映射关系列
                        in2 = int(index2[k])#映射关系列
                        # print(dt1.iloc[j,in1],dt2.iloc[j,in2])
                        value1= str(dt1.iloc[i,in1]).strip()# 获取对比单元格的值，忽略前后空格
                        value2= str(dt2.iloc[j,in2]).strip()
                        if value1 == value2:
                            continue
                        else:
                            # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                            with open(result_name, "a") as file:
                                print(file1 + '|' + "主键：%s" % p1 + '|' + "列%d,行%d" %(in1,i) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(in2,j) + '|' + value2 + '\n')
                                file.write(file1 + '|' + "主键：%s" % p1 + '|' + "列%d,行%d" %(in1,i) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(in2,j) + '|' + value2 + '\n')
                    break
                else:
                    # 如果表一的主键在表二找不到，则将flag置为1，需要输出该信息
                    flag = 1

            if flag == 1:
                # flag == 1,需要输出表一的主键在表二找不到的信息
                # 导入要保存的文件名，mode='a'可以控制连续写入csv文件
                with open(result_name, "a") as file:
                    print(file1 + '|' + "主键：%s" % p1 + '|' + "列%d,行%d" % (
                    int(primary1), i) + '|' + "在表%s列%d找不到" % (file2, int(primary2)) + '\n')
                    file.write(file1 + '|' + "主键：%s" % p1 + '|' + "列%d,行%d" % (
                    int(primary1), i) + '|' + "在表%s列%d找不到" % (file2, int(primary2)) + '\n')

    def compare_for_xls(self,file1,header1,primary1,index1,file2,header2,primary2,index2):
        # 读取两个表
        dt1 = pd.read_excel(file1,header=header1)#header表示第i行为列标签，并忽略其之前的数据
        dt2 = pd.read_excel(file2,header=header2)

        # 导入xlwt模块
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        result_name = file1.split('.')[0] + '_' + file2.split('.')[0] + '_' + 'mapping_compare_result' + now + '.xls'

        workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
        sheet1 = workbook.add_sheet(now,cell_overwrite_ok=True)  # 新建sheet
        workbook.save(result_name)

        for i in range(dt1.shape[0]):#表1行循环
            p1 = str(dt1.iloc[i, int(primary1)]).strip()  # 获取表1主键
            for j in range(dt2.shape[0]):#表2行循环
                p2 = str(dt2.iloc[j, int(primary2)]).strip()  # 获取表2主键
                if p1 == p2:#在表2主键列寻找与表1相等的值
                    flag = 0 #如果相等，将flag置为0
                    for k in range(len(index1)):  # 映射列循环
                        in1 = int(index1[k])#映射关系列
                        in2 = int(index2[k])#映射关系列
                        # print(dt1.iloc[j,in1],dt2.iloc[j,in2])
                        value1= str(dt1.iloc[i,in1]).strip()# 获取对比单元格的值，忽略前后空格
                        value2= str(dt2.iloc[j,in2]).strip()
                        if value1 == value2:
                            continue
                        else:
                            print(file1 + '|' + "主键：%s" % p1 + "列%d,行%d" %(in1,i) + '|' + value1 + '|' + file2 + '|' + "列%d,行%d" %(in2,j) + '|' +
                                value2 + '\n')
                            data = xlrd.open_workbook(result_name, formatting_info=True)
                            excel = copy(wb=data)  # 完成xlrd对象向xlwt对象转换
                            excel_table = excel.get_sheet(0)  # 获得要操作的页
                            table = data.sheets()[0]
                            nrows = table.nrows  # 获得行数
                            # ncols = table.ncols  # 获得列数
                            excel_table.write(nrows+1, 0, file1)  # 第1行第1列数据i
                            excel_table.write(nrows+1, 1, "主键：%s" % p1)
                            excel_table.write(nrows+1, 2, "列%d,行%d" %(in1,i))  # 第1行第2列数据
                            excel_table.write(nrows+1, 3, value1)
                            excel_table.write(nrows+1, 4, file2)
                            excel_table.write(nrows+1, 5, "列%d,行%d" %(in2,j))
                            excel_table.write(nrows+1, 6, value2)
                            excel.save(result_name)
                    break
                else:
                    # 如果表一的主键在表二找不到，则将flag置为1，需要输出该信息
                    flag = 1

            if flag == 1:
                # flag == 1,需要输出表一的主键在表二找不到的信息
                print(
                    file1 + '|' + "主键：%s" % p1 + '|' + "列%d,行%d" % (int(primary1), i) + '|' + "在表%s列%d找不到" % (file2, int(primary2)) + '\n')
                data = xlrd.open_workbook(result_name, formatting_info=True)
                excel = copy(wb=data)  # 完成xlrd对象向xlwt对象转换
                excel_table = excel.get_sheet(0)  # 获得要操作的页
                table = data.sheets()[0]
                nrows = table.nrows  # 获得行数
                # ncols = table.ncols  # 获得列数
                excel_table.write(nrows + 1, 0, file1)  # 第1行第1列数据i
                excel_table.write(nrows + 1, 1, "主键：%s" % p1)
                excel_table.write(nrows + 1, 2, "列%d,行%d" % (int(primary1), i))  # 第1行第2列数据
                excel_table.write(nrows + 1, 3, "在表%s列%d找不到" % (file2, int(primary2)))
                excel.save(result_name)
