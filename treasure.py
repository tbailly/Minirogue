import curses
import random
import settings as S
import math

def init_treasure():
    max_x = 201
    max_y = 36
    tab = '*☉♁⚔'
    treasure_to_summon = random.randrange(4,10) 
    while (treasure_to_summon != 0):
        random_x = math.ceil(random.random() * max_x)
        random_y = math.ceil(random.random() * max_y)
        while (chr(S.win.inch(random_y, random_x)) != '.'):
            random_x = math.ceil(random.random() * max_x)
            random_y = math.ceil(random.random() * max_y)
        treasure_to_summon -= 1
        randomitem = random.randrange(0,len(tab))
        S.win.addch(random_y,random_x,tab[randomitem])

def init_exit():
    max_x = 201
    max_y = 36

    random_x = math.ceil(random.random() * max_x)
    random_y = math.ceil(random.random() * max_y)
    while (chr(S.win.inch(random_y, random_x)) != '.'):
        random_x = math.ceil(random.random() * max_x)
        random_y = math.ceil(random.random() * max_y)
    S.win.addch(random_y,random_x,'☷')

