#-*- coding: utf-8 -*-

from wsgiref import simple_server

from pekipeki import utils
from . import application



def start_server(skype, options):

    app = application.make_application(skype, options)
    server = simple_server.make_server('', 9000, app)

    utils.spawn(server.serve_forever)
