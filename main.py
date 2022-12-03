#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/9 0:56
# @Author  : ningzijing
# @Site    : 
# @File    : main.py
# @Software: PyCharm
import datetime
import traceback

import mapping_data
import matching_data
import primary_mapping_data


def main():
    try:
        mapping_data.CompareMappingData().get_pairwise()
        matching_data.CompareMatchingData().get_pairwise()
        primary_mapping_data.ComparePrimaryMappingData().get_pairwise()
    except:
        traceback.print_exc()
        now = datetime.datetime.strftime()
        log_name = 'error_log' + now + '.txt'
        with open(log_name,'a') as file:
            file.write(traceback.format_exc())
        file.close()

if __name__ == '__main__':
    main()