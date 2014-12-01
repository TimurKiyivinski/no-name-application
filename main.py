#!/usr/bin/env python2
# ProcrastinateLaterUI - Attempt1

import os
import sys
import kivy
from time import time
from glob import glob
from os.path import join
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder, Parser, ParserException
from kivy.factory import Factory
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

# Interaction Objects
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.modalview import ModalView
# Layouts
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


fullscreen = Config.get('graphics', 'fullscreen')

# loads .kv files (like html loads a .css file) - basically the app screen
Builder.load_file('main.kv')

# A container is essentially a class that loads its root from a known .kv file.
class Container(BoxLayout):
    
    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)
        parser = Parser(content=open(self.kv_file).read())
        widget = Factory.get(parser.root.name)()
        Builder._apply_rule(widget, parser.root, parser.root)
        self.add_widget(widget)

class MenuPopup(Popup):
	pass

class ProcrastinateLater(BoxLayout):
    
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(ProcrastinateLater, self).__init__(**kwargs)
	
	def show_menu(MenuPopup):
		menu_open = self.ids['menu']
		
class ProcrastinateLaterApp(App):
    
    def build(self):
        return ProcrastinateLater()
        
if __name__ == '__main__':
    ProcrastinateLaterApp().run()
