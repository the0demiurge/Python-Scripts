import pandas as pd
import math

master_table_name = '0210-1200公益宝为湖北、武汉等地区防控新型冠状病毒感染的肺炎募捐情况统计表（内部）.xlsx'
partial_table_name = '总20200210124559740.xls'

master_table = pd.read_excel(master_table_name, convert_float=False, sheet_name=None, skiprows=1, parse_dates=True).popitem()[-1].applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x).dropna(subset=['序号'])
partial_table = pd.read_excel(partial_table_name, convert_float=False, sheet_name=None, skiprows=1).popitem()[-1].applymap(lambda x: x.replace('  ', ' ') if type(x) == str else x).drop(['发起机构.1', '项目名称.1', '发起机构.2', '项目名称.2'], 1)


def drop_na_cols(table):
    table = table.dropna(axis=1, thresh=math.ceil(len(table) / 2))
    return table


def split_index(table, index):
    positive = table[index].dropna(axis=1, how='all')
    negative = table[index.apply(lambda x: not x)].dropna(axis=1, how='all')
    return positive, negative


master_table = drop_na_cols(master_table)
partial_table = drop_na_cols(partial_table)
# merge
result = pd.merge(left=master_table, right=partial_table, left_on=['慈善组织', '项目名称'], right_on=['发起机构', '项目名称'], how='outer', validate='one_to_one')
# merge with cannot match
abnormal, correct = split_index(result, result.isnull()[['慈善组织', '项目名称', '发起机构']].any(axis=1))
abnormal_partial, abnormal_master = split_index(abnormal, abnormal.isnull()['序号'])
result_name = pd.merge(abnormal_master, abnormal_partial, on='项目名称', how='outer')

# merge with cannot match of project name
abnormal_name, correct_name = split_index(result_name, result_name.isnull()[['慈善组织', '项目名称', '发起机构']].any(axis=1))
abnormal_name_partial, abnormal_name_master = split_index(abnormal_name, abnormal_name.isnull()['序号'])
result_org = pd.merge(abnormal_name_master, abnormal_name_partial, left_on='慈善组织', right_on='发起机构', how='outer')

abnormal_org, correct_org = split_index(result_org, result_org.isnull()[['慈善组织', '项目名称_x', '项目名称_y', '发起机构']].any(axis=1))
correct_org.drop('项目名称_y', 1, inplace=True)
correct_org.columns = correct.columns
correct_name.columns = correct.columns

data = pd.concat([correct, correct_name, correct_org])

data[['已筹金额（元）', '参与捐赠人次（人次）', '已筹金额（元）\n含线下', "参与捐赠人次（人次）\n含线下"]] = data[['筹款量', '捐赠次数', '筹款量.1', '捐赠次数.1', ]]
save = data[master_table.columns]
data2 = data[['筹款量.2', '捐赠次数.2', ]]
data2.columns = ['已筹金额（元）\\n线上', '参与捐赠人次（人次）\\n线上']
save = pd.concat((save, data2), axis=1)
save = save[['序号',
             '备案编号',
             '慈善组织',
             '合作方',
             '项目名称',
             '起始时间',
             '募捐目的',
             '资金还是物资',
             '目标金额（元）',
             '已筹金额（元）',
             '参与捐赠人次（人次）',
             '已筹金额（元）\n含线下',
             '参与捐赠人次（人次）\n含线下',
             '已筹金额（元）\\n线上',
             '参与捐赠人次（人次）\\n线上',
             '募捐状态',
             '筹款链接',
             ]]
save.sort_values('已筹金额（元）', ascending=False).to_excel('总表.xlsx', index=False)
abnormal_org.to_excel('没对应上.xlsx', index=False)
