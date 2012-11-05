#-*- coding:utf-8 -*-

import re
import urllib2

from skypebot import utils, trac
from skypebot.constants import status, event



def nullpo(evt):
    u'''
    ぬるぽに ｶﾞｯ する
    '''

    body = evt.get_body()

    if u'ぬるぽ' in body:
        evt.reply(u'ｶﾞｯ')

    return status.CONTINUE


def haisho(evt):
    u'''
    拝承
    '''

    body = evt.get_body()

    if body.endswith(u'たく'):
        evt.reply(u'拝承')

    return status.CONTINUE



TICKET_REGEX = re.compile(r'#(\d+)')
TICKET_BASE = 'http://legion.ariel-networks.com/agn/ticket/'

REVISION_REGEX = re.compile(r'r(\d+)')
REVISION_BASE = 'http://legion.ariel-networks.com/agn/changeset/'


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



def register_handlers(skp, args):

    tr = trac.Trac(args.trac_url,
                   args.trac_realm,
                   args.trac_user,
                   args.trac_password)

    def make_ticket_summary(x):
        u'''
        trac のサマリを吐く
        '''

        url = TICKET_BASE + x

        try:
            ticket = tr.get_ticket(x)
        except urllib2.HTTPError, e:
            return u'えらーでた {0} {1}'.format(e.code, url)

        return u'{0} {1}'.format(ticket['summary'], url)


    ticket = pick_and_make_url(TICKET_REGEX, make_ticket_summary)
    revision = pick_and_make_url(REVISION_REGEX, lambda x:REVISION_BASE + x)

    skp.register_message_handler(event.RECEIVED, nullpo)
    skp.register_message_handler(event.RECEIVED, ticket)
    skp.register_message_handler(event.RECEIVED, revision)
    skp.register_message_handler(event.RECEIVED, haisho)

