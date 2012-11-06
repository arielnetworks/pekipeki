#-*- coding:utf-8 -*-

import re
import urllib2

from pekipeki import trac
from pekipeki.constants import status, event



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



def register_trac_handlers(skp, args):
    u'''
    trac 用
    '''

    tr = trac.Trac(args.trac_url,
                   args.trac_realm,
                   args.trac_user,
                   args.trac_password)

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



def register_handlers(skp, args):
    u'''
    ハンドラ登録
    '''

    skp.register_message_handler(event.RECEIVED, nullpo)
    skp.register_message_handler(event.RECEIVED, haisho)

    if args.trac_url is not None:
        register_trac_handlers(skp, args)

