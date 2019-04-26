import tcod

from components.ai import ConfusedMonster

from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message(
            'You are already at full health', tcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message(
            'Your wounds start to feel better!', tcod.green)})

    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter \
                and entity != caster \
                and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        text = ('A lighting bolt strikes the {0} '
                'with a loud thunder! The damage is {1}') \
            .format(target.name, damage)
        results.append({'consumed': True, 'target': target,
                        'message': Message(text)})
        results.extend(target.fighter.take_damage(damage))
    else:
        text = 'No enemy is close enough to strike.'
        results.append({'consumed': False, 'target': None,
                        'message': Message(text, tcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        text = 'You cannot target a tile outside your field of view.'
        results.append(
            {'consumed': False, 'message': Message(text, tcod.yellow)})
        return results

    text = ('The fireball explodes,'
            ' burning everything within {0} tiles!').format(radius)
    results.append(
        {'consumed': True, 'message': Message(text, tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            text = 'The {0} gets burned for {1} hit points.'.format(
                entity.name, damage)
            results.append({'message': Message(text, tcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        text = 'You cannot target a tile outside your field of view.'
        results.append(
            {'consumed': False, 'message': Message(text, tcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai
            text = ('The eyes of the {0} look vacant,'
                    ' as he starts to stumble around!').format(entity.name)

            results.append({'consumed': True, 'message': Message(
                text, tcod.light_green)})

            break
    else:
        text = 'There is no targetable enemy at that location.'
        results.append(
            {'consumed': False, 'message': Message(text, tcod.yellow)})

    return results
