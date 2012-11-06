#-*- coding:utf-8 -*-

from . import utils


event = utils.Enum('READ', 'RECEIVED', 'SENDING', 'SENT')
status = utils.Enum('CONTINUE', 'FINISH')

