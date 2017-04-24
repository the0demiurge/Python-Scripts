#!/data/data/com.termux/files/usr/bin/python3
import sys
import os
import re

filename = sys.argv[-1]
if len(sys.argv) == 1:
    filename = 'tensorflow_api.csv'

with open(filename, 'r') as f:
    data = f.readlines()

name = data[0][2:-3]

ops = dict()
for i in data[1:]:
    if i[:2] == "# ":
        key = i[2:-3]
        ops[key] = list()
    elif i[0] != '#':
        ops[key].append(i.split(',')[0:2])

for key in ops:
    with open('%s.dot' % key, 'w') as f:
        print('digraph "%s"{' % key, file=f)
        print('rankdir="LR"', file=f)
        print('node [shape="box"]', file=f)
        #print('\t"{}" -> "{}"[color="red"];'.format(name, key))
        for value in ops[key]:
            print('\t\t"{}" -> "{}" -> "{}";'.format(key, value[0], value[1]), file=f)
        print('}', file=f)
        os.system('dot -T svg -o "%s.svg" "%s.dot"' %(key,key))


