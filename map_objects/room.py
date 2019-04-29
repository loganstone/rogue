from random import randint

from entity import Entity
from data.creature import MONSTERS
from data.stuff import ITEMS

from random_utils import random_choice_from_class_list
from render_functions import RenderOrder


class Rect:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return self.x1 <= other.x2 \
            and self.x2 >= other.x1 \
            and self.y1 <= other.y2 \
            and self.y2 >= other.y1


class Room(Rect):

    def __init__(self, dungeon_level, x, y, w, h):
        Rect.__init__(self, x, y, w, h)
        self.dungeon_level = dungeon_level

    def placement_monsters(self, number_of_monsters, entities):

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(self.x1 + 1, self.x2 - 1)
            y = randint(self.y1 + 1, self.y2 - 1)

            if not any([entity for entity in entities
                        if entity.x == x and entity.y == y]):
                monster = random_choice_from_class_list(
                    MONSTERS, self.dungeon_level)
                entities.append(
                    Entity(x, y,
                           monster.character,
                           monster.color,
                           monster.name, blocks=True,
                           render_order=RenderOrder.ACTOR,
                           fighter=monster.fighter,
                           ai=monster.ai_component))

    def placement_items(self, number_of_items, entities):

        for i in range(number_of_items):
            x = randint(self.x1 + 1, self.x2 - 1)
            y = randint(self.y1 + 1, self.y2 - 1)

            if not any([entity for entity in entities
                        if entity.x == x and entity.y == y]):

                item = random_choice_from_class_list(
                    ITEMS, self.dungeon_level)

                if item.is_consumable:
                    entities.append(
                        Entity(x, y,
                               item.character,
                               item.color,
                               item.name,
                               render_order=RenderOrder.ITEM,
                               item=item.item_component))

                if item.is_equippable:
                    entities.append(
                        Entity(x, y,
                               item.character,
                               item.color,
                               item.name,
                               equippable=item.equippable_component))
