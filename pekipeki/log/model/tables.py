#-*- coding:utf-8 -*-

import sqlalchemy as al
from sqlalchemy import sql
from sqlalchemy.sql import functions
from sqlalchemy.ext import declarative as decl


Base = decl.declarative_base()



class Log(Base):
    u'''
    ユーザの発言を記録する
    '''

    __tablename__ = 'logs'

    id = al.Column(al.Integer, primary_key=True)
    user = al.Column(al.Unicode(255), nullable=False)
    chat = al.Column(al.Unicode(255), nullable=False)
    time = al.Column(al.DateTime, nullable=False)
    message = al.Column(al.UnicodeText, nullable=False)



def _create_maker(cls):
    u'''
    作るための関数を作る
    '''

    def create_entry(sess, **kw):

        entry = cls(**kw)
        sess.add(entry)

        return entry

    return create_entry



def _uc_columns(args):
    u'''
    UniqueConstraint のカラムを取ってくる
    '''

    for arg in args:

        if isinstance(arg, al.UniqueConstraint):
            return set(x.name for x in arg.columns)

    return set()



def _search_maker(cls):
    u'''
    検索のための関数を作る
    '''

    tbl = cls.__table__
    keys = tbl.c.keys()
    cols = [tbl.c[x] for x in keys]
    d = dict(zip(keys, cols))

    def search_entry(sess, **kw):

        query = sql.select(cols,
                           sql.and_(*[d[k] == v for k, v in kw.items()]),
                           tbl).order_by(tbl.c.id)

        result_proxy = sess.execute(query)

        results = list(result_proxy)

        return [cls(**dict(zip(keys, result)))
                for result in results]

    return search_entry



def _exists_checker_maker(cls):
    u'''
    すでにあるかどうかをチェックする関数を作る
    '''

    tbl = cls.__table__
    keys = tbl.c.keys()
    cols = [tbl.c[x] for x in keys]
    d = dict(zip(keys, cols))
    constraints = _uc_columns(cls.__table_args__)

    def check_exists(sess, **kw):

        if set(kw.keys()) != constraints:
            return False

        kw = dict((k, v) for k, v in kw.items()
                  if k in constraints)

        query = sql.select([functions.count()],
                           sql.and_(*[d[k] == v for k, v in kw.items()]),
                           tbl)
        result = sess.execute(query).fetchone()

        return result[0] != 0

    return check_exists



def _deleter_maker(cls):
    u'''
    削除する関数を作る
    '''

    tbl = cls.__table__
    keys = tbl.c.keys()
    cols = [tbl.c[x] for x in keys]
    d = dict(zip(keys, cols))


    def deleter(sess, **kw):
        pass


create_log = _create_maker(Log)
search_log = _search_maker(Log)

