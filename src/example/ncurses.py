from os import system
import curses

myscreen = curses.initscr()
times=10

myscreen.border(0)
myscreen.addstr(12, 15, '测试')
myscreen.refresh()
inputs = []
for i in range(times):
    myscreen.border(0)
    myscreen.addstr(20, 20, '%d/%d'%(i+1, times))
    myscreen.refresh()
    inputs.append(myscreen.getstr(13,15,60))
    myscreen.clear()
    for index, ins in enumerate(inputs[::-1]):
        myscreen.addstr(12-index, 15, ins)
    myscreen.refresh()
myscreen.getch()
curses.endwin()
