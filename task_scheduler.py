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
    while (1):
        try:
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            break
        except:
            print('Error authenticating, retying...')
    return drive

# Schedules folder
def getFolder(drive):
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for drive_file in file_list:
        if drive_file['title'] == 'XML-Schedules' and drive_file['mimeType'] == 'application/vnd.google-apps.folder':
            return drive_file
    drive_file = drive.CreateFile({'title': 'XML-Schedules', 'mimeType': 'application/vnd.google-apps.folder'})
    drive_file.Upload()
    return drive_file

# Uploads a file to Google Drive
def dbUpload(drive, userCategory, categoryStr):
    found = False
    driveFolder = getFolder(drive)
    file_list = drive.ListFile({'q': "'" + driveFolder['id'] + "' in parents and trashed=false"}).GetList()
    for drive_file in file_list:
        if drive_file['title'] == userCategory.name + '.xml':
            found = True
            upSchedule = drive.CreateFile({'id': drive_file['id'],'title': userCategory.name + '.xml',
                "parents": [{"kind": "drive#fileLink","id": driveFolder['id']}]})
            break
    if found == False:
        upSchedule = drive.CreateFile({'title': userCategory.name + '.xml',
            "parents": [{"kind": "drive#fileLink","id": driveFolder['id']}]})
    upSchedule.SetContentString(categoryStr)
    upSchedule.Upload()

# Loads all schedules in the user's Google Drive folder and create a schedule
# accordingly.
def getUserSchedule(drive):
    schedules = classes.schedule()
    try:
        driveFolder = getFolder(drive)
        file_list = drive.ListFile({'q': "'" + driveFolder['id'] + "' in parents and trashed=false"}).GetList()
        for drive_file in file_list:
            if drive_file['mimeType'] == 'text/plain':
                try:
                    drive_category = drive_file['title'][0:-4]
                    root_xml = ET.fromstring(drive_file.GetContentString())
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
                            try:
                                schedules.addTask(drive_category, new_week, new_week_name, new_task)
                            except:
                                print('An error has occured adding task.')
                except NameError:
                        print('An error has occured parsing %s' % drive_file['title'])
    except:
        print('An error has occured')
    return schedules

# Generates XML files based on user schedules
def writeUserSchedule(userSchedule, drive, upCategory = ''):
    for category in userSchedule:
        if upCategory != '':
            if category.name != upCategory:
                print ('Skipping!')
                continue
        print('Uploading schedule: %s' % upCategory)
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
        treeString = ET.tostring(newCat)
        dbUpload(drive, category, treeString)

# Used for debugging purposes.
def main():
    print('Authenticating')
    drive = tsAuthenticate()
    print('Getting schedule')
    test_schedule = getUserSchedule(drive)
    for cat in test_schedule:
        print(cat.name)
    print('Getting folder')
    test_folder = getFolder(drive)
    #print('Writing schedule')
    #writeUserSchedule(test_schedule, drive)

#Run the application
if __name__ == '__main__':
    print('Debugging.')
    main()
