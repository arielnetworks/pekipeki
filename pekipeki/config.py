#-*- coding:utf-8 -*-

import ConfigParser as configparser



class ConfigSection(object):
    u'''
    コンフィグのセクション定義
    '''

    def __init__(self, name, keys, defaults):

        self.name = name
        self.keys = keys
        self.defaults = defaults


    def get(self, key):

        if key not in self.keys:
            raise ValueError('option key not defined: {0}.{1}'.format(self.name, key))

        return self.defaults.get(key)


    def __getattr__(self, key):

        return self.get(key)



class ConfigSetting(object):
    u'''
    コンフィグの設定を定義する
    '''

    def __init__(self):

        self.sections = {}


    def add_section(self, name, keys, defaults):
        u'''
        セクションを追加する

        :param str name: セクション名
        :param keys: セクションのキー
        :type keys: list<str>
        :param defaults: デフォルト値
        :type defaults: map<str, object>
        '''

        self.sections[name] = ConfigSection(name, keys, defaults)


    def get(self, key):

        if key not in self.sections:
            raise ValueError('section not defined: ' + key)

        return self.sections.get(key)


    def has_section(self, key):

        return key in self.sections



class Section(object):
    u'''
    セクション
    '''

    def __init__(self, config, defaults, name):

        self.config = config
        self.defaults = defaults
        self.name = name


    def __get(self, f, key):

        errors = (configparser.NoSectionError,
                  configparser.NoOptionError)

        try:
            return f()
        except errors:
            return self.defaults.get(key)


    def get(self, key):

        def f():
            return '\n'.join([x.strip()
                              for x in self.config.get(self.name, key).splitlines()])

        return self.__get(f, key)


    def get_string(self, key):

        def f():
            self.config.get(self.name, key)

        return self.__get(f, key)


    def get_int(self, key):

        def f():
            return self.config.getint(self.name, key)

        return self.__get(f, key)


    def get_float(self, key):

        def f():
            return self.config.getfloat(self.name, key)

        return self.__get(f, key)



class Config(object):
    u'''
    コンフィグ
    '''

    def __init__(self, config, setting):

        self.config = config
        self.setting = setting


    def get_section(self, section):

        s = self.setting.get(section)

        return Section(self.config, s, section)


    def verify(self):

        sections = self.config.sections()

        for section in sections:

            try:
                sec = self.setting.get(section)
            except:
                if section != 'misc':
                    raise

            for option in self.config.options(section):
                sec.get(option)



def load_config(path, setting):
    u'''
    コンフィグファイルを読み込む
    '''

    global __global_config

    if path is None:
        return

    config = configparser.SafeConfigParser()

    config.read([path])

    conf = Config(config, setting)
    __global_config = conf

    return conf



def get_config(section):
    u'''
    グローバルの config から設定取得
    プラグインから他のプラグインの設定を読みたい時とか
    '''

    return __global_config.get_section(section)

