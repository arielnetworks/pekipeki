#-*- coding:utf-8 -*-

import unittest
import ConfigParser as configparser

from pekipeki import config


class TestConfig(unittest.TestCase):
    u'''
    設定のテスト
    '''

    def test_verify(self):
        u'''
        設定とファイルのチェック
        '''

        setting = config.ConfigSetting()
        setting.add_section('aaa', ['a', 'b', 'c'], dict(a=10, b=20))

        parser = configparser.ConfigParser()
        parser.add_section('aaa')

        c = config.Config(parser, setting)

        c.verify()

        parser.add_section('bbb')

        with self.assertRaises(ValueError):
            c.verify()

        parser = configparser.ConfigParser()
        parser.add_section('aaa')
        parser.set('aaa', 'b')

        c = config.Config(parser, setting)

        c.verify()

        parser.set('aaa', 'd')

        with self.assertRaises(ValueError):
            c.verify()




    def test_config(self):
        u'''
        コンフィグ設定のテスト
        '''

        setting = config.ConfigSetting()

        setting.add_section('aaa', ['a', 'b', 'c'], dict(a=10, b=20))

        parser = configparser.ConfigParser()

        a = config.Config(parser, setting)

        s = a.get_section('aaa')

        self.assertEquals(s.get('a'), 10)

        with self.assertRaises(ValueError):
            a.get_section('bbb')


        with self.assertRaises(ValueError):
            a.get_section('aaa').get('dddd')

