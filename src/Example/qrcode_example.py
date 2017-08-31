#!/usr/bin/env python
import qrcode

data = input('请输入需要转换成二维码的文字：')

# 生成二维码信息
qr = qrcode.QRCode()
qr.add_data(data)

# 选择显示二维码的方式
show = {
    '1': qr.make_image().show,
    '2': qr.print_ascii,
    '3': qr.print_tty,
}
while True:
    try:
        way = input('''\n二维码输出格式有：
        1: 图片
        2: ascii
        3: tty\n请选择二维码输出格式(按Ctrl+D退出)：''')
        if way in show:
            show[way]()
    except (EOFError, KeyboardInterrupt):
        print('作者的对象：小胖儿')
        exit(0)

