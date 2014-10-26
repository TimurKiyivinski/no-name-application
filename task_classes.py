#!/usr/bin/env python2
import task_shared as shared

EMPTY = ''
SPACE = ' '

#Task Class
class task:
    def __init__(self,
            newCat = "",
            newName = "",
            newStatus = "",
            newExplain = "",
            newDay = 0):
        self.category = newCat
        self.name = newName
        self.status = newStatus
        self.explain = newExplain
        self.day = newDay
    def setCategory(self, newCategory):
        self.category = newCategory
    def setStatus(self, newStatus):
        self.status = newStatus
    def setName(self, newName):
        self.name = newName
    def setExplain(self, newExplain):
        self.explain = newExplain
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
    def setWeek(self, newNumber):
        if newNumber in range(1, 53):
            self.number = newNumber
        else:
            self.number = -1
            
class category:
    def __init__(self,
            newCategory = "Personal",
            newWeeks = [],
            newOwners = []):
        self.name = newCategory
        self.weeks = newWeeks
        self.owners = newOwners
    def addTask(self, setWeek, newTask):
        for weekNo in self.weeks:
            if setWeek == weekNo.number:
                weekNo.tasks.append(newTask)
                break
        
class schedule:
    def __init__(self,
            newCategories = []):
        self.categories = []
        for cat in newCategories:
            addCategory(cat)
    def addCategory(self, newCategory):
        for cat in self.categories:
            if newCategory.name == cat.name:
                return 'Category already exists.'
        self.categories.append(newCategory)
        return 'Category %s added successfully.' % newCategory.name
    def addTask(self, setCategory, setWeek, newTask):
        for cat in self.categories:
            if setCategory == cat.name:
                cat.addTask(setWeek, newTask)
                break
        
if __name__ == '__main__':
    print 'Please load this as a module.'
else:
    print 'Loaded as module: %s' % __name__
