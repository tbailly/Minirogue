import curses
import random
import math
import copy

import settings as S

doors = []

class Door:
    def __init__(self,ori,x,y):
        self.ori = ori
        self.x = x
        self.y = y

def clear_door():
    y = 2
    while (y < 37):
        x = 2 
        while (x < 200):
            if (chr(S.win.inch(y, x)) == '+'):
                if (chr(S.win.inch(y + 1, x)) != '#' and chr(S.win.inch(y - 1, x)) != '#' and chr(S.win.inch(y, x + 1)) != '#' and chr(S.win.inch(y, x - 1)) != '#'):
                    if (chr(S.win.inch(y , x + 1)) == '.' or chr(S.win.inch(y, x - 1)) == '.'):
                        S.win.addch(y, x, '|')
                    else:
                        S.win.addch(y, x, '-')
            if (chr(S.win.inch(y, x)) == '#'):
                sharpi = 0
                if (chr(S.win.inch(y + 1, x)) == '#'):
                    sharpi += 1
                if (chr(S.win.inch(y - 1, x)) == '#'):
                    sharpi += 1
                if (chr(S.win.inch(y, x + 1)) == '#'):
                    sharpi += 1
                if (chr(S.win.inch(y, x - 1)) == '#'):
                    sharpi += 1
                if (chr(S.win.inch(y + 1, x)) != '+' and chr(S.win.inch(y - 1, x)) != '+' and chr(S.win.inch(y, x + 1)) != '+' and chr(S.win.inch(y, x - 1)) != '+' and sharpi == 1):
                    S.win.addch(y, x, ' ')
                elif (chr(S.win.inch(y + 1, x)) == '#' and chr(S.win.inch(y - 1, x)) == '#' and chr(S.win.inch(y, x + 1)) == '#' and chr(S.win.inch(y, x - 1)) == '#'):
                    S.win.addch(y, x, ' ')
            x += 1
        y += 1

def genway(p1, p2):
    if (p1.ori == 0):
        p1b = {'x' : p1.x - 1, 'y' : p1.y - 1}
        p1c = {'x' : p1.x, 'y' : p1.y - 1}
    if (p1.ori == 1):
        p1b = {'x' : p1.x - 1, 'y' : p1.y - 1}
        p1c = {'x' : p1.x - 1, 'y' : p1.y}
    if (p1.ori == 2):
        p1b = {'x' : p1.x - 1, 'y' : p1.y + 1}
        p1c = {'x' : p1.x, 'y' : p1.y + 1}
    if (p1.ori == 3):
        p1b = {'x' : p1.x + 1, 'y' : p1.y - 1}
        p1c = {'x' : p1.x + 1, 'y' : p1.y}

    if (p2.ori == 0):
        p2b = {'x' : p2.x - 1, 'y' : p2.y - 1}
        p2c = {'x' : p2.x, 'y' : p2.y - 1}
    if (p2.ori == 1):
        p2b = {'x' : p2.x - 1, 'y' : p2.y - 1}
        p2c = {'x' : p2.x - 1, 'y' : p2.y}
    if (p2.ori == 2):
        p2b = {'x' : p2.x - 1, 'y' : p2.y + 1}
        p2c = {'x' : p2.x, 'y' : p2.y + 1}
    if (p2.ori == 3):
        p2b = {'x' : p2.x + 1, 'y' : p2.y - 1}
        p2c = {'x' : p2.x + 1, 'y' : p2.y}
        
    tmppos = {'x' : p1c['x'], 'y' : p1c['y']}
    tabpos = []
    S.win.addstr(p1b['y'], p1b['x'], "#")
    S.win.addstr(p1c['y'], p1c['x'], "#")
    S.win.addstr(p2b['y'], p2b['x'], "#")
    S.win.addstr(p2c['y'], p2c['x'], "#")

    # While not aligned with final door, we choose randomly one of both directions available
    while (tmppos['x'] != p2b['x'] and tmppos['y'] != p2b['y']):
        diryx = math.floor(random.random() * 2)
        if (diryx == 0):
            if (tmppos['y'] - p2b['y'] > 0):
                tmppos['y'] -= 1
            elif(tmppos['y'] - p2b['y'] < 0):
                tmppos['y'] += 1
        else:
            if (tmppos['x'] - p2b['x'] > 0):
                tmppos['x'] -= 1
            elif(tmppos['x'] - p2b['x'] < 0):
                tmppos['x'] += 1
        if (chr(S.win.inch(tmppos['y'], tmppos['x'])) == ' '):
            tabpos.append(copy.copy(tmppos))
            S.win.addstr(tmppos['y'], tmppos['x'], "#")
    while (tmppos['x'] != p2b['x']):
        if (p1.x - p2b['x'] > 0):
            tmppos['x'] -= 1
        elif(p1.x - p2b['x'] < 0):
            tmppos['x'] += 1
        if ((chr(S.win.inch(tmppos['y'], tmppos['x'])) == ' ')):
            tabpos.append(copy.copy(tmppos))
            S.win.addstr(tmppos['y'], tmppos['x'], "#")
    while (tmppos['y'] != p2b['y']):
        if (p1.y - p2b['y'] > 0):
            tmppos['y'] -= 1
        elif(p1.y - p2b['y'] < 0):
            tmppos['y'] += 1
        if ((chr(S.win.inch(tmppos['y'], tmppos['x'])) == ' ')):
            tabpos.append(copy.copy(tmppos))
            S.win.addstr(tmppos['y'], tmppos['x'], "#")


def replace_door():
    while (len(doors) > 0):

        temp = Door(42, 300, 300)
        i2 = 0
        while (i2 + 1 < len(doors)):
            if ((doors[0].ori == 0) and (doors[i2].y < doors[0].y)):
                temp = temp if ((abs(doors[0].x - temp.x) + abs(doors[0].y - temp.y)) < (abs(doors[0].x - doors[i2].x) + abs(doors[0].y - doors[i2].y))) else doors[i2]
            if (doors[0].ori == 1 and doors[i2].x < doors[0].x):
                temp = temp if ((abs(doors[0].x - temp.x) + abs(doors[0].y - temp.y)) < (abs(doors[0].x - doors[i2].x) + abs(doors[0].y - doors[i2].y))) else doors[i2]
            if (doors[0].ori == 2 and doors[i2].y > doors[0].y):
                temp = temp if ((abs(doors[0].x - temp.x) + abs(doors[0].y - temp.y)) < (abs(doors[0].x - doors[i2].x) + abs(doors[0].y - doors[i2].y))) else doors[i2]
            if (doors[0].ori == 3 and doors[i2].x > doors[0].x):
                temp = temp if ((abs(doors[0].x - temp.x) + abs(doors[0].y - temp.y)) < (abs(doors[0].x - doors[i2].x) + abs(doors[0].y - doors[i2].y))) else doors[i2]
            i2 += 1

        if (temp.x != 300 and temp.y != 300):
            genway(doors[0], temp)
            i3 = 0
            while (doors[i3].x != temp.x and doors[i3].y != temp.y):
                i3 += 1
            #del doors[i3]
        del doors[0]


def gendoor(x, y, height, length, roomdone):
    door_x = random.randrange(x + 1 ,x + length - 1 )
    door_y = random.randrange(y + 1,y + height - 1)

    S.win.addch(y , door_x,'+')
    doors.append(Door(0, door_x, y))

    door_x = random.randrange(x + 1 ,x + length - 1 )
    S.win.addch(y + height , door_x,'+')
    doors.append(Door(2, door_x, y + height))

    S.win.addch(door_y , x,'+')
    doors.append(Door(1, x, door_y))

    door_y = random.randrange(y + 1, y + height - 1)
    S.win.addch(door_y , x + length,'+')
    doors.append(Door(3, x + length, door_y))


def genline(x, y, size):
    S.win.addch(y, x + size, '|')
    while (size >= 1):
        S.win.addch(y , x - 1 + size, '.')
        size -= 1
    S.win.addch(y , x  , '|')

def genroom(x, y, height, length):
    temp  = length 
    while (temp >= 0):
        S.win.addch(y + height , x + temp,'-')
        temp -= 1
    height -= 1
    while (height >= 0):
        genline(x, y + height , length)
        height -= 1
    while (length >= 0):
        S.win.addch(y, x + length,'-')
        length -= 1


def genmap():
    roomdone = 0
    maxheight = 0
    lastlength = 1
    index = random.randrange(5, 10)
    x = 0
    y = random.randrange(2, 10)
    height = random.randrange(5, 10)
    while (index != 0):
        x = (199 if (lastlength >= 199) else random.randrange(lastlength, 199))
        length = random.randrange(5, 30)
        height = random.randrange(5, 10)
        if ((x + length) > 199):
            lastlength = 1;
            y = random.randrange(maxheight + 2, maxheight + 4)
        elif ((y + height) < 37):
            genroom(x, y, height, length)
            gendoor(x, y, height, length,roomdone)
            maxheight = (maxheight if (maxheight > (y + height)) else (y + height))
            lastlength = x + length + 4
            roomdone += 1
        index -= 1
    replace_door()
    clear_door()
