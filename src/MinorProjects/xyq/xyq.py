#!/usr/bin/env python3
import os


def run(cmd, check=True):
    print('$', cmd)
    status = os.system(cmd)
    if check and status != 0:
        print('命令出错：', status)
        exit()


print('请选择操作：\n\t[1] 将镜像文件写入存储卡（危险操作）\n\t[2] 从存储卡制作镜像')
method = input('请输入操作标号 [1/2]：')
if method not in {'1', '2'}:
    print('输入错误')
    exit()

input('不插任何U盘或存储卡，准备好后按回车，将显示所有设备')

run('lsblk')
input('插入U盘或存储卡，准备好后按回车，将显示所有设备')
run('lsblk')

sd = input('输入多出来的设备标号名称，比如“sda”：')

file = input('输入镜像文件名：')

if method == '1':
    input('\n警告：将会把数据写入到 /dev/{} ，会将设备原来的数据全部删除。\n继续按回车，取消按Ctrl+C'.format(sd))
    if not os.path.exists(file):
        print('该文件不存在：', file, '，操作取消')
        exit()
    run('sudo umount /dev/{}*'.format(sd), False)
    run('sudo dd if="{file}" of=/dev/{sd}'.format(file=file, sd=sd))
elif method == '2':
    if os.path.exists(file):
        print(file, '已存在，操作取消')
        exit()
    run('sudo umount /dev/{}*'.format(sd), False)
    run('sudo dd if=/dev/{sd} of="{file}"'.format(file=file, sd=sd))

print('成功')

