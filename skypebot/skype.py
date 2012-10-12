#-*- coding:utf-8 -*-

import Skype4Py

from skypebot import utils


event = utils.Enum('RECEIVED')
status = utils.Enum('CONTINUE', 'FINISH')



class MessageEvent(object):
    u'''
    Skype4Py のイベントオブジェクトが使いにくいので使いやすいように
    '''

    def __init__(self, skype, event, msg):

        self.skype = skype
        self.event = event
        self.message = msg


    def get_body(self):
        u'''
        本文
        '''

        return self.message.Body


    def get_sender(self):
        u'''
        送信者
        '''

        return self.message.Sender


    def reply(self, text):
        u'''
        返信
        '''

        chat = self.skype.Chat(self.message.ChatName)
        sender = self.get_sender()

        print sender.Handle, sender.DisplayName

        fullmsg = '@{0} {1}'.format(sender.Handle, text)

        try:
            chat.SendMessage(fullmsg)
        except:
            import traceback
            traceback.print_exc()



class Skype(object):
    u'''
    Skype 用のインタフェイス
    '''


    def on_message(self, msg, evt):
        u'''
        イベント処理
        '''

        handlers = self.message_handlers.get(event.from_str(evt))

        if not handlers:
            return

        for handler in handlers:
            e = MessageEvent(self.skype, evt, msg)

            try:
                result = handler(e)
            except:
                import traceback
                traceback.print_exc()
                continue

            if result == status.FINISH or not result:
                return



    def __init__(self):

        self.message_handlers = {}

        self.skype = Skype4Py.Skype(Transport='x11')
        self.skype.Attach()

        self.skype.OnMessageStatus = self.on_message



    def register_message_handler(self, ev, handler):
        u'''
        イベントハンドラを追加
        '''

        if ev not in event:
            raise TypeError('{0} is not event object'.format(ev.name))

        self.message_handlers[ev] = self.message_handlers.get(ev, []) + [handler]



def nullpo(evt):
    u'''
    ぬるぽに ｶﾞｯ する
    '''

    body = evt.get_body()

    print body

    if u'ぬるぽ' in body:
        evt.reply('ｶﾞｯ')

    return status.CONTINUE



def init():

    skp = Skype()

    skp.register_message_handler(event.RECEIVED, nullpo)

    return skp

