#!/usr/bin/python3
import os
import re
import sys
from functools import reduce


INSERTED = '#'

if len(sys.argv) < 2:
    print('Usage: python3', __file__, 'FILE_1 [FILE_2 FILE_3, ...]')
    exit()

files = list()
for filename in sys.argv[1:]:
    with open(filename, 'r') as f:
        files.append(f.readlines())

file_len = len(files)
result = list()

max_lines, min_lines = len(max(files, key=len)), len(min(files, key=len))

def str_comp(a, b, inserted=INSERTED):
    result = a if a == b else inserted
    return result

for lines in zip(*files):
    this_line = list()
    for character in zip(*lines):
        this_line.append(reduce(str_comp, character))
    result.append(''.join(this_line))

for line in result:
    print(line[:-1].strip())

