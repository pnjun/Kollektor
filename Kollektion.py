from os import path
from pony import orm
from datetime import datetime
# This class handles a Kollektion

class Kollektion:
    # Load a db from file, according to the models defined. If createNew is True,
    # a new db is created in case dbFile does not exist. If debugDb is True, SQL
    # queries made to the db are printed out.
    def __init__(self, db_file, create_new=False, debug_db=False):
        # Load db from file
        self.db = orm.Database("sqlite", db_file, create_db=create_new)

        # Model definitions:
        # Each model class hinerits from a particular db instance, therefore
        # the model classes defined in a kollektion are direcly linked to the
        # db file that describes that kollektion.

        # Tag:
        # The name of the tag is used to search for tags in the db, each tag
        # has a color. Tags are organized in a tree-like structure: each tag
        # can have a parent tag (but only one) and many children.
        # Tags loops are to be avoided. If an entry is tagged by a tag, it is
        # considered tagged by all parents of that tag.
        class Tag(self.db.Entity):
            name = orm.Required(str, unique=True)
            color = orm.Optional(float)
            parent = orm.Optional("Tag", reverse="children")
            children = orm.Set("Tag", reverse="parent")
            entries = orm.Set('Entry')

        # Entry:
        # The description is what is shown about an Entry when entries are listed
        # Each entry has a creation date and a last modified date (automatically
        # updated at each save) and a set of Tags.
        # The data json is a list of items, each item must have a dict entry
        # named 'class' that identifies the item type (e.g. file, link, note.. etc)
        # everythhing else is left free: this allows for modification of the item
        # types (e.g. adding a new class of items, or a new property for an item)
        # without the need of changing the database structure.
        class Entry(self.db.Entity):
            description = orm.Required(str)
            creationdate = orm.Required(datetime)
            lastmodified = orm.Required(datetime)
            tags = orm.Set(Tag)
            data = orm.Required(orm.Json)

        # Save the db-connected classes in the kollection instance
        self.Tag = Tag
        self.Entry = Entry

        # Generate mappings between the db and the models defined above
        orm.sql_debug(debug_db)
        self.db.generate_mapping(create_tables=create_new)
