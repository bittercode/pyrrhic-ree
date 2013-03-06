#  get the controller and alias it to controller for easier use
from ReeController import controller
controller = controller.Controller


'''
controller funcs
'''


def replaceAll(self):
    return replaceArbitraryCount(0)


def replaceArbitraryCount(self, count):
    return self.compiledRegex.sub(self.regex, self.replace, self.matchString, count, self.flags)


def allMatches(self):
    return self.compiledRegex.findall(self.matchString)


def search(self, searchString):
    return self.compiledRegex.search(self.searchString)
'''
end controller funcs
'''


def should_process_regex(self):
    proceed = True

    if not controller.regex or not controller.matchString:
        self.clear_results
        proceed = False

    return proceed and not self.is_paused


def processReplacements(self):
    #  check for the replacement and then
    #  do the subs - both all subs and just first
    if controller.replace:
        replaceAll = controller.replaceAll()
        replaceFirst = controller.replaceArbitraryCount(1)
        print('REPL: ', replaceAll)
        self.ui.tebRepAll.setText(replaceAll)
        self.ui.tebRep1.setText(replaceFirst)


def processFindAll(self):
    #This is a big change I"m not updating the spinner
    allMatches = controller.allMatches()
    if allMatches:
        print('MatchIndex:', len(allMatches)-1)

    match_obj = controller.search()

    if match_obj is None:
        self.ui.tebMatch.setPlainText("No Match")
        self.ui.tebMatchAll.setPlainText("No Match")
        self.ui.statusbar.showMessage("No Match", 0)
    else:
        #This is the single match
        self.populate_match_textbrowser(match_obj.start(), match_obj.end())
        #This will fill in all matches
        #This is a big change I"m not updating the spinner
        spans = controller.getSpans()
        self.populate_matchAll_textbrowser(spans)


def processGroups(self):
    #This is the start of groups and right now it goes to the end of process_regex
    #It works right now as long as groups are not named - I think
    print(controller.compiledRegex.groupindex)

    allMatches = controller.allMatches()
    match_obj = controller.search()

    group_tuples = []

    if match_obj.groups():
        group_nums = {}

        #This creates a dictionary of group names
        if controller.compiledRegex.groupindex:
            keys = controller.compiledRegex.groupindex.keys()
            for key in keys:
                group_nums[controller.compiledRegex.groupindex[key]] = key

        #Here I build a tuple of tuples - with each group match
        #it is match number, group number, name and then the match
        for x in range(len(allMatches)):
            g = allMatches[x]
            if isinstance(g, tuple):
                for i in range(len(g)):
                    group_tuple = (x+1, i+1, group_nums.get(i+1, ""), g[i])
                    group_tuples.append(group_tuple)
            else:
                group_tuples.append((x+1, 1, group_nums.get(1, ""), g))

    #print(group_tuples)
    self.populate_group_textbrowser(group_tuples)


def process_regex(self):
    if not self.should_process_regex():
        return

    self.process_embedded_flags()
    self.processReplacements()
    self.processFindAll()
    self.processGroups()
