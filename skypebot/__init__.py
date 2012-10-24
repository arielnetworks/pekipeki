#-*- coding:utf-8 -*-
__import__('pkg_resources').declare_namespace(__name__)

__version__ = '0.1.0'
__author__ = '@shomah4a'
__license__ = 'LGPL'

import time


def main():
    u'''
    メイン
    '''

    from skypebot import skype

    skp = skype.init()

    print 'start skyep bot as', skp.skype.User().FullName

    while 1:
        time.sleep(100)


