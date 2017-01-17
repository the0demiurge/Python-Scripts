#!/usr/bin/env python3
""" This is a python script copying stock data from a mobile hard-disk.
"""
import os
import random
import shutil

DATA_PATH = '/media/ash/Seagate Backup Plus Drive'
TARGET_PATH = '/media/ash/39D1F4D861FCE21C'
SAMPLE_RATIO = 0.095
dirs = ['%d' % i for i in range(2009, 2014)]

for path in dirs:
    print(path)
    pathin = DATA_PATH + '/' + path
    file_list = os.listdir(pathin)
    full_num = len(file_list)
    sample_num = int(full_num * SAMPLE_RATIO)
    to_copy = random.sample(file_list, sample_num)

    pathout = TARGET_PATH + '/' + path
    if not os.path.isdir(pathout):
        os.mkdir(pathout)
    for index, file in enumerate(to_copy):
        shutil.copyfile(pathin + '/' + file, pathout + '/' + file)
        print('copying %2.2f' % (100 * index / sample_num), end='%\r')
