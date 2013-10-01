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


from pekipeki import utils

STATUS = utils.Enum('SUCCESS', 'FAILURE', 'UNSTABLE', 'ABORTED')
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



def get_last_status(builds):

    for build in builds:
        url = build['url']
        data = get_json(url)

        if data['result'] is None:
            continue

        data['number'] = build['number']

        return data

    return dict(result=None, number=None, changeSet=[])



def make_changeset_description(changesets):

    result = []

    for item in changesets['items']:
        author = item['user']
        revision = item['commitId']
        message = item['msg']

        result.append(u'''\
---- Revision: r%s ----
Author: %s
Description:
%s
''' % (revision, author, message))

    return u'\n'.join(result)



def check(skp, url, chat, context):

    data = get_json(url)

    builds = data.get('builds')
    name = data.get('name')

    build = get_last_status(builds)

    lastnum = context.get('last_build')
    laststatus = context.get('last_status')

    curnum = build.get('number')
    curstatus = build.get('result')

    if curstatus is not None and \
            STATUS.SUCCESS != curstatus and \
            lastnum != curnum:
        c = skp.get_chat(chat)
        buildurl = build['url']
        msg = make_changeset_description(build['changeSet'])
        c.send_message(u'''%s build %s: %s
%s
''' % (name, curstatus.lower(), buildurl, msg))

    if STATUS.SUCCESS != curstatus and \
            laststatus is not None and \
            STATUS.SUCCESS != laststatus and \
            lastnum != curnum:
        c = skp.get_chat(chat)
        c.send_message(u'%s build fixed: %s' % (name, url))

    context['last_build'] = curnum
    context['last_status'] = curstatus



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






