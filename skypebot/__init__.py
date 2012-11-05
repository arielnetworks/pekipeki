#-*- coding:utf-8 -*-
__import__('pkg_resources').declare_namespace(__name__)

__version__ = '0.1.0'
__author__ = '@shomah4a'
__license__ = 'LGPL'

import sys
import time
import argparse



def make_parser():
    u'''
    パーサ作る
    '''

    parser = argparse.ArgumentParser(description=u'skype bot ってやつ')
    parser.add_argument('--trac-url', dest='trac_url')
    parser.add_argument('--trac-realm', dest='trac_realm')
    parser.add_argument('--trac-username', dest='trac_user')
    parser.add_argument('--trac-password', dest='trac_password')

    return parser


def main():
    u'''
    メイン
    '''

    from skypebot import skype, handlers

    import socket
    socket.setdefaulttimeout(10)

    parser = make_parser()
    args = parser.parse_args(sys.argv[1:])

    skp = skype.init()

    handlers.register_handlers(skp, args)

    print 'start skyep bot'

    while 1:
        time.sleep(100)


