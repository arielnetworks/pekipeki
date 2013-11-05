#-*- coding:utf-8 -*-

from pekipeki.constants import status, event



def nullpo(skype, evt):
    u'''
    ぬるぽに ｶﾞｯ する
    '''

    body = evt.get_body()

    if u'ぬるぽ' in body:
        evt.reply(u'ｶﾞｯ')

    return status.CONTINUE



def haisho(skype, evt):
    u'''
    拝承
    '''

    body = evt.get_body()

    if body.endswith(u'たく'):
        evt.reply(u'拝承')

    return status.CONTINUE



def init_skype(skp, args):
    u'''
    ハンドラ登録
    '''

    skp.register_message_handler(event.RECEIVED, nullpo)
    skp.register_message_handler(event.RECEIVED, haisho)


