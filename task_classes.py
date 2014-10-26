#!/usr/bin/env python2
import task_shared as shared

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
        returnString = shared.wrapString(self.status, '[') + SPACE
        returnString += shared.wrapString(self.category, '{') + SPACE + self.explain
        return returnString

class week:
    def __init__(self,
            newNumber = 1,
            newTasks = []):
        self.tasks = newTasks
        self.number = newNumber
        
if __name__ == '__main__':
    print 'Please load this as a module.'
else:
    print 'Loaded as module: %s' % __name__
