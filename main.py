#!/usr/bin/env python
# -*- coding: utf-8 -*-

#************* IMPORTS **************
#Kivy Imports
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout


#KivyMD Imports
from kivymd.navigationdrawer import MDNavigationDrawer
from kivymd.theming import ThemeManager
from kivymd.card import MDCard
from kivymd.toolbar import Toolbar
from kivy.metrics import dp

#Other python imports
from pony import orm

from Kollektion import *

#*********** SETTINGS ****************
default_window_size = (1400, 930)

#************ CODE *******************

#Widget definitions, the layout of these widgets id definied in the
#Kollektor.kv file
class Tag(BoxLayout):
    color = NumericProperty(0)
    dbTag = ObjectProperty() #handle to db tag correspoinding to gui instance

    #Takes a db tag handle and populates the tag gui with the appropriate info
    def __init__(self, tag, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.dbTag = tag
        self.color = tag.color
        self.ids.tagLabel.text = tag.name

class Entry(MDCard):
    dbEntry = ObjectProperty() #handle to db entry correspoinding to gui instance

    #Takes a db entry handle and populates the gui with the appropriate info
    def __init__(self, entry, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.dbEntry = entry
        self.ids.description.text = entry.description
        for tag in entry.tags:
            guiTag = Tag(tag)
            self.ids.tagList.add_widget(guiTag)

    #Hack della vita
    #Brutally overriding default shadow behaviour
    '''def _update_shadow(self, *args):
        self._shadow = App.get_running_app().theme_cls.quad_shadow
        width = self.width * 1.8
        height = self.height * 1.8

        x = self.center_x - width / 2
        self._soft_shadow_size = (width, height)
        self._hard_shadow_size = (width, height)

        y = self.center_y - height / 2 - dp(.1 * 1.5 ** self.elevation)
        self._soft_shadow_pos = (x, y)
        self._soft_shadow_a = 0.1 * 1.1 ** self.elevation
        self._soft_shadow_texture = self._shadow.textures[
            str(int(round(self.elevation - 1)))]

        y = self.center_y - height / 2 - dp(.5 * 1.18 ** self.elevation)
        self._hard_shadow_pos = (x, y)
        self._hard_shadow_a = .4 * .9 ** self.elevation
        self._hard_shadow_texture = self._shadow.textures[
            str(int(round(self.elevation)))]'''
    pass

class EntryList(BoxLayout):
    #This function accepts a list of tags as input and
    #populates the entry list with the of corresponding entries
    @orm.db_session
    def update(self):
        app = App.get_running_app()

        for entry in app.kollektion.Entry.select():
            guiEntry = Entry(entry)
            self.add_widget(guiEntry)

class TagBar(BoxLayout):
    def on_children(self, instance, val):
        app = App.get_running_app()
        app.root.ids.entryList.update()

#The headbar handles all the magic: searching for entries, showing tags etc
#It is initialized with a db filename and handles to the Tagbar and EntryList
#that will be used to show the data
class HeadBar(Toolbar):
    tagSearch = ObjectProperty()
    #Called when search field is loaded
    def on_tagSearch(self, instance, textbox):
        textbox.bind(on_text_validate=self.validateTag)

    @orm.db_session
    def validateTag(self, textbox):
        app = App.get_running_app()

        #tags = app.kollektion.Tag().select(lambda t: t.name == textbox.text)
        queryTag = orm.select(t for t in app.kollektion.Tag if t.name == textbox.text).first()
        if queryTag is not None:
            guiTag = Tag(queryTag)
            textbox.text = ''
            app.tagBar.add_widget(guiTag)

#Main class of App
class Kollektor(App):
    #Set up basic properties for KivyMD app
    Window.size = default_window_size
    theme_cls = ThemeManager()
    nav_drawer = ObjectProperty()
    title = "Kollektor"

    #Populate entry list, to be changed
    def on_start(self):
        self.kollektion = Kollektion('db.sqlite')
        self.tagBar = self.root.ids.tagBar
        self.root.ids.entryList.update()

#Entry point
if __name__ == '__main__':
    Kollektor().run()
