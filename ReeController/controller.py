'''
This module represents an abstraction of re.

Using this module a view can interact with the re
system. It defines the entire controller API that
all views must be programmed against.
'''

import re


class _ree:
    """
    The Regex API.
    Using a class because it allows us to set up properties
    which you can't do in the module level
    """
    def __init__(self):
        self._regex = ""
        self._matchstring = ""
        self._replaceString = ""
        self.flags = 0
        self.compiledRegex = re.compile(self._regex, self.flags)
        self._flagChecker = re.compile(r"^ *\(\?(?P<flags>[aiLmsx]*)\)")
        self._debug = True

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

    def getSpans(self):
        spans = []
        match_obj = self.compiledRegex.search(self.matchString)
        last_span = None

        while match_obj:
            start = match_obj.start()
            end = match_obj.end()
            span = (start, end)
            if last_span == span:
                break
            spans.append(span)
            last_span = span
            match_obj = self.compiledRegex.search(self.matchString, end)

        if self._debug:
            print("FA Spans: ", spans)

        return spans

Controller = _ree()
