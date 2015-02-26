#-*- coding:utf-8 -*-

from wsgiref import util

import webob

from . import base
from pekipeki.web import template



class ChatItem(object):

    def __init__(self, id, title):

        self.id = id
        self.title = title


class ChatList(base.ControllerBase):


    def GET(self, request):

        chats = self.skype.list_chat()
        chats = [ChatItem(x.get_id(), x.get_title()) for x in chats]

        resp = webob.Response()
        resp.content_type = 'text/html'
        resp.charset = 'utf-8'
        resp.text = template.render('chatlist.html', chatlist=chats)

        return resp



class Chat(base.ControllerBase):


    def get_chat(self, request):

        name = request.path_info
        chats = dict((x.get_id(), x.get_title())
                     for x in self.skype.list_chat())

        if name not in chats:
            return None

        return self.skype.get_chat(name)


    def GET(self, request):

        chat = self.get_chat(request)

        if not chat:
            return self.not_found(request)

        title = chat.get_title()
        name = chat.get_id()
        messages = chat.get_latest_messages(20)

        resp = webob.Response()
        resp.content_type = 'text/html'
        resp.charset = 'utf-8'
        resp.text = template.render('chat.html', title=title, id=name, messages=messages)

        return resp


    def POST(self, request):

        chat = self.get_chat(request)

        if not chat:
            return self.not_found(request)

        msg = request.params.get('message')

        if not msg:
            return self.bad_request(request)

        resp = webob.Response()
        resp.status = 303
        resp.location = util.request_uri(request.environ)

        chat.send_message(msg)

        return resp
