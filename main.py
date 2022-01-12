#!/usr/bin/env python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty

from pony import orm

from Kollektion import Kollektion


class Tag(MDBoxLayout):
    color = NumericProperty(0)
    dbTag = ObjectProperty()  # handle to db tag corresponding to gui instance

    # Takes a db tag handle and populates the tag gui with the appropriate info
    def __init__(self, tag, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.dbTag = tag
        self.color = tag.color
        self.ids.tagLabel.text = tag.name


class Entry(MDCard):
    dbEntry = ObjectProperty()  # handle to db entry corresponding to gui instance

    # Takes a db entry handle and populates the gui with the appropriate info
    def __init__(self, entry, *args, **kwargs):
        super(Entry, self).__init__(*args, **kwargs)
        self.dbEntry = entry
        self.ids.description.text = entry.description
        for tag in entry.tags:
            gui_tag = Tag(tag)
            self.ids.tagList.add_widget(gui_tag)


class EntryList(MDBoxLayout):
    @orm.db_session
    def update(self):
        app = MDApp.get_running_app()

        for entry in app.kollektion.Entry.select():
            gui_entry = Entry(entry)
            self.add_widget(gui_entry)


class TagBar(MDBoxLayout):
    def on_children(self, instance, val):
        app = MDApp.get_running_app()
        app.root.ids.entryList.update()


class HeadBar(MDToolbar):
    @orm.db_session
    def validate_tag(self, textbox):
        app = MDApp.get_running_app()

        # tags = app.kollektion.Tag().select(lambda t: t.name == textbox.text)
        query_tag = orm.select(t for t in app.kollektion.Tag if t.name == textbox.text).first()
        if query_tag is not None:
            gui_tag = Tag(query_tag)
            textbox.text = ''
            app.tagBar.add_widget(gui_tag)


class Kollektor(MDApp):
    # Set up basic properties for KivyMD app
    def __init__(self, **kwargs):
        self.title = "Kollektor"
        Window.size = (1400, 900)
        super().__init__(**kwargs)

    # Populate entry list, to be changed
    def on_start(self):
        self.kollektion = Kollektion('db.sqlite')
        self.root.ids.entryList.update()


# Entry point
if __name__ == '__main__':
    Kollektor().run()
