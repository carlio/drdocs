# -*- coding: utf-8 -*-
from __future__ import division
import ast


SEVERITIES = (
    'GOOD_DOCS',
    'INSUFFICIENT_DOCS',
    'NO_DOCS'
)


class Message(object):
    """
    Represents a message to be conveyed to the user of this library
    """
    def __init__(self, thing, severity, message_text):
        self.thing = thing
        self.severity = severity
        self.message_text = message_text

    def __repr__(self):
        return self.message_text


class DocableThing(object):
    """
    This rather poorly named object represents any Python structure or thing which
    can be documented, such as a class, a module, a method or an attribute. It is
    a general class to collect common information such as location and fully qualified
    name of that thing.
    """
    def __init__(self, filepath, node):
        """
        Generic constructor for a Python "Thing" which is documentable.

        Args:
          filepath(str): the relative path to where this thing was found. May or may
                         not be known if this is just being parsed from a simple string object.
          node(asttoken.Node): An annotated node which is very similar to an ast module node but
                               also has location information of the first and last token making up
                               this node.
        """
        self.filepath = filepath
        self.node = node
        self.docstring = ast.get_docstring(node)

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


class MethodOrFunction(DocableThing):
    """
    Represents either a method or a function. This can be a module-level function, a
    class method or static method. Or an inline function. Anything.
    """

    def __init__(self, filepath, node):
        super(MethodOrFunction, self).__init__(filepath, node)
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
        if self.node.first_token.start[0] <= comment_line <= self.node.last_token.end[0]:
            self.comments.append(token)

    def get_messages(self):
        messages = []
        if not self.docstring:
            messages.append(Message(self, 'INSUFFICIENT_DOCS',
                                    'No docstring for this method/function'))

        # TODO: sufficient docs per complexity and also docstring or not depending on complexity should be configurable
        if self.complexity > 3 and (len(self.comments) / self.complexity) < (1/3):
            messages.append(Message(self, 'INSUFFICIENT_DOCS',
                            'This method or function is complex but does not have a lot of comments'))
        return messages
