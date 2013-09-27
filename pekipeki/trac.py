#-*- coding:utf-8 -*-
u'''
trac を操作する系
'''

import urllib2
import urlparse
import csv



def _get_url(root):
    u'''
    http://host/path から http://host を得る
    '''

    result = urlparse.urlparse(root)

    url = '{0.scheme}://{0.hostname}'.format(result)

    if (result.port):
        url = url + ':' + str(url.port)

    return url + '/'



def _get_content_encode(resp):
    u'''
    Content-Type からエンコード情報を取ってくる
    '''

    typ = resp.headers.get('Content-Type')

    if typ is None:
        return 'ascii'

    values = typ.split('=')

    if len(values) > 1:
        return values[-1]

    return 'ascii'



class Trac(object):
    u'''
    trac をあれこれするためのクラス
    '''

    def __init__(self, root, realm, user, password):

        self.root = root.rstrip('/')
        self.user = user
        self.password = password
        self.realm = realm


    def make_opener(self):

        mgr = urllib2.HTTPPasswordMgr()
        mgr.add_password(self.realm, _get_url(self.root), self.user, self.password)
        handler = urllib2.HTTPBasicAuthHandler(mgr)

        return urllib2.build_opener(handler)


    def get_ticket(self, no):
        u'''
        チケット番号から情報を取得
        '''

        ticket_base = self.get_ticket_url(no)

        ticket_url = ticket_base + '?format=csv'

        opener = self.make_opener()

        data = opener.open(ticket_url)

        encode = _get_content_encode(data)

        reader = csv.DictReader(data)

        value = reader.next()

        return dict((k, v.decode(encode)) for k, v in value.iteritems())



    def get_ticket_url(self, no):
        u'''
        チケット番号から URL 生成
        '''

        ticket_url = '{0}/ticket/{1}'.format(self.root, no)

        return ticket_url


    def get_revision_url(self, no):
        u'''
        リビジョン番号から URL 生成
        '''

        revision_url = '{0}/changeset/{1}'.format(self.root, no)

        return revision_url


