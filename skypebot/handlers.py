#-*- coding:utf-8 -*-

import re

from skypebot import utils
from skypebot.constants import status


def nullpo(evt):
    u'''
    ぬるぽに ｶﾞｯ する
    '''

    body = evt.get_body()

    print body

    if u'ぬるぽ' in body:
        evt.reply('ｶﾞｯ')

    return status.CONTINUE



TICKET_REGEX = re.compile(r'#(\d+)')
TICKET_BASE = 'http://legion.ariel-networks.com/agn/ticket/'

REVISION_REGEX = re.compile(r'r(\d+)')
REVISION_BASE = 'http://legion.ariel-networks.com/agn/changeset/'


def pick_and_make_url(reg, baseurl):
    u'''
    抜き出して URL 吐き出す
    '''

    def replace(evt):
        u'''
        特定の形式をなんとかする
        '''

        body = evt.get_body()

        print body

        for m in reg.finditer(body):
            link = baseurl + m.group(1)

            print link

            evt.send(link)

        return status.CONTINUE


    return replace


ticket = pick_and_make_url(TICKET_REGEX, TICKET_BASE)

revision = pick_and_make_url(REVISION_REGEX, REVISION_BASE)










