# -*- coding: utf-8 -*-


def simple_func_no_comments(arg1):
    return arg1 > 4


def complex_func_no_comments(arg1, arg2):
    if arg1 > 10:
        if arg2 < 5:
            tot = 0
            for x in range(arg1, arg2):
                tot += (x/2)
            return tot
        else:
            if arg2 == (arg1*3):
                return 9
            else:
                return 4
    else:
        return arg1 / 4


def func_with_inner_func():
    def inner_func():
        # comment here does it mean anything for the outer func?
        print 1
    inner_func()
