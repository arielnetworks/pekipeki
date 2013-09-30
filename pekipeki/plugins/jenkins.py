#-*- coding:utf-8 -*-

import threading
import urllib2
import time
import traceback

try:
    import json
except:
    import simplejson as json

import sched


THREAD = None


def loop_event(sc, interval, func, *args):

    def call():

        try:
            func(*args)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

        sc.enter(interval, 1, call, ())

    sc.enter(0, 1, call, ())



def get_json(url):

    url = url + 'api/json/'
    data = json.loads(urllib2.urlopen(url).read())

    return data



def check(skp, url, chat, context):

    data = get_json(url)

    builds = data.get('builds')
    name = data.get('name')

    burl = builds[0]['url']
    build = get_json(burl)

    lastnum = context.get('last_build')
    laststatus = context.get('last_status')

    curnum = builds[0]['number']

    if build['result'] != 'SUCCESS' and lastnum != curnum:
        c = skp.get_chat(chat)
        c.send_message('%s build failed: %s' % (name, burl))

    context['last_build'] = curnum



def run(skp, targets, interval):

    sc = sched.scheduler(time.time, time.sleep)

    for url, chat in targets:
        loop_event(sc, interval, check, skp, url, chat, {})

    sc.run()



def init_config(conf_addr):

    keys = ['targets', 'interval']
    defaults = dict(targets=[], interval='600')

    conf_addr(keys, defaults)



def parse_targets(targets):

    result = []

    for line in targets.splitlines():
        line = line.strip()

        if not line:
            continue

        result.append(tuple([x.strip() for x in line.split(',')]))

    return result



def init_skype(skp, conf):

    global THREAD

    targets = conf.get('targets')
    interval = int(conf.get('interval'))

    if not targets:
        return

    targets = parse_targets(targets)

    th = threading.Thread(target=run, args=(skp, targets, interval))
    th.setDaemon(True)
    th.start()
    THREAD = th






