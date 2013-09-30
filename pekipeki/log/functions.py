#-*- coding:utf-8 -*-

from .model import session, tables

import sqlalchemy as al
from sqlalchemy import sql



def search(sess, name, chat, page=0, count=20):

    t = tables.Log.__table__

    where = sql.and_(t.c.user == name,
                     t.c.chat == chat)

    query = sql.select([t.c.user, t.c.message, t.c.time],
                       where,
                       t).order_by(t.c.time.desc())

    query = query.offset(page*count).limit(count)

    result = sess.execute(query)
    items = result.fetchall()

    return [dict(zip(x.keys(), x.values()))
            for x in items]



