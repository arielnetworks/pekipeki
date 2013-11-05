#-*- coding:utf-8 -*-

from .model import session, tables

import sqlalchemy as al
from sqlalchemy import sql



def search(sess, word, chat, page=0, count=20):

    t = tables.Log.__table__

    where = sql.and_(t.c.chat == chat,
                     sql.or_(t.c.user.like(u'%'+word+u'%'),
                             t.c.message.like(u'%'+word+u'%')))

    query = sql.select([t.c.user, t.c.message, t.c.time],
                       where,
                       t).order_by(t.c.time.desc())

    query = query.offset(page*count).limit(count)

    result = sess.execute(query)
    items = result.fetchall()

    return [dict(zip(x.keys(), x.values()))
            for x in items]



def increment_score(sess, name):

    score = sess.query(tables.UserScore).filter_by(name=name).first()

    if score is None:
        user = tables.UserScore(name=name, score=1)
        sess.add(user)
        return 1
    else:
        score.score += 1
        return score.score









