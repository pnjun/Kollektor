#!/usr/bin/env python
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput

from pony import orm

from Kollektion import Kollektion


class Tag(MDBoxLayout):
    color = NumericProperty(0)
    dbTag = ObjectProperty()  # handle to db tag corresponding to gui instance

    # Takes a db tag handle and populates the tag gui with the appropriate info
    def __init__(self, tag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_tag = tag
        self.color = tag.color
        self.ids.tag_label.text = tag.name


class Entry(MDCard):
    dbEntry = ObjectProperty()  # handle to db entry corresponding to gui instance

    # Takes a db entry handle and populates the gui with the appropriate info
    def __init__(self, entry, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_entry = entry
        self.ids.description.text = entry.description
        for tag in entry.tags:
            gui_tag = Tag(tag)
            self.ids.tagList.add_widget(gui_tag)


# TODO: create decorator that sets system_cursor in a context manager
class EntryList(MDBoxLayout):
    def __init__(self, tag_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.populate(tag_list)

    def search_entries(self, tag_list):
        app = MDApp.get_running_app()

        query = app.kollektion.Entry.select()
        for tag in tag_list:
            query = query.filter(lambda e: tag in e.tags)
        return query

    @orm.db_session
    def populate(self, tag_list):
        Window.set_system_cursor('wait')

        for entry in self.search_entries(tag_list):
            gui_entry = Entry(entry)
            self.add_widget(gui_entry)
        Window.set_system_cursor('arrow')


class TagBar(MDBoxLayout):
    def on_children(self, instance, val):
        app = MDApp.get_running_app()
        tag_list = [t.db_tag for t in self.children]
        scroll_view = app.root.ids.entry_scroll
        if scroll_view.children:
            scroll_view.remove_widget(scroll_view.children[0])
        scroll_view.add_widget(EntryList(tag_list))


class TagSearch(TextInput):

    def keyboard_on_key_down(self, keyboard, keycode, text, modifiers):
        """ Overrides a backspace and enter key presses for custom behaviour """
        _, key_name = keycode
        if key_name == 'backspace' and self.text == '':
            app = MDApp.get_running_app()
            try:
                app.tag_bar.remove_widget(app.tag_bar.children[0])
            except IndexError:
                pass
        elif key_name == 'enter':
            # Catch the on_enter event and block it so that the textInput doesn't lose focus
            # since, the standard on_text_validate removes focus from the textInput.
            self.on_enter()
        else:
            super().keyboard_on_key_down(keyboard, keycode, text, modifiers)

    @orm.db_session
    def on_text(*args):
        """ TODO: give hints for autocomplete"""
        pass

    @orm.db_session
    def on_enter(self):
        """ Load appropriate tags from DB and add it to the tag bar"""
        app = MDApp.get_running_app()

        query_tag = app.kollektion.Tag.select(lambda t: t.name.lower() == self.text.lower()).first()

        if query_tag is not None:
            self.text = ''
            gui_tag = Tag(query_tag)
            app.tag_bar.add_widget(gui_tag)


class Kollektor(MDApp):
    # Set up basic properties for KivyMD app
    def __init__(self, **kwargs):
        self.title = "Kollektor"
        Window.size = (1400, 900)
        super().__init__(**kwargs)

    # Populate entry list, to be changed
    def on_start(self):
        self.kollektion = Kollektion('db.sqlite')
        self.tag_bar = self.root.ids.filter_bar.ids.tag_bar


# Entry point
if __name__ == '__main__':
    Kollektor().run()
