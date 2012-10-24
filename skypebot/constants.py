#-*- coding:utf-8 -*-

from . import utils


event = utils.Enum('RECEIVED', 'SENT', 'SENDING')
status = utils.Enum('CONTINUE', 'FINISH')

