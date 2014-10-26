#!/usr/bin/env python2
import xml.etree.ElementTree as ET
import glob
from os import listdir
from os.path import isfile, join

#task_scheduler
import task_classes as classes
import task_shared as shared

PATH = './Schedules'
EMPTY = ''
SPACE = ' '
    
#Create application folder
def dbSetup():
    print 'Setting up TaskScheduler database.'

#Reads the user's schedule from the database
def getUserSchedule():
    schedules = classes.schedule()
    cats = ['Games', 'University']
    for CATEGORY in cats:
        print '%s' % join(PATH, CATEGORY + '.xml')
        tree = ET.parse(join(PATH, CATEGORY + '.xml'))
        root_xml = tree.getroot()
        for week_xml in root_xml:
            new_week = week_xml.attrib
            for task_xml in week_xml:
                new_task = classes.task()
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
                #schedules.append(new_task)
                schedules.addTask(CATEGORY, new_week, new_task)
    return schedules

#Main function for CLI usage
def main(userSchedule):
    #TODO: Get schedules!
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
