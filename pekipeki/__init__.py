#-*- coding:utf-8 -*-

__import__('pkg_resources').declare_namespace(__name__)

__version__ = '0.1.0'
__author__ = '@shomah4a'
__license__ = 'LGPL'

import sys
import time
import argparse

from . import config



def make_parser():
    u'''
    パーサ作る
    '''

    parser = argparse.ArgumentParser(description=u'skype bot ってやつ')
    parser.add_argument('--config-file', '-f', dest='config_file')

    return parser



def load_plugins():
    u'''
    プラグインロード
    '''

    from pekipeki import plugins, utils

    return utils.list_package_modules(plugins)



def init_plugins():
    u'''
    プラグイン初期化
    '''

    for mod in load_plugins():

        if hasattr(mod, 'initialize'):
            mod.initialize()



def get_name(mod):

    return mod.__name__.split('.')[-1]



def init_config():
    u'''
    コンフィグのセクション情報を追加する
    '''

    conf = config.ConfigSetting()

    for mod in load_plugins():

        def conf_addr(keys, defaults):
            conf.add_section(get_name(mod), keys, defaults)

        if hasattr(mod, 'init_config'):

            mod.init_config(conf_addr)

        if not conf.has_section(get_name(mod)):
            conf_addr([], {})


    return conf



def init_skype(skp, conf):
    u'''
    ハンドラを登録する
    '''

    from pekipeki import plugins, utils

    for mod in utils.list_package_modules(plugins):

        if not hasattr(mod, 'init_skype'):
            sys.stderr.write('skip {0}'.format(mod.__name__))
            continue

        sec = conf.get_section(get_name(mod))

        try:
            mod.init_skype(skp, sec)
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

    init_plugins()

    config_setting = init_config()

    conf = config.load_config(args.config_file, config_setting)

    conf.verify()

    skp = skype.init()

    init_skype(skp, conf)

    print 'start skyep bot'

    while 1:
        time.sleep(100)


