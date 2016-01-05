#-*- coding:utf-8 -*-
u'''
サービス用のインタフェイス的なの。
skype とか slack とかで使えるようにしたい
'''

from pekipeki import interfaces


class ServiceProxy(interfaces.Service):
    u'''
    サービス用のインタフェイスまとめ
    '''

    def __init__(self):

        self.services = []


    def add_service(self, service):

        self.services.append(service)


    def get_type(self):

        return 'proxy'


    def register_message_handler(self, ev, handler):
        u'''
        登録されたサービスすべてにメッセージハンドラを登録

        :param pekipeki.constants.event ev: イベントの種類
        :param function(pekipeki.services.interfaces.MessageEvent) handler: メッセージハンドラ
        '''

        for service in self.services:
            service.register_message_handler(ev, handler)


    def register_command_handler(self, ev, command, handler):
        u'''
        登録されたサービスすべてにコマンドハンドラを登録

        :param pekipeki.constants.event ev: イベントの種類
        :param str command: コマンド名
        :param function(MessageEvent) handler: コマンドハンドラ
        '''

        for service in self.services:
            service.register_command_handler(ev, command, handler)


    def get_chat(self, name):
        u'''
        チャットを取得

        :param str name: 部屋の名前
        :return: Chat
        '''

        for service in self.services:

            chat = service.get_chat(name)

            if chat is not None:
                return chat


    def list_chat(self):
        u'''
        チャットの一覧を取得

        :return: [Chat]
        '''

        return reduce(lambda x, y: x + y.list_chat(), self.services, [])


def init(conf):

    from . import skype, slack
    from pekipeki import utils

    proxy = ServiceProxy()

    for service in [slack, skype]:
        name = utils.get_name(service)
        s = service.init(conf.get_section(name))

        if s:
            proxy.add_service(s)
            print 'initialized service:', name

    return proxy
