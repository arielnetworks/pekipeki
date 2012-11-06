#-*- coding:utf-8 -*-

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



def register_handlers(skp, args):
    u'''
    ハンドラ登録
    '''

    skp.register_message_handler(event.RECEIVED, nullpo)
    skp.register_message_handler(event.RECEIVED, haisho)


