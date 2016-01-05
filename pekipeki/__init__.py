#-*- coding:utf-8 -*-

__import__('pkg_resources').declare_namespace(__name__)

__version__ = '0.1.0'
__author__ = '@shomah4a'
__license__ = 'LGPL'

import sys
import time
import itertools



def make_parser():
    u'''
    パーサ作る
    '''
    import argparse

    parser = argparse.ArgumentParser(description=u'skype bot ってやつ')
    parser.add_argument('--config-file', '-f', dest='config_file')

    return parser



def load_plugins():
    u'''
    プラグインロード
    '''

    from pekipeki import plugins, utils

    return utils.list_package_modules(plugins)



def load_services():
    u'''
    プラグインロード
    '''

    from pekipeki import services, utils

    return utils.list_package_modules(services)



def init_plugins():
    u'''
    プラグイン初期化
    '''

    for mod in load_plugins():

        if hasattr(mod, 'initialize'):
            mod.initialize()



def init_config():
    u'''
    コンフィグのセクション情報を追加する
    '''

    from . import config, utils
    conf = config.ConfigSetting()

    targets = itertools.chain(load_services(), load_plugins())

    for mod in targets:

        def conf_addr(keys, defaults):
            conf.add_section(utils.get_name(mod), keys, defaults)

        if hasattr(mod, 'init_config'):

            mod.init_config(conf_addr)

        if not conf.has_section(utils.get_name(mod)):
            conf_addr([], {})

    return conf



def init_handlers(skp, conf):
    u'''
    ハンドラを登録する
    '''

    from pekipeki import plugins, utils

    for mod in utils.list_package_modules(plugins):

        if not hasattr(mod, 'init_skype') and not hasattr(mod, 'init_handler'):
            sys.stderr.write('skip {0}\n'.format(mod.__name__))
            continue

        sec = conf.get_section(utils.get_name(mod))

        try:
            if hasattr(mod, 'init_skype'):
                mod.init_skype(skp, sec)
            elif hasattr(mod, 'init_handler'):
                mod.init_handler(skp, sec)

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
    from . import config
    from pekipeki import services

    import socket
    socket.setdefaulttimeout(10)

    parser = make_parser()
    args = parser.parse_args(sys.argv[1:])

    init_plugins()

    config_setting = init_config()

    conf = config.load_config(args.config_file, config_setting)

    conf.verify()

    skp = services.init(conf)

    init_handlers(skp, conf)

    while 1:
        time.sleep(100)
