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
    cats = ['Games', 'University']
    schedules = classes.schedule()
    for CATEGORY in cats:
        try:
            print '%s' % join(PATH, CATEGORY + '.xml')
            tree = ET.parse(join(PATH, CATEGORY + '.xml'))
            root_xml = tree.getroot()
            for week_xml in root_xml:
                new_week = week_xml.attrib['val']
                new_week_name = week_xml.attrib['name']
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
                        elif items_tag == 'time':
                            new_task.setTime(items_text)
                        else:
                            print 'Unknown tag:'
                            print items_tag
                    schedules.addTask(CATEGORY, new_week, new_week_name, new_task)
        except NameError:
            print 'An error has occured parsing the XML.'
    return schedules

#Main function for CLI usage
def main(userSchedule):
    #TODO: Get schedules!
    #'''
    for category in userSchedule:
        print category.toString()
        for week in category:
            print week.toString()
            for task in week:
                print task.toString()

#Run the application
if __name__ == '__main__':
    print 'Command line interface activated.'
    main(getUserSchedule())
else:
    print 'Loaded as a module.'
