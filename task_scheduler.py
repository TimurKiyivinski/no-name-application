#!/usr/bin/env python2

DATABASE = 'schedule.db'
EMPTY = ''
SPACE = ' '

#Task Class
class task:
    def __init__(self, newStatus, newCategory, newExplain, newWeek, newDay):
        self.status = newStatus
        self.category = newCategory
        self.explain = newExplain
        self.week = newWeek
        self.day = newDay
    def toString(self):
        returnString = EMPTY
        if self.status != EMPTY:
            returnString = wrapString('[', self.status) + SPACE
        returnString += wrapString('{', self.category) + SPACE + self.explain
        return returnString

#Wraps a string
def wrapString(wrapper, string):
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
    schedule_1 = task('DONE', 'PERSONAL', 'Get this message to send.', 2, 0)
    schedule_2 = task(EMPTY, 'WORK', 'Submit reports.', 2, 0)
    schedule_3 = task(EMPTY, 'PERSONAL', 'Write a biography on my sad life.', 2, 0)
    schedule_4 = task('DONE', 'PERSONAL', 'Get this message to send again.', 2, 0)
    schedule_5 = task('POSTPONED', 'WORK', 'Life threatening mission.', 2, 0)
    schedule_6 = task(EMPTY, 'PERSONAL', 'Dwell on the meaning on keyboards.', 2, 0)
    schedules = [schedule_1, schedule_2, schedule_3, schedule_4, schedule_5, schedule_6]
    return schedules

#Main function for CLI usage
def main(userSchedule):
    #drive = tsAuthenticate()
    #dbUpload(drive, "<schedule>EXAMPLE!</schedule>")
    for schedule in userSchedule:
        print schedule.toString()
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
            #listSchedule('Monday')
            print 'Week number 23'
        elif userInput == 'h':
            #List history!
            print 'Schedule History'
        elif userInput == 'q':
            quit('Bye!')
        else:
            print 'Invalid selection!'

#Run the application
if __name__ == '__main__':
    print 'Command line interface activated.'
    main(getUserSchedule())
    raw_input()
else:
    print 'Loaded as a module.'
