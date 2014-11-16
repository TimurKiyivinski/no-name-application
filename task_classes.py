#!/usr/bin/env python2
import task_shared as shared

EMPTY = ''
SPACE = ' '

#Task Class
class task:
    def __init__(self,
            newName = "",
            newStatus = "",
            newExplain = "",
            newDay = 0,
            newTime = 0):
        self.name = newName
        self.status = newStatus
        self.explain = newExplain
        self.day = newDay
        self.time = newTime
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
    def setTime(self, newTime):
        self.time = newTime
    def toString(self):
        returnString = shared.wrapString(self.status, '[') + SPACE
        returnString += shared.wrapString(self.name, '(') + SPACE
        returnString += shared.wrapString(self.explain, '<')
        return returnString

class week:
    def __init__(self,
            newNumber = 1,
            newName = "",
            newTasks = []):
        self.number = newNumber
        self.name = newName
        self.tasks = newTasks
        self.iter_current = 0
    def __iter__(self):
        return self
    def next(self):
        if self.iter_current >= len(self.tasks):
            self.iter_current = 0
            raise StopIteration
        else:
            self.iter_current += 1
            return self.tasks[self.iter_current - 1]
    def setName(self, newName):
        self.name = newName
    def setWeek(self, newNumber):
        if newNumber in range(1, 53):
            self.number = newNumber
        else:
            self.number = -1
    def addTask(self, newTask):
        self.tasks.append(newTask)
    def toString(self):
        return "Week " + str(self.number) + SPACE + ":" + SPACE + self.name
            
class category:
    def __init__(self,
            newCategory = "Personal",
            newWeeks = []):
        self.name = newCategory
        self.weeks = newWeeks
        self.iter_current = 0
    def __iter__(self):
        return self
    def next(self):
        if self.iter_current >= len(self.weeks):
            self.iter_current = 0
            raise StopIteration
        else:
            self.iter_current += 1
            return self.weeks[self.iter_current - 1]
    def setName(self, newName):
        self.name = newName
    def addWeek(self, newWeek):
        for weekNo in self.weeks:
            if newWeek.number == weekNo.number:
                return 'Week already exists.'
        self.weeks.append(newWeek)
        return 'Week succesfully added.' 
    def addTask(self, setWeek, setWeekName, newTask):
        for weekNo in self.weeks:
            if int(setWeek) == int(weekNo.number):
                weekNo.addTask(newTask)
                return
        new_week = week(setWeek, setWeekName, [])
        new_week.addTask(newTask)
        self.addWeek(new_week)
    def toString(self):
        return 'Category %s: %d weeks.' % (self.name, len(self.weeks))
        
class schedule:
    def __init__(self,
            newCategories = []):
        self.categories = []
        self.iter_current = 0
        for cat in newCategories:
            self.addCategory(cat)
    def __iter__(self):
        return self
    def next(self):
        if self.iter_current >= len(self.categories):
            self.iter_current = 0
            raise StopIteration
        else:
            self.iter_current += 1
            return self.categories[self.iter_current - 1]
    def addCategory(self, newCategory):
        for cat in self.categories:
            if newCategory.name == cat.name:
                return 'Category already exists.'
        self.categories.append(newCategory)
        return 'Category %s added successfully.' % newCategory.name
    def addTask(self, setCategory, setWeek, setWeekName, newTask):
        for cat in self.categories:
            if setCategory == cat.name:
                cat.addTask(setWeek, setWeekName, newTask)
                return
        new_category = category(setCategory, [])
        new_category.addTask(setWeek, setWeekName, newTask)
        self.addCategory(new_category)
        
if __name__ == '__main__':
    print 'Please load this as a module.'
else:
    print 'Loaded as module: %s' % __name__
