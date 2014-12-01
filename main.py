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
        category_page = self.ids['category_page']
        self.schedule = scheduler.getUserSchedule()
        for category in self.schedule:
            category_button = Button(text=category.name, size_y='48dp')
            category_button.bind(on_press=partial(self.loadTasks, category_name=category.name))
            category_page.add_widget(category_button)
    def loadTasks(self, *args, **kwargs):
        categoryName = kwargs['category_name']
        print(str(kwargs))
        for category in self.schedule:
            if category.name == categoryName:
                sm = self.ids['sm']
                sm.current = 'ViewTasks'
                weekPages = self.ids['ViewPage']
                for week in category:
                    print(week.number)
                    gridPage = GridLayout(cols=1, size_hint_y=None)
                    gridPage.bind(minimum_height=gridPage.setter('height'))
                    for task in week:
                        taskButton = Button(text=task.name, size_hint_y=None)
                        gridPage.add_widget(taskButton)
                    scrollPage = ScrollView()
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
