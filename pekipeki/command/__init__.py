#-*- coding:utf-8 -*-

import sys


class CommandDispatcher(object):


    def __init__(self):

        self.commands = {}



    def register_command(self, event, command, func):

        d = self.commands.get(event, {})
        self.commands[event] = d

        f = d.get(command)

        if f is not None:
            print >> sys.stderr, 'replace %s:%s from %s to %s' % (event, command, f, func)

        d[command] = func


    def dispatch_command(self, skype, ev, typ, command, args):

        d = self.commands.get(typ)

        if d is None:
            return

        cmd = d.get(command)

        if cmd is None:
            return

        cmd(skype, ev, args)



