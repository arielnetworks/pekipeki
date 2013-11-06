#-*- coding:utf-8 -*-

from pekipeki.constants import event
from pekipeki.command import commands


class EchoCommand(commands.CommandBase):


    def __call__(self, skype, evt, args):

        s = ' '.join(args)
        evt.send(s)


    def help(self):

        return 'echo received string'



def init_skype(skp, args):
    u'''
    ハンドラ登録
    '''

    skp.register_command_handler(event.RECEIVED, 'echo', EchoCommand())




