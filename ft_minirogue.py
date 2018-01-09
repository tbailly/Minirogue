import curses
import random
import math
import copy
from curses.textpad import Textbox, rectangle

import settings as S
import genmap
import Monster
import treasure
import Hero


# COMMANDS TO RESIZE TERMINAL (but not iterm)
# from term import opentty, cbreakmode

# with opentty() as tty:
#     if tty is not None:
#         with cbreakmode(tty, min=0):
#             print('\033[8;50;202t');
#curses.resizeterm(50, 50)

# All the windows are global
S.init()

def main():
    S.win.clear()
    
    # GENERATE MAP AND EDGES
    curses.textpad.rectangle(S.win, 0,0, 1+50+1, 1+200+1)  
    S.win.refresh()
    #while (True):
     #   test = S.win.getch()
      #  S.win.addstr(42,42,str(test))
    # TEST FOR WAY
    genmap.genmap()
    treasure.init_exit()
    # SUMMON HERO AND MONSTERS
    hero = Hero.Hero()
    Monster.init_monsters()
    treasure.init_treasure()
    # GENERATE UI
    refresh_ui(hero)

    # GENERATE DIALOG BOX
    refresh_dialog("", False)

    # Main Game Loop
    running = True
    while (running):
        S.win.move(0, 0)
        key = S.win.getch()
        refresh_dialog("", False)

        if (key == 27):
            running = False
        Hero.hero_move(hero, S.monsters, key)
        Monster.monsters_moves(hero, S.monsters)
        refresh_ui(hero)
        S.win.move(0, 0)

def refresh_ui(hero):
    infos = "GOLDS : " + str(hero.gold) + "     ARMOR : " + str(hero.armor) + "     HEALTH : " + str(hero.pv['current']) + " (" + str(hero.pv['max']) + ")     STRENGTH : " + str(hero.strength)
    S.win_ui.clear()
    S.win_ui.border('|', '|', '-', '-', '+', '+', '+', '+')
    S.win_ui.move(math.ceil(S.win_ui.getmaxyx()[0] / 2) - 1, math.ceil(S.win_ui.getmaxyx()[1] / 2 - len(infos) / 2))
    S.win_ui.addstr(infos)
    S.win_ui.refresh()

def refresh_dialog(message, append):
    S.win_dialog.clear()
    S.win_dialog.border('|', '|', '-', '-', '+', '+', '+', '+')
    if (append == True):
        S.dialogs += "\n" + message
    else:
        S.dialogs = message
    if (len(S.dialogs) <= 197):
        S.win_dialog.move(math.ceil(S.win_dialog.getmaxyx()[0] / 2) - 1, math.ceil(S.win_dialog.getmaxyx()[1] / 2 - len(S.dialogs) / 2))
        S.win_dialog.addstr(S.dialogs)
    else:
        i = 0;
        while (len(S.dialogs) > 197):
            S.win_dialog.addstr(2 + i, 2, S.dialogs[0:196])
            S.dialogs = S.dialogs[196:len(S.dialogs)]
            i += 1;
        S.win_dialog.addstr(2 + i, math.ceil(S.win_dialog.getmaxyx()[1] / 2 - len(S.dialogs) / 2), S.dialogs)
    S.win_dialog.refresh()

def game_over(hero):
    refresh_ui(hero)
    del hero
    while (len(S.monsters) > 0):
        del S.monsters[0]
    win_go = curses.newwin(1+5+1, 1+74+1, 21, 62)
    win_go.addstr(" _______  _______  __   __  _______    _______  __   __  _______  ______   \n|       ||   _   ||  |_|  ||       |  |       ||  | |  ||       ||    _ |  \n|    ___||  |_|  ||       ||    ___|  |   _   ||  |_|  ||    ___||   | ||  \n|   | __ |       ||       ||   |___   |  | |  ||       ||   |___ |   |_||_ \n|   ||  ||       ||       ||    ___|  |  |_|  ||       ||    ___||    __  |\n|   |_| ||   _   || ||_|| ||   |___   |       | |     | |   |___ |   |  | |\n|_______||__| |__||_|   |_||_______|  |_______|  |___|  |_______||___|  |_|")
    win_go.refresh()

    # Game Over Loop
    running = True
    while (running):
        key = S.win.getch()

        if (key == 27):
            curses.nocbreak(); S.win.keypad(0); curses.echo()
            curses.endwin()
            running = False
        if (key == 97):
            main()

def create_new_lvl(hero):
    max_x = 201
    max_y = 36
    while (len(S.monsters) > 0):
        del S.monsters[0]
    S.win.clear()
    curses.textpad.rectangle(S.win, 0,0, 1+50+1, 1+200+1)  
    genmap.genmap()
    treasure.init_exit()
    treasure.init_treasure()
    Monster.init_monsters()
    refresh_ui(hero)
    refresh_dialog("", False)
    random_x = math.ceil(random.random() * max_x)
    random_y = math.ceil(random.random() * max_y)
    ground = chr(S.win.inch(random_y, random_x))
    while (ground != '.' and ground != '#'):
        random_x = math.ceil(random.random() * max_x)
        random_y = math.ceil(random.random() * max_y)
        ground = chr(S.win.inch(random_y, random_x))
    hero.pos['x'] = random_x
    hero.pos['y'] = random_y
    hero.ground_under = ground
    S.win.move(hero.pos['y'], hero.pos['x'])
    S.win.addstr('☺')
    S.win.refresh()



if __name__ == '__main__':
	main()
