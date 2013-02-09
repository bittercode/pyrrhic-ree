'''
This module represents an abstraction of re.

Using this module a view can interact with the re
system. It defines the entire controller API that
all views must be programmed against.
'''

import re

class ree:
    """The Regex API."""
    def __init__(self):
        self._regex = ""
        self._matchstring = ""
        self._replaceString = ""
        self._flags = 0
        self._compiledRegex = re.compile(self._regex, self._flags)

    def regex():
        doc = "The regex string"
        def fget(self):
            return self._regex
        def fset(self, value):
            try:
                self._regex = str(value)
            except UnicodeError:
                self._regex = unicode(value)
            self._compiledRegex = re.compile(self._regex, self._flags)
        return locals()
    regex = property(**regex())

    def matchString():
        doc = "The match string."
        def fget(self):
            return self._matchString
        def fset(self, value):
            try:
                self._matchString = str(value)
            except UnicodeError:
                self._matchstring = unicode(value)
        return locals()
    matchString = property(**matchString())

    def replaceString():
        doc = "The replacement string"
        def fget(self):
            return self._replaceString
        def fset(self, value):
            try:
                self._replaceString = str(value)
            except UnicodeError:
                self._replaceString = unicode(value)
        return locals()
    replaceString = property(**replaceString())