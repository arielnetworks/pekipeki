#-*- coding:utf-8 -*-

import StringIO

from pekipeki.constants import status, event
from pekipeki.log.model import tables, session
from pekipeki.log import functions



@session.with_transaction
def add_log(sess, id, user, message, chat, date):
    tables.create_log(sess,
                      id=id,
                      user=user,
                      message=message,
                      chat=chat,
                      time=date)


class DBLogger(object):

    def __init__(self, skype):

        self.skype = skype


    def add_log(self, evt):

        msg = evt.get_body()
        sender = evt.get_sender()

        add_log(evt.get_id(),
                sender.get_user_id(),
                msg,
                evt.get_chat_name(),
                evt.get_datetime())



@session.without_transaction
def search(sess, skype, event, args):

    print 'aaaaaaaaa'

    if len(args) < 1:
        event.reply('''Usage: $search ${username}''')
        return

    chat = event.get_chat_name()
    user = args[0]

    results = functions.search(sess, user, chat)

    if not results:
        event.send('not found')
        return

    fp = StringIO.StringIO()

    print >> fp, 'Search result: latest 20'

    for result in reversed(results):

        date = result.get('time')
        user = result.get('user')
        msg = result.get('message')

        print >> fp, ' ', '[%s] %s: %s' % (date.strftime('%Y/%m/%d %H:%M:%S'), user, msg)

    event.send(fp.getvalue())



def init_config(conf_addr):

    keys = ['db_uri', 'echo']
    defaults = dict(echo=False)

    conf_addr(keys, defaults)



def init_skype(skp, conf):

    if conf.get('db_uri') is None:
        return

    session.initialize(conf)

    logger = DBLogger(skp)

    skp.register_message_handler(event.RECEIVED, logger.add_log)

    skp.register_command_handler(event.RECEIVED, 'search', search)
    skp.register_command_handler(event.SENT, 'search', search)


