# -*- coding: utf-8 -*-
import sys
from drdocs.parse import parse_module


def run():
    path = sys.argv[1]
    parse_module(path)
