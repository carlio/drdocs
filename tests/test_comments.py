# -*- coding: utf-8 -*-
from unittest import TestCase
from drdocs.parse import parse_code


class TestCommentsAndComplexity(TestCase):
    """
    One of the measurements and moans of this tool is to make sure that
    complex code (measured by McCabe complexity) should have a docstring
    or several inline comments which would clarify each of the steps. The
    assumption is that lots of possible code forks means lots of decisions
    were made while writing the code which means it should have a good
    explanation for the maintainer.

    This series of tests verifies that the complexity to comment density ratio
    can be measured, and that the configuration options for this tool will
    allow suppression or ignoring those if desired.
    """

    def test_simple_func_no_comments(self):
        source = '''def func(arg1):
    return arg1 > 4'''
        print [t.get_messages() for t in parse_code(source, 'test')]

    def test_simple_func_with_docstring(self):
        source = '''def func(arg1):
  """
  This function does nothing interesting at all.

  Args:
    arg1(int): A number that is not quite big enough
  """
  if arg1 > 2:
    arg1 += 2
  elif arg1 < 0:
    arg1 = 4
  else:
    arg1 = arg1 * 2
  return arg1 + 1
'''
        print [(t.complexity, len(t.comments), t.get_messages()) for t in parse_code(source, 'test')]

    def test_simple_func_inline_comments(self):
        source = '''def func(arg1):
  ret = arg1 * 3
  # need three times more!
  return ret'''
        print [t.get_messages() for t in parse_code(source, 'test')]
