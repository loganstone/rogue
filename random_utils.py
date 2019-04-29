from random import randint


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value
    return 0


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]


def random_choice_from_class_list(class_list, dungeon_level):
    chances = []
    choices = []
    for class_ in class_list:
        if isinstance(class_.chances, list):
            chances.append(from_dungeon_level(class_.chances, dungeon_level))
        else:
            chances.append(class_.chances)
        choices.append(class_())

    return choices[random_choice_index(chances)]
