# -*- coding: utf-8 -*-
import ast
import tokenize
from collections import defaultdict

import asttokens
from drdocs.things import MethodOrFunction
from mccabe import PathGraphingAstVisitor
from six import StringIO


"""
This module takes python modules and converts them into simplified data
structures representing their type and attaching comment objects to them if
found.

This can be either a docstring (parsed using the ast module) or a #comment
(parsed using the tokenize module).
"""


def parse_module_file(filepath):
    """
    Given a filepath which is assumed to be a python module, separate it into the various
    things which can be documented and attached any relevant comments and documentation to it.

    Args:
      filepath(str): A path to the module to inspect. This can be either an absolute path
                     or a path relative to the current working directory.
    """
    return parse_module_code(open(filepath).read(), filepath=filepath)


def parse_module_code(source, filepath=None):
    """
    Parse a string containing Python source into the various Thing objects that it represents
    and are interesting to this library.

    Args:
      source(str): A string representing an entire block of Python code which should be inspected.
      filepath(str): The path containing this code. If left as None, the default, no path information
                     will be recorded.
    """
    # Both the AST and tokens are required, as the AST module does not return regular comments
    # but the tokenize module does not have quite enough structure information. The asttoken
    # library is used to annotate AST nodes with location information, which can then be used in
    # combination with the tokens to attach comments which may have been removed. Additionally,
    # the mccabe library is then used to annotate nodes with complexity information.
    astok = asttokens.ASTTokens(source, parse=True)

    # For the purposes of this library, a particular documentable thing is considered to have coordinates
    # of the location of the first token making up its node in the AST, which forms the key in this dictionary
    things = defaultdict(list)

    # split the AST into the nodes we care about and discard the ones we don't care about
    for node in ast.walk(astok.tree):
        if isinstance(node, ast.FunctionDef):
            coords = (node.lineno, node.col_offset)
            things[coords].append(MethodOrFunction(filepath, node))

    # now attach inline comments because the number of comments should be appropriate for the McCabe complexity
    # of certain types of node
    tokens = tokenize.generate_tokens(StringIO(source).readline)
    for token in tokens:
        if token[0] == tokenize.COMMENT:
            for thing_list in things.values():
                for thing in thing_list:
                    # allow the Thing object to determine whether to pay attention to this comment or not
                    thing.add_comment(token)

    # now attach complexity information to them
    visitor = PathGraphingAstVisitor()
    visitor.preorder(astok.tree, visitor)

    for graph in visitor.graphs.values():
        complexity = graph.complexity()
        coords = (graph.lineno, graph.column)
        for thing in things[coords]:
            if isinstance(thing, MethodOrFunction):
                thing.set_complexity(complexity)

    for thing_list in things.values():
        for thing in thing_list:
            thing._print_docs()
