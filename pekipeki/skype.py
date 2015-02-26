#-*- coding:utf-8 -*-

import re
import shlex

import Skype4Py

from pekipeki import constants
from pekipeki.constants import event
from . import command
from pekipeki.command import commands


CMD_REG = re.compile(r'\$[^ ]+')


class Sender(object):

    def __init__(self, sender):

        self.sender = sender


    def get_fullname(self):

        return self.sender.FullName


    def get_user_id(self):

        return self.sender.Handle


    def get_display_name(self):

        return self.sender.DisplayName



class Message(object):

    def __init__(self, message):

        self.message = message


    def get_date(self):

        return self.message.Datetime


    def get_body(self):

        return self.message.Body


    def get_sender(self):

        return Sender(self.message.Sender)



class Chat(object):

    def __init__(self, chat):
        self.chat = chat


    def send_message(self, msg):

        self.chat.SendMessage(msg)


    def get_id(self):

        return self.chat.Name


    def get_title(self):

        return self.chat.FriendlyName


    def get_latest_messages(self, count=20):

        msgs = self.chat.Messages[-count:]

        return [Message(x) for x in msgs]



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


    def __init__(self):

        self.message_handlers = {}

        self.skype = Skype4Py.Skype(Transport='x11')
        self.skype.Attach()

        self.skype.OnMessageStatus = self.on_message

        self.command_dispatcher = command.CommandDispatcher()

        self.command_dispatcher.register_command(event.RECEIVED, 'commands', commands.CommandsCommand())
        self.command_dispatcher.register_command(event.RECEIVED, 'help', commands.HelpCommand())


    def on_message(self, msg, evt):
        u'''
        イベント処理
        '''

        event = constants.event.from_str(evt)

        e = MessageEvent(self.skype, event, msg)

        self.proc_handlers(event, e)
        self.proc_command_handlers(event, e)


    def proc_handlers(self, event, message):

        handlers = self.message_handlers.get(event)

        if not handlers:
            return

        for handler in handlers:

            try:
                result = handler(self, message)
            except:
                import traceback
                traceback.print_exc()
                continue

            if result is None:
                continue

            if result == constants.status.FINISH:
                break


    def proc_command_handlers(self, event, message):

        body = message.get_body()

        if CMD_REG.match(body):
            args = self.parse_args(body)
            cmd = args[0]
            args = args[1:]
            self.command_dispatcher.dispatch_command(self, message, event, cmd, args)



    def parse_args(self, body):

        msgs = body.lstrip('$')

        msgs = msgs.encode('utf-8')

        args = [x.decode('utf-8') for x in shlex.split(msgs)]

        return args



    def register_message_handler(self, ev, handler):
        u'''
        イベントハンドラを追加
        '''

        if ev not in constants.event:
            raise TypeError('{0} is not event object'.format(ev.name))

        self.message_handlers[ev] = self.message_handlers.get(ev, []) + [handler]


    def register_command_handler(self, ev, command, handler):

        self.command_dispatcher.register_command(ev, command, handler)


    def get_chat(self, name):

        return Chat(self.skype.Chat(name))


    def list_chat(self):

        return [Chat(x) for x in self.skype.Chats]


    def get_command_dispatcher(self):

        return self.command_dispatcher



def init():

    skp = Skype()

    return skp
