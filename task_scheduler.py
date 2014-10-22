#!/usr/bin/env python2
import xml.etree.ElementTree as ET

DATABASE = 'schedule.db'
EMPTY = ''
SPACE = ' '

#Task Class
class task:
    def __init__(self,
            newCat = "",
            newName = "",
            newStatus = "",
            newExplain = "",
            newWeek = 0,
            newDay = 0):
        self.category = newCat
        self.name = newName
        self.status = newStatus
        self.explain = newExplain
        self.week = newWeek
        self.day = newDay
    def setCategory(self, newCategory):
        self.category = newCategory
    def setStatus(self, newStatus):
        self.status = newStatus
    def setName(self, newName):
        self.name = newName
    def setExplain(self, newExplain):
        self.explain = newExplain
    def setWeek(self, newWeek):
        if newWeek in range(1, 53):
            self.week = newWeek
        else:
            self.week = -1
    def setDay(self, newDay):
        if newDay in range(0, 7):
            self.day = newDay
        else:
            self.day = -1
    def toString(self):
        returnString = wrapString(self.status, '[') + SPACE
        returnString += wrapString(self.category, '{') + SPACE + self.explain
        return returnString

#Wraps a string
def wrapString(string, wrapper):
    wrapEnd = ''
    if wrapper == '[':
        wrapEnd = ']'
    elif wrapper == '{':
        wrapEnd = '}'
    elif wrapper == '(':
        wrapEnd = ')'
    elif wrapper == '<':
        wrapEnd = '>'
    else:
        return string
    return wrapper + string + wrapEnd
    
#Create application folder
def dbSetup():
    print "Setting up TaskScheduler database."

#Reads the user's schedule from the database
def getUserSchedule():
    schedules = []
    tree = ET.parse('Schedules/Games.xml')
    root_xml = tree.getroot()
    for week_xml in root_xml:
        for task_xml in week_xml:
            new_task = task()
            new_task.setCategory("Games")
            for items_xml in task_xml:
                items_tag = items_xml.tag
                items_text = items_xml.text
                if items_text is None:
                    continue
                if items_tag == 'status':
                    new_task.setStatus(items_text)
                elif items_tag == 'name':
                    new_task.setName(items_text)
                elif items_tag == 'desc':
                    new_task.setExplain(items_text)
                elif items_tag == 'day':
                    new_task.setDay(items_text)
                else:
                    print "Unknown tag:"
                    print items_tag
            schedules.append(new_task)
    return schedules

#Main function for CLI usage
def main(userSchedule):
    for schedule in userSchedule:
        print schedule.toString()
    '''
    userInput = EMPTY
    while True:
        print 'Task Scheduler'
        if userInput != ' ':
            print 'Previous selection: %s' % userInput
        print 'a - View schedule'
        print 'h - Schedule history'
        print 'q - Quit'
        userInput = raw_input('Selection:')
        if userInput == 'a':
            print 'Week number 23'
        elif userInput == 'h':
            #List history!
            print 'Schedule History'
        elif userInput == 'q':
            quit('Bye!')
        else:
            print 'Invalid selection!'
        '''

#Run the application
if __name__ == '__main__':
    print 'Command line interface activated.'
    main(getUserSchedule())
    raw_input()
else:
    print 'Loaded as a module.'
