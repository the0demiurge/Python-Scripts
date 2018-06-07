import curses
import locale
from curses import textpad
from math import ceil
from ast import literal_eval as loadstr


locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()


class Reigon(object):
    def __init__(self, shape, border=True):
        """Draw a reigon, with a border and can judge weather a coord in this reigon
        shape: (left up y, left up x, rigth bottom y, rigth bottom x)
        """
        assert len(shape) == 4, 'Shape must be 4-tuple'
        self.update(shape)
        if border:
            self.border = 1
        else:
            self.border = 0

    def update(self, shape):
        self.shape = shape
        self.luy, self.lux, self.rby, self.rbx = shape
        self.height, self.width = self.rby - self.luy, self.rbx-self.lux

    def is_in_window(self, y, x):
        return self.luy <= y <= self.rby and self.lux <= x <= self.rbx

    def is_in_content(self, y, x):
        return self.luy + self.border <= y <= self.rby - self.border and self.lux + self.border <= x <= self.rbx - self.border

    @staticmethod
    def coord2newwin(shape):
        luy, lux, rby, rbx = shape
        height, width = rby - luy, rbx-lux
        return height, width, luy, lux


class RectAngle(Reigon):
    def __init__(self, shape, parent_window):
        """SubWindow
        shape: (left up y, left up x, rigth bottom y, rigth bottom x)
        """
        super(RectAngle, self).__init__(shape, border=True)
        self.parent_window = parent_window
        self.draw()

    def draw(self):
        textpad.rectangne(self.parent_window, *self.coord2newwin(self.shape))


class SubWindow(Reigon):
    def __init__(self, shape, border=True):
        """SubWindow
        shape: (left up y, left up x, rigth bottom y, rigth bottom x)
        """
        super(SubWindow, self).__init__(shape, border)
        self.window = curses.newwin(*self.coord2newwin(self.shape))
        if border:
            self.window.border()

    def resize(self, shape):
        self.update(shape)


class Textbox(object):
    def __init__(self, shape, parent_window):
        self.parent_window = parent_window
        self.update(shape)
        self.border_rectangle = RectAngle(self.border_rectangle)
        self.window = curses.newwin(self.parent_window, *Reigon.coord2newwin(self.input_reigon))
        self.textbox = textpad.Textbox(self.window)

    def update(self, shape):
        self.border_reigon = shape
        self.input_reigon = (shape[0]+1, shape[1]+1, shape[2]-1, shape[3]-1)
        self.border_rectangle.update(self.border_reigon)

    def resize(self, shape):
        self.update(shape)
        # resize self.window


class ContactWindow(SubWindow):
    def __init__(self, contact_width=20, config_path=None):
        super(ContactWindow, self).__init__()

    def add_contact(self, ip, port):
        pass

    def delect_contact(self, index):
        pass

    def choose_contact(self, index):
        pass

    def save_contact(self):
        pass

    def load_contact(self):
        pass

    def refresh(self):
        pass


class MessageWindow(SubWindow):
    def __init__(self, contact_width=20, config_path=None):
        pass

    def show(self, messages, index):
        pass

    def input(self):
        pass

    def send(self):
        pass

    def scroll(self, down=True):
        pass


class ChatWindow(object):
    def __init__(self):
        self.screen = curses.initscr()
        self.contact_window = ContactWindow()
        self.message_window = MessageWindow()
        self.screen.refresh()


def handle_quit(*args, **kwargs):
    curses.endwin()
    exit()


def handle_mouse(screen, win, *args, **kwargs):
    data = curses.getmouse()
    win.window.clear()
    win.window.border()
    win.window.addstr(5, 5, str(data))
    if data[-1] == curses.BUTTON1_CLICKED:
        win.window.addstr(7, 6, str(win.is_in_window(data[1], data[2])))
        win.window.addstr(8, 6, str(win.is_in_content(data[1], data[2])))
    win.window.refresh()


def handle_resize(screen, win, *args, **kwargs):
    y, x = screen.getmaxyx()
    win.window.resize(20, 40)
    screen.clear()
    win.window.clear()
    win.window.addstr(5, 5, str((y, x)))
    win.window.border()
    screen.refresh()
    win.window.refresh()
    if y < 10 or x < 30:
        screen.clear()
        win.window.clear()
        screen.addstr(y//2-1, 0, 'Sreen Too Small!'.center(x)[:x])


handlers = {
    ord('q'): handle_quit,
    curses.KEY_MOUSE: handle_mouse,
    curses.KEY_RESIZE: handle_resize,
    curses.BUTTON1_CLICKED: None,
    curses.REPORT_MOUSE_POSITION: None,
    curses.A_BLINK: None,
}


def init():
    screen = curses.initscr()
    curses.curs_set(False)  # hide cursor
    screen.keypad(1)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)
    curses.noecho()
    win = SubWindow(shape=(0, 0, 20, 40))
    screen.refresh()
    win.window.refresh()

    # textbox = Textbox(shape=(1, 15, 38, 17), parent_window=win.window)
    return screen, win


def ui_loop():
    screen, win = init()
    while True:
        event = screen.getch()
        if event in handlers:
            handlers[event](screen=screen, win=win)


try:
    ui_loop()
except KeyboardInterrupt:
    handle_quit()
curses.endwin()


exit()
# ui
#
#
#
import curses
import locale
from curses import textpad
from math import ceil

locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

msgs = list()
stdscr = curses.initscr()
# curses.noecho()
curses.cbreak()

len_contact = 20
contacts = curses.newwin(curses.LINES, len_contact, 0, 0)
messages = curses.newwin(curses.LINES, curses.COLS - len_contact, 0, len_contact)


attrs = {'curses.A_BLINK': curses.A_BLINK,
         'curses.A_BOLD': curses.A_BOLD,
         'curses.A_DIM': curses.A_DIM,
         'curses.A_REVERSE': curses.A_REVERSE,
         'curses.A_STANDOUT': curses.A_STANDOUT,
         'curses.A_UNDERLINE': curses.A_UNDERLINE, }
for i, attr in enumerate(attrs):
    contacts.addstr(i+2, 1, attr, attrs[attr])
contacts.addstr(1, 1, '测试')
contacts.border()
messages.border()
textpad.rectangle(messages, curses.LINES-4, 1, curses.LINES-2, curses.COLS-len_contact-2)
stdscr.refresh()
contacts.refresh()
messages.refresh()
try:
    for index in range(100):
        msglen = curses.COLS-len_contact-4
        msgheight = curses.LINES - 5
        data = messages.getstr(curses.LINES - 3, 2, msglen).decode('utf-8')
        data = [['> ', '  '][i != 0] + data[msglen * i:msglen*(i+1)] for i in range(ceil(len(data)/msglen))]
        msgs.extend(data)

        for j, info in zip(range(msgheight), msgs[-(msgheight):]):
            messages.addstr(j+1, 1, ' ' * (curses.COLS - len_contact - 2))
            messages.addstr(j+1, 1, info)

        messages.addstr(curses.LINES-3, 2, ' ' * msglen)
        messages.border()
        contacts.border()
        textpad.rectangle(messages, curses.LINES-4, 1, curses.LINES-2, curses.COLS-len_contact-2)
        messages.refresh()
        contacts.refresh()
        messages.getch()
        curses.getmouse()
except KeyboardInterrupt:
    curses.endwin()
# window resize
#
#
#
import curses
from curses import textpad


screen = curses.initscr()
curses.noecho()
# curses.cbreak()
screen.keypad(1)
subwin = curses.newwin(25, 25, 1, 10)
subwin2 = curses.newwin(25, 25, 1, 10+25)
# screen.getch()
# curses.endwin()
# for ki in dir(subwin):
#     print(ki, getattr(subwin, ki), sep='\t')
# exit()
# subwin.border()
# subwin2.border()
screen.refresh()
subwin.refresh()
subwin2.refresh()
box = textpad.Textbox(subwin, insert_mode=True)
while True:
    y, x = screen.getmaxyx()
    resize = curses.is_term_resized(y, x)
    key = screen.getch()
    if key == ord('q'):
        break

    elif key == ord('i'):
        string = box.edit()
        subwin2.addstr(0, 0, str(string))
        subwin.refresh()


curses.endwin()
