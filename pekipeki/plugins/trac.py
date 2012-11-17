#-*- coding:utf-8 -*-

import re
import urllib2

from pekipeki import trac
from pekipeki.constants import status, event



TICKET_REGEX = re.compile(r'#(\d+)')

REVISION_REGEX = re.compile(r'r(\d+)')


def pick_and_make_url(reg, mkmsg):
    u'''
    抜き出して URL 吐き出す
    '''

    def replace(evt):
        u'''
        特定の形式をなんとかする
        '''

        body = evt.get_body()

        for m in reg.finditer(body):
            link = mkmsg(m.group(1))

            evt.send(link)

        return status.CONTINUE


    return replace


def init_config(conf_addr):

    keys = ['url', 'realm', 'user', 'password']

    conf_addr(keys, {})



def register_handlers(skp, conf):
    u'''
    trac 用ハンドラ登録
    '''

    if conf.url is None:
        return

    tr = trac.Trac(conf.url,
                   conf.realm,
                   conf.user,
                   conf.password)

    def make_ticket_summary(x):
        u'''
        trac のサマリを吐く
        '''

        url = tr.get_ticket_url(x)

        try:
            ticket = tr.get_ticket(x)
        except urllib2.HTTPError, e:
            return u'えらーでた {0} {1}'.format(e.code, url)

        return u'{0} {1}'.format(ticket['summary'], url)


    ticket = pick_and_make_url(TICKET_REGEX, make_ticket_summary)
    revision = pick_and_make_url(REVISION_REGEX, tr.get_revision_url)

    skp.register_message_handler(event.RECEIVED, ticket)
    skp.register_message_handler(event.RECEIVED, revision)

