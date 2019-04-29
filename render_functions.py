import tcod

from enum import Enum, auto

from data.tile import load_customfont, WALL_TILE, FLOOR_TILE

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    STAIRS = auto()
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x
             and entity.y == y
             and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value,
               maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1,
                      False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1,
                          False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(
        panel, int(x + total_width / 2), y,
        tcod.BKGND_NONE, tcod.CENTER,
        '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map,
               fov_recompute, message_log, screen_width,
               screen_height, bar_width, panel_height, panel_y,
               mouse, colors, game_state):
    # Draw all the tiles in the game map
    load_customfont()
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        tcod.console_put_char_ex(
                            con, x, y, WALL_TILE,
                            tcod.white,
                            tcod.black)
                    else:
                        tcod.console_put_char_ex(
                            con, x, y, FLOOR_TILE,
                            tcod.white,
                            tcod.black)
                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:

                        tcod.console_put_char_ex(
                            con, x, y, WALL_TILE,
                            tcod.gray,
                            tcod.black)
                    else:
                        tcod.console_put_char_ex(
                            con, x, y, FLOOR_TILE,
                            tcod.gray,
                            tcod.black)

    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)
    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    tcod.console_set_default_background(panel, tcod.black)
    panel.clear(fg=(255, 255, 63))

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(
            panel, message_log.x, y,
            tcod.BKGND_NONE,
            tcod.LEFT, message.text)
        y += 1

    render_bar(
        panel, 1, 1, bar_width,
        'HP', player.fighter.hp, player.fighter.max_hp,
        tcod.light_red, tcod.darker_red)

    text = 'Dungeon level: {0}'.format(game_map.dungeon_level)
    tcod.console_print_ex(
        panel, 1, 3, tcod.BKGND_NONE, tcod.LEFT, text)
    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE, tcod.LEFT,
                          get_names_under_mouse(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width,
                      panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inv_title = ('Press the key next to an item to use it,'
                         ' or Esc to cancel.\n')
        else:
            inv_title = ('Press the key next to an item to drop it,'
                         ' or Esc to cancel.\n')

        inventory_menu(con, inv_title, player,
                       50, screen_width, screen_height)
    elif game_state == GameStates.LEVEL_UP:
        text = 'Level up! Choose a stat to raise:'
        level_up_menu(con, text, player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) \
            or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(con, entity.x, entity.y,
                              entity.char, tcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
