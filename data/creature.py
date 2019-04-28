import tcod

from components.ai import BasicMonster
from components.fighter import Fighter


class Monster:
    chances = 0

    def __init__(self, name, character, color, fighter, ai_component):
        self.name = name
        self.character = character
        self.color = color
        self.fighter = fighter
        self.ai_component = ai_component


class Orc(Monster):
    chances = 80

    def __init__(self):
        Monster.__init__(
            self,
            self.__class__.__name__,
            'o',
            tcod.desaturated_green,
            Fighter(hp=20, defense=0, power=4, xp=35),
            BasicMonster())


class Troll(Monster):
    chances = [[15, 3], [30, 5], [60, 7]]

    def __init__(self):
        Monster.__init__(
            self,
            self.__class__.__name__,
            'T',
            tcod.darker_green,
            Fighter(hp=30, defense=2, power=8, xp=100),
            BasicMonster())


MONSTERS = [Orc, Troll]
