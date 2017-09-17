#!/usr/bin/env python
# 把当前文件夹里面多个excel整合到一起，
# 以"学号"的列进行排序，生成result.xlsx

import os
import pandas as pd

data = list()
if os.path.exists('result.xlsx'):
    os.remove('result.xlsx')

for i in os.listdir():
    if i[0] != '.' and i.split('.')[-1][:3] == 'xls':
        print(i)
        data.append(pd.read_excel(i, sheetname='Sheet1'))

c = pd.concat(data)

# 如果不需要排序，把下一行删掉即可
c.sort_values('学号', inplace=True)

c.to_excel('result.xlsx', index=False)
