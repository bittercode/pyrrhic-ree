'''
This module represents an abstraction of re.

Using this module a view can interact with the re
system. It defines the entire controller API that
all views must be programmed against.
'''

import re

# Using a class because it allows us to set up properties
# which you can't do in the module level
class _ree:
    """The Regex API."""
    def __init__(self):
        self._regex = ""
        self._matchstring = ""
        self._replaceString = ""
        self.flags = 0
        self.compiledRegex = re.compile(self._regex, self.flags)
        self._flagChecker = re.compile(r"^ *\(\?(?P<flags>[aiLmsx]*)\)")

    #  use property to force regex compile on set
    def regex():
        doc = "The regex string"
        def fget(self):
            return self._regex
        def fset(self, value):
            self._regex = str(value)
            self.compiledRegex = re.compile(self._regex, self.flags)
        return locals()
    regex = property(**regex())

    #  use property to force new values to convert to strings
    def matchString():
        doc = "The match string."
        def fget(self):
            return self._matchString
        def fset(self, value):
            self._matchString = str(value)
        return locals()
    matchString = property(**matchString())

    #  use property to force new values to convert to strings
    def replaceString():
        doc = "The replacement string"
        def fget(self):
            return self._replaceString
        def fset(self, value):
            self._replaceString = str(value)
        return locals()
    replaceString = property(**replaceString())

    def embeddedFlags(self):
        match = self._flagChecker.match(self.regex)
        return set(match.group('flags')) if match else set() 



Controller = _ree()

