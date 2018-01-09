import curses
import random
import math

import settings as S
import ft_minirogue as Main

class Hero:
    def __init__(self):
        max_x = 201
        max_y = 36
        random_x = math.ceil(random.random() * max_x)
        random_y = math.ceil(random.random() * max_y)
        while (chr(S.win.inch(random_y, random_x)) != '.'):
            random_x = math.ceil(random.random() * max_x)
            random_y = math.ceil(random.random() * max_y)
        self.pv = {'current' : 30, 'max' : 30}
        self.gold = 0
        self.pos = {'x' : random_x, 'y' : random_y}
        self.pos_next = {'x' : random_x, 'y' : random_y}
        self.armor = 5
        self.strength = 5
        self.acc = 5
        self.ground_under = '.'
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr('☺', curses.color_pair(1))
    
    def walk(self):
        # Put back the ground where the hero was, save the next ground the hero will be on, and move the hero !
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr(self.ground_under)
        self.pos['x'] = self.pos_next['x']
        self.pos['y'] = self.pos_next['y']
        self.ground_under = chr(S.win.inch(self.pos['y'], self.pos['x']))
        S.win.move(self.pos['y'], self.pos['x'])
        S.win.addstr('☺', curses.color_pair(1))

    def fight(self, monsters):
        i = 0;
        # Find the right monster in monsters to fight against
        while ((monsters[i].pos['x'] != self.pos_next['x']) and (monsters[i].pos['y'] != self.pos_next['y'])):
            i += 1
            # TODO On calcule vraiment comme ça l'accuracy ? Et pas de résistance/armor pour les monstres ?
        if ((random.random() * self.acc) >= 1):
            monsters[i].pv -= self.strength
            Main.refresh_dialog("Vous frappez un joli coup sur le " + monsters[i].name + " et il perd " + str(self.strength) + " PV", False)
            # Kills the monster if it has no pv left. It won't be able to retaliate
            if (monsters[i].pv <= 0):
                Main.refresh_dialog("Le " + monsters[i].name + " est vaincu ! ", True)
                S.win.addstr(monsters[i].pos['y'], monsters[i].pos['x'], monsters[i].ground_under)
                del(monsters[i])
        else:
            Main.refresh_dialog("Vous manquez de peu le " + monsters[i].name, False)

    def find_treasure(self, icon):
        if (icon == '*'):
            self.gold += 50
            Main.refresh_dialog("Vous récoltez 50 d'or", False)

        if (icon == '♁'):
            self.pv['current'] += 5;
            if (self.pv['current'] >= self.pv['max']):
                self.pv['current'] = self.pv['max']
            Main.refresh_dialog("Vous récupérez une potion et la buvez instantanément : vous regagnez 5 points de vie", False)
        if (icon == '☉'):
            self.armor += 2
            Main.refresh_dialog("Vous trouvez une armure de cuir mal en point : vous gagnez 2 points d'armure", False)
        if (icon == '⚔'):
            self.strength += 2
            Main.refresh_dialog("Cette arme tranchante vous permettra de vous défaire plus rapidement de vos ennemis : vous gagnez 2 de force", False)
        self.ground_under = '.'


def hero_move(hero, monsters, key):
    hero.pos_next['x'] = hero.pos['x']
    hero.pos_next['y'] = hero.pos['y']
    if (key == curses.KEY_LEFT):
        hero.pos_next['x'] -= 1
    if (key == curses.KEY_UP):
        hero.pos_next['y'] -= 1
    if (key == curses.KEY_RIGHT):
        hero.pos_next['x'] += 1
    if (key == curses.KEY_DOWN):
        hero.pos_next['y'] += 1
    if (key == 46 and hero.ground_under == '☷') :
        Main.create_new_lvl(hero)
    front = chr(S.win.inch(hero.pos_next['y'], hero.pos_next['x']))
    #if (chr(S.win.inch(hero.pos_next['x'], hero.pos_next['y'])) != '-' and
    #        chr(S.win.inch(hero.pos_next['x'], hero.pos_next['y'])) != '|' and
    #        chr(S.win.inch(hero.pos_next['x'], hero.pos_next['y'])) != 'B' and
    #        chr(S.win.inch(hero.pos_next['x'], hero.pos_next['y'])) != 'K'):
    if (front == '☷' or front == '.' or front == '#' or front == '+'):
        hero.walk()
    elif (front == '♖' or front == '☡' or front == '♘' or front == '⚧' or front == '☃' or front == '♀' or front == '☿'):
        hero.fight(monsters)
    elif (front == '*' or front == '☉' or front == '♁' or front == '⚔'):
        hero.walk()
        hero.find_treasure(front)
    

