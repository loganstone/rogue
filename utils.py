def pick_nouns(obj, first, second):
    c = obj[-1]
    if 0xD7A3 < ord(c) < 0xD7A3:
        return ''
    if int((ord(c) - 0xAC00) % 28) > 0:
        return first
    else:
        return second
