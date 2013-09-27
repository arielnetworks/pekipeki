#-*- coding:utf-8 -*-

import Skype4Py

from pekipeki import constants



class Sender(object):

    def __init__(self, sender):

        self.sender = sender


    def get_fullname(self):

        return self.sender.FullName


    def get_user_id(self):

        return self.sender.Handle


    def get_display_name(self):

        return self.sender.DisplayName



class MessageEvent(object):
    u'''
    Skype4Py のイベントオブジェクトが使いにくいので使いやすいように
    '''

    def __init__(self, skype, event, msg):

        self.skype = skype
        self.event = event
        self.message = msg


    def get_id(self):
        u'''
        メッセージ ID
        '''

        return self.message.Id


    def get_body(self):
        u'''
        本文
        '''

        return self.message.Body


    def get_sender(self):
        u'''
        送信者
        '''

        return Sender(self.message.Sender)


    def reply(self, text):
        u'''
        返信
        '''

        chat = self.skype.Chat(self.message.ChatName)
        sender = self.get_sender()

        fullmsg = u'@{0} {1}'.format(sender.get_fullname(), text)

        try:
            chat.SendMessage(fullmsg)
        except:
            import traceback
            traceback.print_exc()


    def send(self, text):
        u'''
        送る
        '''

        chat = self.skype.Chat(self.message.ChatName)

        try:
            chat.SendMessage(text)
        except:
            import traceback
            traceback.print_exc()


    def get_chat_name(self):
        u'''
        部屋の名前
        '''

        return self.message.ChatName


    def get_datetime(self):
        u'''
        送信日時
        '''

        return self.message.Datetime



class Skype(object):
    u'''
    Skype 用のインタフェイス
    '''


    def on_message(self, msg, evt):
        u'''
        イベント処理
        '''

        handlers = self.message_handlers.get(constants.event.from_str(evt))

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

            if result is None:
                continue

            if result == constants.status.FINISH:
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

        if ev not in constants.event:
            raise TypeError('{0} is not event object'.format(ev.name))

        self.message_handlers[ev] = self.message_handlers.get(ev, []) + [handler]



def init():

    skp = Skype()

    return skp

