#-*- coding:utf-8 -*-

import webdispatch

from webob import dec

from .controller import main, chat


def hello(environ, start_response):

    start_response('200 ok', [])

    return ['hello, world']



def make_application(skype, options):

    dispatcher = webdispatch.URLDispatcher()

    dispatcher.add_url('main', '/', dec.wsgify(main.Main(skype)))
    dispatcher.add_url('chatlist', '/chats/', dec.wsgify(chat.ChatList(skype)))
    dispatcher.add_url('chat', '/chats/*', dec.wsgify(chat.Chat(skype)))


    return dispatcher
