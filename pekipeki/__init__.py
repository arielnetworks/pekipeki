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



def register_handlers(skp, args):
    u'''
    ハンドラを登録する
    '''

    from pekipeki import handlers, utils

    for mod in utils.list_package_modules(handlers):

        if not hasattr(mod, 'register_handlers'):
            sys.stderr('skip {0}'.format(mod.__name__))

        try:
            mod.register_handlers(skp, args)
            print 'register handler plugin:', mod.__name__
        except KeyboardInterrupt:
            raise
        except:
            import traceback
            traceback.print_exc()



def main():
    u'''
    メイン
    '''

    from pekipeki import skype

    import socket
    socket.setdefaulttimeout(10)

    parser = make_parser()
    args = parser.parse_args(sys.argv[1:])

    skp = skype.init()

    register_handlers(skp, args)

    print 'start skyep bot'

    while 1:
        time.sleep(100)


