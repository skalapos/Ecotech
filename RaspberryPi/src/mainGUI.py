"""
 * @file mainGUI.py
 * @authors Steven Kalapos & Ben Bellerose
 * @date May 22 2018
 * @modified May 22 2018
 * @modifiedby SK
 * @brief GUI managment and creation
 */
 """
import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty, Property 
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen


import random

##https://github.com/kivy/kivy/wiki/Data-driven-variables-with-kivy-properties##
class temperature(Label):
    def update(self):
        text = str(random.randint(0,100))

#default "screen saver"
class defaultScreenLayout(GridLayout):
    def __init__(self, **kwargs):
        super(defaultScreenLayout, self).__init__(**kwargs)
    
    Clock.schedule_interval(temperature.update,2)

#main App GUI control
class ecozoneApp(App):

    def build(self):
        return defaultScreenLayout()