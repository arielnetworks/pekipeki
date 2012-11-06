#-*- coding:utf-8 -*-

import unittest

from pekipeki import utils


class TestUtils(unittest.TestCase):

    def setUp(self):

        self.enum = utils.Enum('A', 'B', 'C', 'D')


    def test_enum(self):
        u'''
        列挙体っぽいなにかのテスト
        '''

        e = self.enum

        e.A
        e.B
        e.C
        e.D

        self.assertEquals(str(e.A), 'A')

        with self.assertRaises(AttributeError):
            e.F



    def test_iter(self):
        u'''
        列挙体を列挙してみる
        '''

        e = self.enum

        self.assertEquals(list(e),
                          [e.A, e.B, e.C, e.D])

        self.assertEquals(e.elements(),
                          [e.A, e.B, e.C, e.D])


    def test_contains(self):
        u'''
        含まれる
        '''

        e = self.enum

        self.assertIn(e.A, e)
        self.assertIn(e.B, e)
        self.assertIn(e.C, e)

        self.assertNotIn(1, e)



    def test_from_str(self):
        u'''
        文字列から変換してみる
        '''

        e = self.enum

        self.assertIs(e.from_str('A'), e.A)
        self.assertIs(e.from_str('B'), e.B)
        self.assertIs(e.from_str('C'), e.C)
        self.assertIs(e.from_str('D'), e.D)

        with self.assertRaises(AttributeError):
            e.from_str('E')



