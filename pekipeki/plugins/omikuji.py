#-*- coding:utf-8 -*-

import random
import sched
import time
import threading

from pekipeki.constants import status, event
from pekipeki import utils

RAND = random.Random()

ANSWERS = [u'大吉',
           u'吉'
           u'吉'
           u'中吉'
           u'中吉'
           u'小吉',
           u'小吉',
           u'中吉'
           u'中吉'
           u'小吉',
           u'小吉',
           u'凶',
           u'凶',
           u'凶',
           u'大凶']



def omikuji(skype, evt, args):
    u'''
    進捗どうですかに応える
    '''

    value = RAND.choice(ANSWERS)

    evt.reply(value)



def init_skype(skp, conf):

    skp.register_command_handler(event.RECEIVED, 'omikuji', omikuji)
