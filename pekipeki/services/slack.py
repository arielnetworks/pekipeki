#-*- coding: utf-8 -*-
u'''
slack 用の何か
'''

import urllib2
import json

from pekipeki import constants
from pekipeki.constants import event
from pekipeki import command
from pekipeki.command import commands
from pekipeki import interfaces



class IncomingWebhook(interfaces.Chat):
    u'''
    incoming webhook でメッセージを送る
    '''

    def __init__(self, url):
        self.hook_url = url


    def send_message(self, msg):
        u'''
        部屋にメッセージを送る
        '''

        payload = json.dumps(dict(text=msg))

        urllib2.urlopen(self.hook_url, payload)


    def get_id(self):
        u'''
        部屋のIDを取得
        '''

        return self.hook_url


    def get_title(self):
        u'''
        部屋のタイトルを取得
        '''

        return self.hook_url


    def get_latest_messages(self, count=20):
        u'''
        最新のメッセージを取ってくる
        オプションで取得する数を渡せる
        '''

        return []



class Slack(interfaces.Service):
    u'''
    Slack 用のインタフェイス
    '''

    def get_type(self):

        return 'slack'


    def register_message_handler(self, ev, handler):
        u'''
        イベントハンドラを追加

        :param pekipeki.constants.event ev: イベントの種類
        :param function(pekipeki.services.interfaces.MessageEvent) handler: メッセージハンドラ
        '''

    def register_command_handler(self, ev, command, handler):
        u'''
        コマンドハンドラを追加

        :param pekipeki.constants.event ev: イベントの種類
        :param str command: コマンド名
        :param function(MessageEvent) handler: コマンドハンドラ
        '''


    def get_chat(self, name):
        u'''
        チャットを取得

        :param str name: 部屋の名前
        :return: Chat
        '''

        # incoming webhook
        if name.startswith('http://') or name.startswith('https://'):
            return IncomingWebhook(name)



    def list_chat(self):
        u'''
        チャットの一覧を取得

        :return: [Chat]
        '''

        return []


def init():

    return Slack()
