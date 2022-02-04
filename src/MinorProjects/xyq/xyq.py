#!/usr/bin/env python3
import os
import subprocess
from ast import literal_eval


def run(cmd, check=True):
    print('$', cmd)
    # return
    status = os.system(cmd)
    if check and status != 0:
        print('命令出错：', status)
        exit()


def get_info(info='TYPE'):
    data = subprocess.check_output(['lsblk', '-o', f'PATH,{info}']).decode().strip().split('\n')
    result = dict()
    for line in data[1:]:
        k, v, *_ = line.split(' ', 1) + ['']
        result[k.strip()] = v.strip()
    return result


def get_all_info():
    result = dict()
    for info in 'TYPE,PATH,FSTYPE,FSSIZE,FSUSED,FSUSE%,HOTPLUG,MODEL,SIZE,STATE'.split(','):
        result[info] = get_info(info)
    return result


result = get_all_info()


def show_dev_info(dev):
    return f"{dev}\t{result['MODEL'][dev]}\t{result['SIZE'][dev]}"


def select_disk(message='输入选择的存储卡：'):
    global result
    result = get_all_info()
    disks = sorted({k for k, v in result['TYPE'].items() if v == 'disk' and result['HOTPLUG'][k] == '1'})
    if len(disks) == 1:
        return disks[0]
    elif len(disks) == 0:
        print("没有找到内存卡或u盘设备")
        exit()
        return None
    else:
        while True:
            for i, p in enumerate(disks):
                print(f"[{i}]: \t{show_dev_info(p)}")
            n = (input(message).strip())
            try:
                n = literal_eval(n)
            except SyntaxError:
                pass
            if isinstance(n, int) and 0 <= n < len(disks):
                return disks[n]
            elif isinstance(n, str) and n in disks:
                return n


print('请选择操作：\n\t[1] 从存储卡制作镜像\n\t[2] 将镜像文件写入存储卡（危险操作）\n\t[3] 将数据从来源存储卡复制到目标存储卡（危险操作）')
method = input('请输入操作标号 [1/2/3]：')
if method not in {'1', '2', '3'}:
    print('输入错误')
    exit()

input('插入U盘或存储卡，准备好后按回车')

if method == '1':
    sd = select_disk('选择来源存储卡：')
    print(f'选择了设备：{show_dev_info(sd)}')
    file = input('输入镜像文件名：')
    if file.strip().startswith('/dev'):
        print("镜像文件不能是设备")
        exit()
    if os.path.exists(file):
        print(file, '已存在，操作取消')
        exit()
    run(f'sudo umount {sd}*', False)
    run(f'sudo dd if={sd} of="{file}"')
elif method == '2':
    sd = select_disk('选择目标存储卡：')
    print(f'选择了设备：{show_dev_info(sd)}')
    file = input('输入镜像文件名：')
    if file.strip().startswith('/dev'):
        print("镜像文件不能是设备")
        exit()
    prompt = input(f'\n警告：将会把数据从{file}写入到 {sd} ，会将设备原来的数据全部删除。\n继续输入"yes"后按回车，取消按回车：')
    if not os.path.exists(file):
        print('该文件不存在：', file, '，操作取消')
        exit()
    if prompt != 'yes':
        print("操作取消")
        exit()
    run(f'sudo umount {sd}*', False)
    run(f'sudo dd if="{file}" of={sd}')
elif method == '3':
    sd_from = select_disk("选择来源内存卡：")
    print(f'选择了来源设备：{show_dev_info(sd_from)}')
    sd_to = select_disk("选择目标存储卡：")
    print(f'选择了目标设备：{show_dev_info(sd_to)}')
    if sd_from == sd_to:
        print(f"来源设备{sd_from}不能与目标设备{sd_to}相同")
        exit()
    prompt = input(f'\n警告：将会把数据从{sd_from}写入到 {sd_to} ，会将设备原来的数据全部删除。\n继续输入"yes"后按回车，取消按回车：')
    if prompt != 'yes':
        print("操作取消")
        exit()
    run(f'sudo umount {sd_from}*', False)
    run(f'sudo umount {sd_to}*', False)
    run(f'sudo dd if={sd_from} of={sd_to}')

print('成功')
