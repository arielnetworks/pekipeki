#-*- coding:utf-8 -*-

import random
import sched
import time
import threading

from pekipeki.constants import status, event
from pekipeki import utils

RAND = random.Random()

ANSWERS = [(250, u'進捗ダメです!'),
           (256, u'進捗ありました!')]


INTERVAL = 60 * 60 * 2 # 二時間


THREAD = None


def answer(skype, evt):
    u'''
    進捗どうですかに応える
    '''

    body = evt.get_body()

    if not body.startswith(u'進捗どうですか'):
        return

    value = RAND.randint(0, 255)

    for threshold, ans in ANSWERS:
        if value < threshold:
            evt.reply(ans)
            break;
    else:
        evt.reply(u'なんかへん')



def question(skp, chat):

    c = skp.get_chat(chat)
    c.send_message(u'進捗どうですか!')



def run(skp, targets, interval):

    sc = sched.scheduler(time.time, time.sleep)

    for chat in targets:
        utils.loop_event(sc, interval, question, skp, chat)

    sc.run()



def init_config(conf_addr):

    keys = ['targets', 'interval']
    defaults = dict(targets=[], interval=str(INTERVAL))

    conf_addr(keys, defaults)



def parse_targets(targets):

    result = []

    for line in targets.splitlines():
        line = line.strip()

        if not line:
            continue

        result.append(line.strip())

    return result



def init_skype(skp, conf):

    global THREAD

    skp.register_message_handler(event.RECEIVED, answer)

    targets = conf.get('targets')
    interval = int(conf.get('interval'))

    if not targets:
        return

    targets = parse_targets(targets)

    th = threading.Thread(target=run, args=(skp, targets, interval))
    th.setDaemon(True)
    th.start()
    THREAD = th
