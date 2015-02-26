#-*- coding:utf-8 -*-

import webob

from . import base
from pekipeki.web import template


class Main(base.ControllerBase):


    def __init__(self, skype):
        self.skype = skype


    def GET(self, request):

        links = [
            ('chats', u'へやいちらん')
            ]

        resp = webob.Response()
        resp.content_type = 'text/html'
        resp.charset = 'utf-8'
        resp.text = template.render('main.html', links=links)

        return resp
