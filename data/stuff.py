import tcod

from random import randint

from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.item import Item

from game_messages import Message

from item_functions import (cast_confuse,
                            cast_fireball,
                            cast_lightning,
                            heal)


class ItemBase:
    chances = 0
    is_consumable = False
    is_equippable = False

    def __init__(self, name, character, color):
        self.name = name
        self.character = character
        self.color = color


class Consumable(ItemBase):
    is_consumable = True

    def __init__(self, name, character, color, item_component):
        ItemBase.__init__(self, name, character, color)
        self.item_component = item_component


class Scroll(Consumable):

    def __init__(self, name, color, item_component):
        Consumable.__init__(self, name, '#', color, item_component)


class Potion(Consumable):

    def __init__(self, name, color, item_component):
        Consumable.__init__(self, name, '!', color, item_component)


class Equipment(ItemBase):
    is_equippable = True

    def __init__(self, name, character, color, equippable_component):
        ItemBase.__init__(self, name, character, color)
        self.equippable_component = equippable_component


class HealingPotion(Potion):
    chances = 35

    def __init__(self):
        amount = randint(30, 40)
        Potion.__init__(
            self,
            'Healing Potion',
            tcod.violet,
            Item(use_function=heal, amount=amount))


class LightningBoltScroll(Scroll):
    chances = [[25, 4]]

    def __init__(self):
        damage = randint(10, 50)
        Scroll.__init__(
            self,
            'Lightning Bolt Scroll',
            tcod.yellow,
            Item(use_function=cast_lightning,
                 damage=damage, maximum_range=5))


class FireballScroll(Scroll):
    chances = [[25, 6]]

    def __init__(self):
        text = ('Left-click a target tile for the fireball,'
                ' or right-click to cancel.')
        damage = randint(20, 25)
        Scroll.__init__(
            self,
            'Fireball Scroll',
            tcod.red,
            Item(use_function=cast_fireball,
                 targeting=True,
                 targeting_message=Message(text, tcod.light_cyan),
                 damage=damage, radius=3))


class ConfusionScroll(Scroll):
    chances = [[10, 2]]

    def __init__(self):

        text = ('Left-click an enemy to confuse it,'
                ' or right-click to cancel.')
        Scroll.__init__(
            self,
            'Confusion Scroll',
            tcod.light_pink,
            Item(use_function=cast_confuse,
                 targeting=True,
                 targeting_message=Message(text, tcod.light_cyan),
                 number_of_turns=10))


class Dagger(Equipment):

    def __init__(self):
        Equipment.__init__(
            self,
            'Dagger',
            '_',
            tcod.sky,
            Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2))


class Sword(Equipment):
    chances = [[5, 4]]

    def __init__(self):
        Equipment.__init__(
            self,
            'Sword',
            '/',
            tcod.sky,
            Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4))


class Shield(Equipment):
    chances = [[15, 8]]

    def __init__(self):
        Equipment.__init__(
            self,
            'Shield',
            '[',
            tcod.darker_orange,
            Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1))


ITEMS = [
    # Potions
    HealingPotion,

    # Scrolls
    LightningBoltScroll,
    FireballScroll,
    ConfusionScroll,

    # Equipment
    Sword,
    Shield
]
