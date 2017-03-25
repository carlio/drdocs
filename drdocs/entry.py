# -*- coding: utf-8 -*-
import sys
from drdocs.parse import parse_file


def run():
    path = sys.argv[1]
    things = parse_file(path)
    for t in things:
        print t.get_messages()
