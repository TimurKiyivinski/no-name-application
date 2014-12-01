#!/usr/bin/env python2
import xml.etree.ElementTree as ET
import glob
from os import listdir
from os.path import isfile, join

# google drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# task_scheduler
import task_classes as classes
import task_shared as shared

PATH = './Schedules'
EMPTY = ''
SPACE = ' '

# Google Drive authentication
def tsAuthenticate():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    return drive

# Uploads a file to Google Drive
def dbUpload(drive, userCategory, categoryStr):
    upSchedule = drive.CreateFile({'title': userCategory.name + 'xml'})
    upSchedule.SetContentString(schedule)
    upSchedule.Upload()

# Prepare the user's Google Drive for use with the application.
def dbSetup():
    cats = ['Games', 'University']
    schedules = classes.schedule()
    for CATEGORY in cats:
        print('%s' % join(PATH, CATEGORY + '.xml'))

# Loads all schedules in the user's Google Drive folder and create a schedule
# accordingly.
def getUserSchedule():
    cats = ['Games', 'University']
    schedules = classes.schedule()
    for CATEGORY in cats:
        try:
            print('%s' % join(PATH, CATEGORY + '.xml'))
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
                            print('Unknown tag:')
                            print(items_tag)
                    schedules.addTask(CATEGORY, new_week, new_week_name, new_task)
        except NameError:
            print('An error has occured parsing the XML.')
    return schedules

# Generates XML files based on user schedules
def writeUserSchedule(userSchedule):
    for category in userSchedule:
        newCat = ET.Element('schedule')
        for week in category:
            newWeek = ET.SubElement(newCat, 'week')
            newWeek.set("val", str(week.number))
            newWeek.set("name", week.name)
            for task in week:
                newTask = ET.SubElement(newWeek, 'task')
                newTaskStatus = ET.SubElement(newTask, 'status')
                newTaskStatus.text = str(task.status)
                newTaskName = ET.SubElement(newTask, 'name')
                newTaskName.text = str(task.name)
                newTaskDesc = ET.SubElement(newTask, 'desc')
                newTaskDesc.text = str(task.explain)
                newTaskDay = ET.SubElement(newTask, 'day')
                newTaskDay.text = str(task.day)
                newTaskTime = ET.SubElement(newTask, 'time')
                newTaskTime.text = str(task.time)
        newTree = ET.ElementTree(newCat)
        newTree.write(category.name + ".xml")

# Used for debugging purposes.
def main(userSchedule):
    for category in userSchedule:
        print(category.toString())
        for week in category:
            print(week.toString())
            for task in week:
                print(task.toString())

#Run the application
if __name__ == '__main__':
    print('Debugging.')
    main(getUserSchedule())
