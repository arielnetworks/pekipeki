#-*- coding: utf-8 -*-

import webob


class ControllerBase(object):

    ALLOW_METHODS = {'GET', 'POST'}

    def __init__(self, skype):

        self.skype = skype


    def __call__(self, request):

        method = request.method

        if method not in self.ALLOW_METHODS:
            return self.not_found(request)

        return getattr(self, method)(request)


    def not_found(self, request):

        res = webob.Response()
        res.status = 404

        res.body = 'not found'

        return res


    def bad_request(self, request):

        res = webob.Response()
        res.status = 400

        res.body = 'bad request'

        return res



    def GET(self, request):

        return self.not_found(request)


    def POST(self, request):

        return self.not_found(request)
