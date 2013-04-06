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
        self._matchString = ""
        self._replaceString = ""
        self._flags = 0
        self.compiledRegex = re.compile(self._regex, self._flags)
        self._flagChecker = re.compile(r"^ *\(\?(?P<flags>[aiLmsx]*)\)")
        self._debug = True
        self.updateView = lambda: None
        self._flagSet = set()

    #  use property to force regex compile on set
    def regex():
        doc = "The regex string"

        def fget(self):
            return self._regex

        def fset(self, value):
            self._regex = str(value)
            self.compile()
            self.updateView()
        return locals()
    regex = property(**regex())

    #  use property to force new values to convert to strings
    def matchString():
        doc = "The match string."

        def fget(self):
            return self._matchString

        def fset(self, value):
            self._matchString = str(value)
            self.updateView()
        return locals()
    matchString = property(**matchString())

    #use a property to force compile on flag update
    def flags():
        doc = "The flags to be compiled with the regex"

        def fget(self):
            return self._flags

        def fset(self, value):
            self._flags = value
            self.compile()
            self.updateView()

        return locals()
    flags = property(**flags())

    #  use property to force new values to convert to strings
    def replaceString():
        doc = "The replacement string"

        def fget(self):
            return self._replaceString

        def fset(self, value):
            self._replaceString = str(value)
            self.updateView()
        return locals()
    replaceString = property(**replaceString())

    def embeddedFlags(self):
        match = self._flagChecker.match(self.regex)
        newFlagSet = set(match.group('flags')) if match else set()
        self._flagSet, missingFlagSet = newFlagSet, self._flagSet - newFlagSet
        return self._flagSet, missingFlagSet

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

    def replaceAll(self):
        return self.replaceArbitraryCount(0)

    def replaceArbitraryCount(self, count):
        return self.compiledRegex.sub(
            self._replaceString,
            self._matchString,
            count,
        )

    def search(self):
        return self.compiledRegex.search(self.matchString)

    def getGroups(self):
        '''
        Returns all groups - Named or not - as a list of tuples.

        The tuples contain the following format
        t[0] match number (starting at 1 for first match)
        t[1] group number (starting at 1 for first group)
        t[2] group name (defaults to empty string for unamed group)
        t[3] the matched string
        '''
        matches = self.compiledRegex.findall(self.matchString)
        matchObj = self.search()

        groupTuples = []

        if matchObj is not None and matchObj.groups():
            groupNames = {}

            if self.compiledRegex.groupindex:
                groupNames = {v: k for k, v in self.compiledRegex.groupindex.items()}

            for x, group in enumerate(matches):
                if isinstance(group, tuple):
                    for i in range(len(group)):
                        tmpGroup = (x + 1, i + 1, groupNames.get(i + 1, ""), group[i])
                        groupTuples.append(tmpGroup)
                else:
                    tmpTuple = (x+1, 1, groupNames.get(1, ""), group)
                    groupTuples.append(tmpTuple)

        return groupTuples

    def compile(self):
        tmp = None
        try:
            tmp = re.compile(self._regex, self._flags)
        except re.error:
            if self._debug:
                print("Incomplete Regex")
        else:
            self.compiledRegex = tmp

Controller = _ree()
