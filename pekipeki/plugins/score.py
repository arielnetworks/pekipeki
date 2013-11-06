#-*- coding:utf-8 -*-

import re

from pekipeki.constants import status, event
from pekipeki.log.model import tables, session
from pekipeki.log import functions


COUNT_REGEX = re.compile(u'([^ ]+) *(\+\+|--)')



@session.with_transaction
def increment_score(sess, name, op):

    d = {'++': 1, '--': -1}[op]

    return functions.update_score(sess, name, d)



def find_increment(body):

    m = COUNT_REGEX.search(body)

    if m is None:
        return

    return m.group(1).strip(), m.group(2)



def score_increment(skype, evt):

    body = evt.get_body()

    name, op = find_increment(body)

    if name is None:
        return

    result = increment_score(name, op)

    evt.send(u'%s 現在: %s' % (name, result))



def init_skype(skp, conf):

    skp.register_message_handler(event.RECEIVED, score_increment)

