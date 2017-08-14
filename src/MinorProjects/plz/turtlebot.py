
# coding: utf-8

# In[14]:


import sys
import os
import turtle
t = turtle.Pen()


# In[18]:


# turtle bot 模拟器
# 只有三种动作，前进、左转、右转，转弯半径恒定为 r， 前进距离恒定为 l
r = 15 # 转弯半径
rl = 5 # 转弯时走的路程
l = 5 # 前进时走的路程


# In[16]:


# 画盒子
ld = (5, 5)
ru = (205, 205)
# 开始画
t.color("")
t.goto(ld)
t.color("grey")
t.pensize(4)
t.goto(ld[0], ru[1])
t.goto(*ru)
t.goto(ru[0], ld[1])
t.goto(*ld)


# In[11]:


def left():
    t.circle(r, rl)
def right():
    t.circle(-r, rl)
def forward():
    t.forward(l)
def undo():
    t.undo()
def save(name='turtle.eps'):
    t.color("")
    t.goto(-500, -500)
    ts = turtle.getscreen()
    ts.getcanvas().postscript(file=name)
def reset():
    t.color("")
    t.goto(0,0)
    t.color("black")
    t.pensize(1)
    t.seth(0)
def pensize(s=None):
    try:
        if s is None:
            s = input('pen size（输入数字）:')
            print(s, file=open(path, 'a'))
        t.pensize(float(s))
    except:
        print('画笔粗细输入错误')
def color(c=None):
    try:
        if c is None:
            c = input('color(什么都不写的话颜色为透明，其他颜色用英文即可):')
            print(c, file=open(path, 'a'))
        t.color(c)
    except:
        print('颜色错误')
def show_help():
    help_info = '''用法：
    支持解析脚本（直接把动作写到文本文档里即可）：python turtle.py <file>
    
    机器人运动指令：
    w
   asd 分别为方向键，前后左右；
    
    r：reset,           回到原来位置
    g：go to,           指定的坐标位置，颜色什么的全部重置
    z：set heading      设置头部朝向
    l：draw line        从当前位置到指定坐标画一条线
    
    属性设置指令：
    t：set turtle bot,  设置运动半径和距离
    c：color,           改变颜色
    p：pen size,        改变画笔粗细
    
    其他：
    o：save,            保存图片
    q：quit,            退出
    h：help,            显示帮助'''
    print(help_info)
    print("方格坐标为左下角",ld, "右上角", ru)
def goto(position=None):
    try:
        t.color("")
        if not position:
            position = input("请输入坐标，横纵坐标用空格分隔：")
            print(position, file=open(path, 'a'))
        position = [int(i) for i in position.split()]
        t.goto(*position)
        t.color("black")
        t.pensize(1)
    except:
        print('坐标输入错误！')
def draw_line(position=None):
    try:
        if not position:
            position = input("请输入坐标，横纵坐标用空格分隔：")
            print(position, file=open(path, 'a'))
        position = [int(i) for i in position.split()]
        t.goto(*position)
    except:
        print('坐标输入错误！')
def set_turtle(s=None):
    global r
    global l
    try:
        t.color("")
        if not s:
            s = input("请输入半径和直线距离，用空格分隔：")
            print(s, file=open(path, 'a'))
        s = [float(i) for i in s.split()]
        [r, l] = s
    except:
        print('r\\l输入错误！')
def set_heading(s=None):
    try:
        if not s:
            s = input("请输入头部的角度：")
            print(s, file=open(path, 'a'))
        s = float(s)
        t.seth(s)
    except:
        print('r\\l输入错误！')
def nop():
    pass
        
act = {
    'w': forward,
    's': undo,
    'r': reset,
    'a': left,
    'd': right,
    'c': color,
    'p': pensize,
    'o': save,
    'q': exit,
    'l': draw_line,
    'h': show_help,
    'g': goto,
    't': set_turtle,
    'z': set_heading,
    '------': nop,
}
reset()
path = ''


# In[12]:


# 如果输入脚本则读取脚本
read_data = False
if len(sys.argv) > 1:
    path = sys.argv[1]
    data = open(sys.argv[1]).readlines()
    for i, line in enumerate(data):
        try:
            if read_data:
                read_data = False
                act[data[i-1].strip()](line.strip())
            elif line.strip() in list('gcptlz'):
                read_data = True
            else:
                act[line.strip()]()
        except:
            print('输入错误', line, i)


# In[57]:


act['h']()
warns = 'yes'

if not path:
    print('输入历史自动保存，成为脚本')
    path = input('请输入脚本文件名：')
    if os.path.exists(path):
        warns = input('警告！该文件已存在！继续将在该文件之后append内容！继续请输入“yes”')
else:
    print("可以继续输入指令，输入的指令将继续保存在该文件，与之前的内容使用分隔线分隔")
        
if warns == 'yes':
    print('------', file=open(path, 'a'))
    while True:
        print("当前坐标：", t.pos(), "角度", t.heading())
        info = input("turtlebot>")
        print(info, file=open(path, 'a'))
        try:
            act[info]()
        except:
            print('输入错误！')
            act['h']()
    

