#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 11:24:15 2016

use main()
@author: 老徐
"""
from datetime import datetime
from datetime import timedelta
from pandas import read_excel
from numpy import array
from numpy import nan


def str2time(str):
    try:
        return datetime.strptime(str, '%H:%M')
    except:
        #print('err with time as', str)
        return datetime.strptime('0', '%H')


def main():
    filename = input('请输入文件路径:\n')    #'/home/ash/Desktop/1_标准报表.xls'#
    sheetname = input('请输入sheetname:\n')
    column = input('请输入该页的第几个版块:\n')
    xls_column = {'1':'A:N', '2':'P:AC', '3':'AE:AR'}
    data = read_excel(filename,  sheetname=sheetname, parse_cols=xls_column[column], skiprows=10)
    data = data.replace(to_replace={'旷工' : nan})
    data = array(data)
    data = data[:,[1,3,6,8,10,12]]
    time_of_a_day = timedelta(0)
    for _ in range(len(data)):
        for __ in range(3):
            if (data[_, __*2] is not nan) and (data[_, __*2+1] is not nan):
                time_of_a_day += str2time(data[_, __*2+1]) - str2time(data[_, __*2])
    result = time_of_a_day
    sec = result.total_seconds()
    s = sec % 3600
    hour = (sec - s) / 3600
    minutes = s / 60
    print('total {0:d} hours and {1:.0f} mins'.format(hour, minutes))
    print('for my lover, 小胖儿～, 13自动化老徐')
    return result


if __name__ == "__main__":
    main()
    input('\n\n请输入回车继续')
