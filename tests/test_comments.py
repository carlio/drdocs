# -*- coding: utf-8 -*-
from unittest import TestCase
from drdocs.parse import parse_module_code


class TestCommentsAndComplexity(TestCase):

    def test_simple_func_no_comments(self):
        source = '''def func(arg1):
    return arg1 > 4'''
        parse_module_code(source)

    def test_simple_func_with_docstring(self):
        source = '''def func(arg1):
  """
  This function does nothing interesting at all.

  Args:
    arg1(int): A number that is not quite big enough
  """
  return arg1 + 1
'''
        parse_module_code(source)

    def test_simple_func_inline_comments(self):
        source = '''def func(arg1):
  ret = arg1 * 3
  # need three times more!
  return ret'''
        parse_module_code(source)
