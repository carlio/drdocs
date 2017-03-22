# -*- coding: utf-8 -*-
import os


def load_test_data(filename):
    filepath = os.path.join(os.path.dirname(__file__), 'testdata', filename)
    return open(filepath).read()
