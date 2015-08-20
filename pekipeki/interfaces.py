#-*- coding:utf-8 -*-

import abc


class User(object):
    u'''
    送信者
    '''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_fullname(self):
        u'''
        ユーザのフルネームを取得
        '''


    @abc.abstractmethod
    def get_user_id(self):
        u'''
        ユーザIDを取得
        '''


    @abc.abstractmethod
    def get_display_name(self):
        u'''
        表示名を取得
        '''



class Message(object):
    u'''
    通知されたメッセージ
    '''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_date(self):
        u'''
        送信された時刻を取得
        '''


    @abc.abstractmethod
    def get_body(self):
        u'''
        メッセージ本文を取得
        '''


    @abc.abstractmethod
    def get_sender(self):
        u'''
        送信者を取得
        '''


class Chat(object):
    u'''
    部屋
    '''

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def send_message(self, msg):
        u'''
        部屋にメッセージを送る
        '''


    @abc.abstractmethod
    def get_id(self):
        u'''
        部屋のIDを取得
        '''


    @abc.abstractmethod
    def get_title(self):
        u'''
        部屋のタイトルを取得
        '''


    @abc.abstractmethod
    def get_latest_messages(self, count=20):
        u'''
        最新のメッセージを取ってくる
        オプションで取得する数を渡せる
        '''


class MessageEvent(object):
    u'''
    メッセージが来た時に渡されるイベント
    '''

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def get_id(self):
        u'''
        メッセージ ID を取得
        '''


    @abc.abstractmethod
    def get_body(self):
        u'''
        本文を取得
        '''


    @abc.abstractmethod
    def get_sender(self):
        u'''
        送信者を取得
        '''


    @abc.abstractmethod
    def reply(self, text):
        u'''
        イベントを起こした人に返信する
        '''


    @abc.abstractmethod
    def send(self, text):
        u'''
        部屋にメッセージを送る
        '''


    @abc.abstractmethod
    def get_chat_name(self):
        u'''
        部屋の名前を取得
        '''


    @abc.abstractmethod
    def get_datetime(self):
        u'''
        送信日時を取得
        '''


class Service(object):
    u'''
    Skype とか Slack とか用のインタフェイス
    '''

    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def get_type(self):
        u'''
        サービスタイプを文字列で返す
        '''


    @abc.abstractmethod
    def register_message_handler(self, ev, handler):
        u'''
        イベントハンドラを追加

        :param pekipeki.constants.event ev: イベントの種類
        :param function(pekipeki.services.interfaces.MessageEvent) handler: メッセージハンドラ
        '''

    @abc.abstractmethod
    def register_command_handler(self, ev, command, handler):
        u'''
        コマンドハンドラを追加

        :param pekipeki.constants.event ev: イベントの種類
        :param str command: コマンド名
        :param function(MessageEvent) handler: コマンドハンドラ
        '''


    @abc.abstractmethod
    def get_chat(self, name):
        u'''
        チャットを取得

        :param str name: 部屋の名前
        :return: Chat

        '''


    @abc.abstractmethod
    def list_chat(self):
        u'''
        チャットの一覧を取得

        :return: [Chat]
        '''
