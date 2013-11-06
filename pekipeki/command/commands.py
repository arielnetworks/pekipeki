#-*- coding: utf-8 -*-

import abc
import StringIO


class CommandBase(object):

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def __call__(self, skype, evt, args):
        u'''
        :param skype: skype 操作用オブジェクト
        :param evt: イベントオブジェクト
        :param [str] args: 引数
        '''
        raise NotImplementedError


    @abc.abstractmethod
    def help(self):
        u'''
        :return: ヘルプ表示用文字列
        '''
        raise NotImplementedError



class HelpCommand(CommandBase):


    def __call__(self, skype, evt, args):

        if len(args) < 1:
            evt.send('usage: $help command(without doller}')
            return

        name = args[0]

        cmds = skype.get_command_dispatcher().get_commands()

        c = cmds.get(evt.event)

        if c is None:
            evt.send('invalid command: %s' % name)
            return

        cmd = c.get(name)

        if cmd is None:
            evt.send('invalid command: %s' % name)
            return

        if not hasattr(cmd, 'help'):
            evt.send('command help not found')
            return

        evt.send(cmd.help())


    def help(self):

        return 'help for command'



class CommandsCommand(CommandBase):


    def __call__(self, skype, evt, args):

        cmds = skype.get_command_dispatcher().get_commands()

        c = cmds.get(evt.event)

        if c is None:
            return

        fp = StringIO.StringIO()

        print >> fp
        print >> fp, 'Available commands:'

        for cmd in sorted(c.keys()):
            print >> fp, '-', cmd

        evt.send(fp.getvalue())


    def help(self):

        return 'list available commands'

