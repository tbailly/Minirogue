import curses
import random
import math

import settings as S
import ft_minirogue as Main


class Monster:
    def __init__(self, pv, x, y, strength, acc, icon,ground_under):
        self.name = 'Inconnue'
        self.pv = pv
        self.pos = {'x' : x, 'y' : y}
        self.strength = strength
        self.acc = acc
        self.pos_next = {'x' : self.pos['x'], 'y' : self.pos['y']}
        self.ground_under = ground_under
        self.icon = icon
        if (icon == '♖'):
            self.name = 'Gardien'
        if (icon == '☡'):
            self.name = 'Snake'
        if (icon == '♘'):
            self.name = 'Cavalier sans tete et sans cheval'
        if (icon == '☃'):
            self.name = 'Snowman'
        if (icon == '⚧'):
            self.name = 'Ghost'
        if (icon == '♀'):
            self.name = 'Minion'
        if (icon == '☿'):
            self.name = 'Demon'
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr(icon, curses.color_pair(2))

    def fight(self, hero):
        if ((random.random() * self.acc) >= 1):
            hero.pv['current'] -= self.strength
            Main.refresh_dialog("Le " + self.name + " vous inflige " + str(self.strength) + " points de dégats", True)
            # If player have no hp left, he dies and game_over pops
            if (hero.pv['current'] <= 0):
                hero.pv['current'] = 0
                Main.game_over(hero)

    def walk(self):
        # Put back the ground where the hero was, save the next ground the hero will be on, and move the hero !
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr(self.ground_under)
        self.pos['x'] = self.pos_next['x']
        self.pos['y'] = self.pos_next['y']
        self.ground_under = chr(S.win.inch(self.pos['y'], self.pos['x']))
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr(self.icon, curses.color_pair(2))

def monsters_moves(hero, monsters):
    i = 0
    while (i < len(monsters)):
        monsters[i].pos_next['x'] = monsters[i].pos['x']
        monsters[i].pos_next['y'] = monsters[i].pos['y']
        if ((abs(hero.pos['x'] - monsters[i].pos['x']) + abs(hero.pos['y'] - monsters[i].pos['y'])) < 10):
            monster_move(hero, monsters[i])
        else:
            rand = random.random()
            if (rand > 0.75):
                monsters[i].pos_next['y'] -= 1
            elif (rand > 0.5):
                monsters[i].pos_next['y'] += 1
            elif (rand > 0.25):
                monsters[i].pos_next['x'] -= 1
            else:
                monsters[i].pos_next['x'] += 1
            front = chr(S.win.inch(monsters[i].pos_next['y'], monsters[i].pos_next['x']))
            if ((front == '*' or front == '☉' or front == '♁' or front == '.' or front == '#' or front == '+')):
                monsters[i].walk()
        i += 1

def monster_move(hero, monster):
    i = 0

    if (hero.pos['y'] + 1 < monster.pos['y']):
        monster.pos_next['y'] -= 1
    elif (hero.pos['x'] + 1 < monster.pos['x']):
        monster.pos_next['x'] -= 1
    elif (hero.pos['y'] - 1 > monster.pos['y']):
        monster.pos_next['y'] += 1
    elif (hero.pos['x'] - 1 > monster.pos['x']):
        monster.pos_next['x'] += 1
    else:
        i = 1;
        monster.fight(hero)
    if (i == 0):
        front = chr(S.win.inch(monster.pos_next['y'], monster.pos_next['x']))
        if (front == '*' or front == '☉' or front == '♁' or front == '.' or front == '#' or front == '+'):
            monster.walk()


def init_monsters():
    monsters_to_summon = 6
    max_x = 201
    max_y = 36
    tabmstr = "♖☡♘⚧☃♀☿"
    
    while (monsters_to_summon != 0):
        random_x = math.ceil(random.random() * max_x)
        random_y = math.ceil(random.random() * max_y)
        ground = chr(S.win.inch(random_y, random_x))
        while (ground != '.' and ground != '#'):
            random_x = math.ceil(random.random() * max_x)
            random_y = math.ceil(random.random() * max_y)
            ground = chr(S.win.inch(random_y, random_x))
        monsters_to_summon -= 1
        S.monsters.append(Monster(math.ceil(random.random() * 8), random_x, random_y, 1, 3 + math.ceil(random.random() * 3), tabmstr[random.randrange(0,len(tabmstr))],ground))


