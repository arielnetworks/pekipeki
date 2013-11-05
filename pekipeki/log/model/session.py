#-*- coding:utf-8 -*-

import functools

import sqlalchemy as al
from sqlalchemy import orm

from . import tables


class Session():

    def __init__(self):

        self.session = session()


    def __enter__(self):

        return self.session


    def __exit__(self, *exception):

        if exception[0] is not None:
            self.session.rollback()

        self.session.close()


    def __getattr__(self, name):

        return getattr(self.session, name)




def with_transaction(f):

    @functools.wraps(f)
    def call(*args, **argd):
        with Session() as sess:
            with sess.begin():
                return f(sess, *args, **argd)

    return call



def without_transaction(f):

    @functools.wraps(f)
    def call(*args, **argd):
        with Session() as sess:
            return f(sess, *args, **argd)

    return call



engine = None
session = None
meta = None


def initialize(conf):

    global engine
    global session
    global meta

    url = conf.get('db_uri')
    echo = bool(conf.get('echo'))

    engine = al.create_engine(url, echo=echo)

    session = orm.sessionmaker(autocommit=True, autoflush=False)
    session.configure(bind=engine)

    tables.Base.metadata.bind = engine
    tables.Base.metadata.create_all()


