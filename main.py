#!/usr/bin/env python2

import os
import sys
import kivy
from functools import partial
from time import time
from glob import glob
from os.path import join

# Kivy
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder, Parser, ParserException
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import *

# Task Scheduler
import task_classes as classes
import task_scheduler as scheduler

# Loads the .kv interface
Builder.load_file('main.kv')

# Create the interface
class Container(BoxLayout):
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        parser = Parser(content=open(self.kv_file).read())
        widget = Factory.get(parser.root.name)()
        Builder._apply_rule(widget, parser.root, parser.root)
        self.add_widget(widget)

class ProcrastinateLater(BoxLayout):
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    def __init__(self, **kwargs):
        super(ProcrastinateLater, self).__init__(**kwargs)
        # Authenticate with drive
        self.drive = scheduler.tsAuthenticate()
        category_page = self.ids['category_page']
        self.schedule = scheduler.getUserSchedule(self.drive)
        self.current_category = ''
        self.current_week = 1
        view_status_button = Button(text='View Tasks By Status', size_y='48dp')
        view_status_button.bind(on_press=partial(self.loadTasksByStatus))
        view_category_button = Button(text='View Tasks By Category', size_y='48dp')
        view_category_button.bind(on_press=partial(self.loadTasksByCategory))
        category_page.add_widget(view_status_button)
        category_page.add_widget(view_category_button)
        for category in self.schedule:
            category_button = Button(text=category.name, size_y='48dp')
            category_button.bind(on_press=partial(self.loadTasks, category_name=category.name))
            category_page.add_widget(category_button)
    def addItem(self, *args, **kwargs):
        task = classes.task()
        taskGrid = GridLayout(cols=1)
        scrollTask = ScrollView()
        scrollTask.add_widget(taskGrid)
        taskPopup = Popup(title=task.name, content=scrollTask, auto_dismiss=False, size_hint=(1, 1))
        taskNameText = TextInput(text=task.name)
        taskExplainText = TextInput(text=task.explain)
        taskDayText = TextInput(text=str(task.day))
        taskDayTime = TextInput(text=str(task.time))
        taskSaveButton = Button(text='Save')
        taskSaveButton.bind(on_press=partial(self.addNewTask,
            taskButtonPopup=taskPopup,
            newTaskName=taskNameText,
            newTaskExplain=taskExplainText,
            newTaskDay=taskDayText,
            newTaskTime=taskDayTime))
        taskCloseButton = Button(text='Cancel', on_press=taskPopup.dismiss)
        taskGrid.add_widget(taskNameText)
        taskGrid.add_widget(taskExplainText)
        taskGrid.add_widget(taskDayText)
        taskGrid.add_widget(taskDayTime)
        taskGrid.add_widget(taskSaveButton)
        taskGrid.add_widget(taskCloseButton)
        taskPopup.open()
        pass
    def showTask(self, *args, **kwargs):
        task = kwargs['taskItem']
        taskGrid = GridLayout(cols=1)
        scrollTask = ScrollView()
        scrollTask.add_widget(taskGrid)
        taskPopup = Popup(title=task.name, content=scrollTask, auto_dismiss=False, size_hint=(1, 1))
        taskNameText = TextInput(text=task.name)
        taskExplainText = TextInput(text=task.explain)
        taskDayText = TextInput(text=str(task.day))
        taskDayTime = TextInput(text=str(task.time))
        taskSaveButton = Button(text='Save')
        taskSaveButton.bind(on_press=partial(self.saveTask,
            taskButtonPopup=taskPopup,
            oldTask=task,
            newTaskName=taskNameText,
            newTaskExplain=taskExplainText,
            newTaskDay=taskDayText,
            newTaskTime=taskDayTime))
        taskCloseButton = Button(text='Cancel', on_press=taskPopup.dismiss)
        taskGrid.add_widget(taskNameText)
        taskGrid.add_widget(taskExplainText)
        taskGrid.add_widget(taskDayText)
        taskGrid.add_widget(taskDayTime)
        taskGrid.add_widget(taskSaveButton)
        taskGrid.add_widget(taskCloseButton)
        taskPopup.open()
        pass
    def saveTask(self, *args, **kwargs):
        taskPopup = kwargs['taskButtonPopup']
        oldTask = kwargs['oldTask']
        newTaskName = kwargs['newTaskName'].text
        newTaskExplain = kwargs['newTaskExplain'].text
        try:
            newTaskDay = int(kwargs['newTaskDay'].text)
        except:
            newTaskDay = -1
        try:
            newTaskTime = int(kwargs['newTaskTime'].text)
        except:
            newTaskTime = 0
        newTask = classes.task(newTaskName, 'Completed', newTaskExplain, newTaskDay, newTaskTime)
        self.schedule.updateTask(oldTask, newTask)
        taskPopup.dismiss()
        self.loadTasks(category_name=self.current_category)
        scheduler.writeUserSchedule(self.schedule, self.drive, self.current_category)
        pass
    def addNewTask(self, *args, **kwargs):
        taskPopup = kwargs['taskButtonPopup']
        newTaskName = kwargs['newTaskName'].text
        newTaskExplain = kwargs['newTaskExplain'].text
        try:
            newTaskDay = int(kwargs['newTaskDay'].text)
        except:
            newTaskDay = -1
        try:
            newTaskTime = int(kwargs['newTaskTime'].text)
        except:
            newTaskTime = 0
        newTask = classes.task(newTaskName, 'Completed', newTaskExplain, newTaskDay, newTaskTime)
        categories = self.schedule.addTask(self.current_category, self.current_week, "", newTask)
        taskPopup.dismiss()
        self.loadTasks(category_name=self.current_category)
        scheduler.writeUserSchedule(self.schedule, self.drive, self.current_category)
        pass
    def loadTasks(self, *args, **kwargs):
        categoryName = kwargs['category_name']
        self.current_category = categoryName
        print(str(kwargs))
        for category in self.schedule:
            if category.name == categoryName:
                sm = self.ids['sm']
                sm.current = 'ViewTasks'
                weekPages = self.ids['ViewPage']
                weekPages.clear_widgets()
                for week in category:
                    print(week.number)
                    gridPage = GridLayout(background_color=(1, 0, 1, .9), cols=1, size_hint_y=None)
                    gridPage.bind(minimum_height=gridPage.setter('height'))
                    weekButton = Button(text=str(week.number), size_hint_y=None, height='50dp')
                    gridPage.add_widget(weekButton)
                    tabbedPage = TabbedPanel(size_hint_y=None, do_default_tab=False, height=self.height)
                    # Create all the panels for days
                    # Monday
                    tabbedItem_monday = TabbedPanelItem(text='Monday')
                    gridPage_monday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_monday.bind(minimum_height=gridPage_monday.setter('height'))
                    scrollPage_monday = ScrollView()
                    scrollPage_monday.add_widget(gridPage_monday)
                    tabbedItem_monday.add_widget(scrollPage_monday)
                    # Tuesday
                    tabbedItem_tuesday = TabbedPanelItem(text='Tuesday')
                    gridPage_tuesday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_tuesday.bind(minimum_height=gridPage_tuesday.setter('height'))
                    scrollPage_tuesday = ScrollView()
                    scrollPage_tuesday.add_widget(gridPage_tuesday)
                    tabbedItem_tuesday.add_widget(scrollPage_tuesday)
                    # Wednesday
                    tabbedItem_wednesday = TabbedPanelItem(text='Wednesday')
                    gridPage_wednesday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_wednesday.bind(minimum_height=gridPage_wednesday.setter('height'))
                    scrollPage_wednesday = ScrollView()
                    scrollPage_wednesday.add_widget(gridPage_wednesday)
                    tabbedItem_wednesday.add_widget(scrollPage_wednesday)
                    # Thursday
                    tabbedItem_thursday = TabbedPanelItem(text='Thursday')
                    gridPage_thursday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_thursday.bind(minimum_height=gridPage_thursday.setter('height'))
                    scrollPage_thursday = ScrollView()
                    scrollPage_thursday.add_widget(gridPage_thursday)
                    tabbedItem_thursday.add_widget(scrollPage_thursday)
                    # Friday
                    tabbedItem_friday = TabbedPanelItem(text='Friday')
                    gridPage_friday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_friday.bind(minimum_height=gridPage_friday.setter('height'))
                    scrollPage_friday = ScrollView()
                    scrollPage_friday.add_widget(gridPage_friday)
                    tabbedItem_friday.add_widget(scrollPage_friday)
                    # Saturday
                    tabbedItem_saturday = TabbedPanelItem(text='Saturday')
                    gridPage_saturday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_saturday.bind(minimum_height=gridPage_saturday.setter('height'))
                    scrollPage_saturday = ScrollView()
                    scrollPage_saturday.add_widget(gridPage_saturday)
                    tabbedItem_saturday.add_widget(scrollPage_saturday )
                    # Sunday
                    tabbedItem_sunday = TabbedPanelItem(text='Sunday')
                    gridPage_sunday = GridLayout(cols=1, size_hint_y=None)
                    gridPage_sunday.bind(minimum_height=gridPage_sunday.setter('height'))
                    scrollPage_sunday = ScrollView()
                    scrollPage_sunday.add_widget(gridPage_sunday)
                    tabbedItem_sunday.add_widget(scrollPage_sunday)
                    # Unassigned
                    tabbedItem_no_day = TabbedPanelItem(text='Unassigned')
                    gridPage_no_day = GridLayout(cols=1, size_hint_y=None)
                    gridPage_no_day.bind(minimum_height=gridPage_no_day.setter('height'))
                    scrollPage_no_day = ScrollView()
                    scrollPage_no_day.add_widget(gridPage_no_day)
                    tabbedItem_no_day.add_widget(scrollPage_no_day)
                    for task in week:
                        taskButton = Button(text=task.name, size_hint_y=None)
                        taskButton.bind(on_press=partial(self.showTask, taskItem=task))
                        if task.day == 1:
                            gridPage_monday.add_widget(taskButton)
                        elif task.day == 2:
                            gridPage_tuesday.add_widget(taskButton)
                        elif task.day == 3:
                            gridPage_wed.add_widget(taskButton)
                        elif task.day == 4:
                            gridPage_thursday.add_widget(taskButton)
                        elif task.day == 5:
                            gridPage_friday.add_widget(taskButton)
                        elif task.day == 6:
                            gridPage_saturday.add_widget(taskButton)
                        elif task.day == 7:
                            gridPage_sunday.add_widget(taskButton)
                        else:
                            gridPage_no_day.add_widget(taskButton)
                    # Add widgets to tabbed page
                    tabbedPage.add_widget(tabbedItem_monday)
                    tabbedPage.add_widget(tabbedItem_tuesday)
                    tabbedPage.add_widget(tabbedItem_wednesday)
                    tabbedPage.add_widget(tabbedItem_thursday)
                    tabbedPage.add_widget(tabbedItem_friday)
                    tabbedPage.add_widget(tabbedItem_saturday)
                    tabbedPage.add_widget(tabbedItem_sunday)
                    tabbedPage.add_widget(tabbedItem_no_day)
                    gridPage.add_widget(tabbedPage)
                    scrollPage = ScrollView(size=self.size)
                    scrollPage.add_widget(gridPage)
                    weekPages.add_widget(scrollPage)
    def loadTasksByStatus(self, *args, **kwargs):
        print('TASK BY STATUS')
        tasks = self.schedule.getTasks()
    def loadTasksByCategory(self, *args, **kwargs):
        print('TASK BY CATEGORY')
        tasks = self.schedule.getTasks()
    def resetTaskPage(self, task):
        x = 1

class ProcrastinateLaterApp(App):
    def build(self):
        return ProcrastinateLater()
        
if __name__ == '__main__':
    ProcrastinateLaterApp().run()
