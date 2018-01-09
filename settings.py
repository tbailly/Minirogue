import curses



def init():
        global monsters
        global win
        global win_ui
        global win_dialog
        win = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        win.keypad(True)
        win_ui = curses.newwin(1+3+1, 1+199+1, 38, 1)
        win_dialog = curses.newwin(1+7+1, 1+199+1, 43, 1)
        monsters = []
        global dialogs
        dialogs = "aaa"
        curses.init_pair(1, 14, 0)
        curses.init_pair(2, 9, 0)
        curses.init_pair(3, 11, 0)
        curses.init_pair(4, 12, 0)
        curses.init_pair(5, 13, 0)
        curses.init_pair(6, 14, 0)

