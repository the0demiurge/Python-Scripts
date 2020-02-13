#!/usr/bin/env python3
import pandas as pd
import math
import sys

if len(sys.argv) != 3:
    print('用法：\npython3', __file__, '主表路径', '分表路径')
    exit()

master_table_name, partial_table_name = sys.argv[-2:]

header_master = ["已筹金额（元）\n含转账", "参与捐赠人次（人次）", "已筹金额（元）\n含转账及线下录入", "参与捐赠人次（人次）.1", "已筹金额（元）\n不含转账及线下录入", "参与捐赠人次（人次）.2", ]
header_partial = ['筹款量', '捐赠次数', '筹款量.1', '捐赠次数.1', '筹款量.2', '捐赠次数.2', ]

master_table = pd.read_excel(master_table_name, convert_float=False, sheet_name=None, skiprows=1, parse_dates=True, na_values='').popitem()[-1].applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x).dropna(subset=['备案编号'])
partial_table = pd.read_excel(partial_table_name, convert_float=False, sheet_name=None, skiprows=1).popitem()[-1].applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x).drop(['发起机构.1', '项目名称.1', '发起机构.2', '项目名称.2'], 1)
master_table = master_table.applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x)
partial_table = partial_table.applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x)
print('原始主表：', master_table.shape)
print('原始分表：', partial_table.shape)


def convert_return_to_newline(table):
    new_columns = [i.replace('\r', '\n').replace('\n\n', '\n') for i in table.columns]
    table.columns = new_columns
    return table


def drop_na_cols(table):
    table = table.dropna(axis=1, thresh=math.ceil(len(table) / 2))
    return table


def split_index(table, index):
    positive = table[index].dropna(axis=1, how='all')
    negative = table[index.apply(lambda x: not x)].dropna(axis=1, how='all')
    return positive, negative


master_table = convert_return_to_newline(drop_na_cols(master_table))
partial_table = drop_na_cols(partial_table)
# merge
result = pd.merge(left=master_table, right=partial_table, left_on=['慈善组织', '项目名称'], right_on=['发起机构', '项目名称'], how='outer', validate='one_to_one')
print('按照项目名称与组织合并后总数：', result.shape)
# merge with cannot match
abnormal, correct = split_index(result, result.isnull()[['慈善组织', '项目名称', '发起机构']].any(axis=1))
abnormal_partial, abnormal_master = split_index(abnormal, abnormal.isnull()['备案编号'])
result_name = pd.merge(abnormal_master, abnormal_partial, on='项目名称', how='outer')
print('匹配：', correct.shape, '未匹配', abnormal.shape, '->', '未匹配主表', abnormal_master.shape, '未匹配副表', abnormal_partial.shape)

# merge with cannot match of project name
print('仅按照项目名称匹配合并后总数：', result_name.shape)
abnormal_name, correct_name = split_index(result_name, result_name.isnull()[['慈善组织', '项目名称', '发起机构']].any(axis=1))
abnormal_name_partial, abnormal_name_master = split_index(abnormal_name, abnormal_name.isnull()['备案编号'])
result_org = pd.merge(abnormal_name_master, abnormal_name_partial, left_on='慈善组织', right_on='发起机构', how='outer')
print('匹配：', correct_name.shape, '未匹配', abnormal_name.shape, '->', '未匹配主表', abnormal_name_master.shape, '未匹配副表', abnormal_name_partial.shape)

print('仅按照组织匹配合并后总数：', result_org.shape)
abnormal_org, correct_org = split_index(result_org, result_org.isnull()[['慈善组织', '项目名称_x', '项目名称_y', '发起机构']].any(axis=1))
correct_org = result_org
print('匹配：', correct_org.shape, '未匹配', abnormal_org.shape)

correct_org.drop('项目名称_y', 1, inplace=True)
correct_org.columns = correct.columns
correct_name.columns = correct.columns
data = pd.concat([correct, correct_name, correct_org])

data[header_master] = data[header_partial]
save = data[master_table.columns]
try:
    save = save.sort_values(header_master[0], ascending=False)
except KeyError as e:
    print('!!!!!!!!!!排序失败，找不到表头：', e)
save.drop(columns='序号', inplace=True)
# save.to_excel('matched.xlsx', index=False)
save.to_excel('matched_without_cols.xlsx', index=False, header=False)
print('最终表格', save.shape, '=', [correct.shape, correct_name.shape, correct_org.shape], '最终未匹配：', abnormal_org.shape)

if len(abnormal_org):
    abnormal_org.to_excel('没对应上.xlsx', index=False)
    print('没对应上的数量', abnormal_org.shape)
