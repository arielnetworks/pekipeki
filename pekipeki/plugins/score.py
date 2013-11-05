#-*- coding:utf-8 -*-

import re

from pekipeki.constants import status, event
from pekipeki.log.model import tables, session
from pekipeki.log import functions


nameregex = re.compile(u'([^ ]+) *\+\+')


@session.with_transaction
def increment_score(sess, name):

    return functions.increment_score(sess, name)



def find_name(body):

    m = nameregex.search(body)

    if m is None:
        return

    return m.group(1).strip()



def score_increment(skype, evt):

    body = evt.get_body()

    name = find_name(body)

    if name is None:
        return

    result = increment_score(name)

    evt.send(u'%s 現在: %s' % (name, result))



def init_skype(skp, conf):

    skp.register_message_handler(event.RECEIVED, score_increment)

