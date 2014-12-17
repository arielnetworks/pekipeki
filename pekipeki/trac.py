#-*- coding:utf-8 -*-
u'''
trac を操作する系
'''

import urllib
import urllib2
import urlparse
import csv
import StringIO

try:
    import json
except ImportError:
    import simplejson as json



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



def _remove_bom(fp):
    u'''
    BOM がついているらしいので消す
    '''

    data = fp.read()
    
    return StringIO.StringIO(data.lstrip('\xef\xbb\xbf'))


class Trac(object):
    u'''
    trac をあれこれするためのクラス
    '''

    def __init__(self, root, realm, user, password):

        self.root = root.rstrip('/')
        self.user = user
        self.password = password
        self.realm = realm

        self.rpc = RPCMaker(self)


    def make_opener(self):

        mgr = urllib2.HTTPPasswordMgr()
        mgr.add_password(self.realm, _get_url(self.root), self.user, self.password)
        handler = urllib2.HTTPBasicAuthHandler(mgr)

        return urllib2.build_opener(handler)


    def make_url(self, url):

        return '{0}/{1}'.format(self.root, url.lstrip('/'))


    def post(self, url, data, content_type='text/plain'):

        url = self.make_url(url)
        opener = self.make_opener()

        req = urllib2.Request(url, data)
        req.add_header('Content-type', content_type)

        data = opener.open(req)
        encode = _get_content_encode(data)

        body = data.read().decode(encode)

        return body


    def get_ticket(self, no):
        u'''
        チケット番号から情報を取得
        '''

        ticket_base = self.get_ticket_url(no)
        ticket_url = ticket_base + '?format=csv'

        opener = self.make_opener()
        data = opener.open(ticket_url)
        encode = _get_content_encode(data)
        reader = csv.DictReader(_remove_bom(data))

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


    def get_report_url(self, no):
        report_url = '{0}/report/{1}'.format(self.root, no)
        return report_url


    def get_report(self, no, each=100, page=1):
        u'''
        保存されたレポートを取得する
        '''

        report_url = self.get_report_url(no)

        param = dict(format='csv', max=each, page=page)
        geturl = report_url + '?' + urllib.urlencode(param)

        opener = self.make_opener()
        data = opener.open(geturl)
        encode = _get_content_encode(data)
        reader = csv.DictReader(_remove_bom(data))

        return [dict((k, v.decode(encode)) for k, v in value.iteritems())
                for value in reader]


class RPCMaker(object):

    def __init__(self, trac):

        self.trac = trac


    def __getattr__(self, name):

        return RPC(name, self.trac)



class RPC(object):
    u'''
    Trac の rpc のためのもの
    '''

    def __init__(self, name, trac):

        self.name = name
        self.trac = trac


    def __getattr__(self, name):

        mname = self.name + '.' + name

        return RPC(mname, self.trac)


    def __call__(self, *params):

        param = dict(method=self.name,
                     params=params)
        jsonstr = json.dumps(param)

        url = 'login/jsonrpc'
        data = self.trac.post(url, jsonstr, 'application/json')

        return json.loads(data)

