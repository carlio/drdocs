# -*- coding: utf-8 -*-

""" module doc """

x = 1
""" something about x """


def fartypants(a, b, c):
    if a > 1:
        return b + c
    elif b != 5:
        return c
    else:
        return a * b + c


class Banana(object):
    """ Fruit is good for you
    don't you know? """

    j = x
    """ J J J J J """

    def __init__(self, cakes=False):
        """
        Create a new Banana with optional cake capability

        @cakes: if this is a cake or not
        """
        pass

    def eric(self):
        # this is a comment but not a docstring
        print 1
        # as is this
        return 1
