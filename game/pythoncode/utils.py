# coding=utf-8

def is_whole_number(val):
    if isinstance(val, int):
        return True
    return float(val).is_integer()