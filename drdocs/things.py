

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

    def __repr__(self):
        """
        A representation of where this Thing was found when parsing and running.

        Returns:
          str: a human readable and human useful representation of where to find this thing in the codebase
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


class Function(DocableThing):
    pass


class ClazzMethod(DocableThing):
    pass
