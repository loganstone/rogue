import tcod

WALL_TILE = 256
FLOOR_TILE = 257
PLAYER_TILE = 258
ORC_TILE = 259
TROLL_TILE = 260
SCROLL_TILE = 261
HEALINGPOTION_TILE = 262
SWORD_TILE = 263
SHIELD_TILE = 264
STAIRSDOWN_TILE = 265
DAGGER_TILE = 266


def load_customfont():
    # The index of the first custom tile in the file
    a = 256

    # The "y" is the row index,
    # here we load the sixth row in the font file.
    # Increase the "6" to load any new rows from the file
    for y in range(5, 6):
        tcod.console_map_ascii_codes_to_font(a, 32, 0, y)
        a += 32
