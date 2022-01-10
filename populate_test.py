from Kollektion import *
from pony import orm
from datetime import datetime

k = Kollektion('db.sqlite', create_new=True)

with orm.db_session:
    t1 = k.Tag(name='Ciao', color=0.15)
    t2 = k.Tag(name='Porn', color=0.07)
    t3 = k.Tag(name='Tag Lungo', color=0.61)
    t4 = k.Tag(name='Misure', color=0.76)

    for i in range(5):
        k.Entry(description='Un post su reddit',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t4],
                data=['lol', 'asdf'])

        k.Entry(description='Stocazzo',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t2, t3, t1],
                data=['oijj'])

        k.Entry(description='Alabama',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t4, t1],
                data=['adsoisf', 'asdg4rfb'])

        k.Entry(description='The matrix Triology',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t1, t2],
                data=['adpprorsf'])

        k.Entry(description='Filosofia spicciola',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t2, t1, t3, t4],
                data=['adspbporoif', 'rg5rbfh', 'asfgqwt4bttrsf'])

        k.Entry(description='Domani vado a spasso',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t3, t4],
                data=['adsf'])

        k.Entry(description='Misure fighissime',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t2, t4],
                data=['lkasjgoei;wgj'])

        k.Entry(description='bla bla bla',
                creationdate=datetime.now(),
                lastmodified=datetime.now(),
                tags=[t4, t3, t1],
                data=['adsf'])
