from Kollektion import *
from pony import orm
from datetime import datetime

k = Kollektion('db.sqlite', True)

with orm.db_session:
    t1 = k.Tag(name=u'Ciao', color = 0.15)
    t2 = k.Tag(name=u'Porn', color = 0.07)
    t3 = k.Tag(name=u'Tag Lungo', color = 0.61)
    t4 = k.Tag(name=u'Misure', color = 0.76)

    for i in range(5):
        e = k.Entry(description= "Un post su reddit",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t4],
                    data = ['lol', 'asdf'])

        e = k.Entry(description= "Stocazzo ",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t2, t3, t1],
                    data = ['oijj'])

        e = k.Entry(description= "Alabama",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t4, t1],
                    data = ['adsoisf', 'asdg4rfb'])

        e = k.Entry(description= "The matrix Triology",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t1, t2],
                    data = ['adpprorsf'])

        e = k.Entry(description= "Filosofia spicciola",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t2, t1, t3, t4],
                    data = ['adspbporoif', 'rg5rbfh', 'asfgqwt4bttrsf'])

        e = k.Entry(description= "Domani vado a spasso",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t3, t4],
                    data = ['adsf'])

        e = k.Entry(description= "Misure fighissime",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t2, t4],
                    data = ['lkasjgoei;wgj'])

        e = k.Entry(description= "bla bla bla",
                    creationdate= datetime.now(),
                    lastmodified= datetime.now(),
                    tags = [t4, t3, t1],
                    data = ['adsf'])
