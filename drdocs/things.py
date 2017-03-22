# -*- coding: utf-8 -*-
import ast


class DocableThing(object):
    """
    This rather poorly named object represents any Python structure or thing which
    can be documented, such as a class, a module, a method or an attribute. It is
    a general class to collect common information such as location and fully qualified
    name of that thing.
    """
    def __init__(self, filepath, line_number, char_number, fqn):
        """
        Generic constructor for a Python "Thing" which is documentable.

        Args:
          filepath(str): the relative path to where this thing was found
          line_number(int): the line in the file where this thing was found
          char_number(int): the character position on the line in which this thing begins
          fqn(str): some kind of identifier which would allow a user to figure out where this
                    thing is in their code - for example, module.SomeClass.attribute_name
        """
        self.filepath = filepath
        self.line_number = line_number
        self.char_number = char_number
        self.fqn = fqn

    def get_doc_status(self, config):
        """
        Returns an object representing whether or not this Thing has been documented well enough
        to the criteria defined in the configuration.

        Args:
          config(config.Config): the configuration specified when running this tool which will change
                                 what each Thing considers necessary for "sufficient" documentation.

        Returns:
          doc_status: An object describing how this object was documented along with ratings based on
                      how well the documentation passed the checks required in the configuration.

        Raises:
          NotImplementedError: it is expected that subclasses provide the specific implementation of this
        """
        raise NotImplementedError

    def __repr__(self):
        """
        A representation of where this Thing was found when parsing and running.

        Returns:
          str: a human readable and human useful representation of where to find this Thing in the codebase
        """
        return "%s (%s %s:%s)" % (self.fqn, self.filepath, self.line_number, self.char_number)


class Module(DocableThing):
    pass


class ModuleAttribute(DocableThing):
    pass


class Class(DocableThing):
    pass


class ClassAttribute(DocableThing):
    pass


class MethodOrFunction(object):
    """
    Represents either a method or a function. This can be a module-level function, a
    class method or static method. Or an inline function. Anything.
    """

    def __init__(self, filepath, node):
        """
        Args:
          filepath(str): The file containing the definition of this method or function. May or may
                         not be known if this is just being parsed from a simple string object.
          node(asttoken.Node): An annotated node which is very similar to an ast module node but
                                also has location information of the first and last token making up
                                this node.
        """
        self.filepath = filepath
        self.node = node
        self.docstring = ast.get_docstring(node)
        self.complexity = None
        self.comments = []

    def set_complexity(self, complexity):
        """
        Sets the McCabe complexity of this method or function, if known.
        """
        self.complexity = complexity

    def add_comment(self, token):
        """
        If a COMMENT token occurs inside the scope of the node of this method, accumulate it here.
        """
        # TODO: consider indentation? Since indentation is not syntactically necessary for comments
        # it is currently simply a case of any comment at any level of indentation in the scope of this
        # node is taken note of.
        comment_line = token[2][0]
        if comment_line <= self.node.first_token.start[0]:
            # this comment is before this method/func, abort
            return
        if comment_line >= self.node.last_token.end[0]:
            # this comment is after this method/func, abort
            return
        self.comments.append(token)

    def _print_docs(self):
        print self.docstring
        for c in self.comments:
            print c[1]
