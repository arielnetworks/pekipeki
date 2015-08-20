#-*- coding:utf-8 -*-

import time
import sched
import StringIO

from pekipeki import config, trac, utils


class ReportSetting(object):

    def __init__(self, report):

        sp = report.split(',')

        self.title = sp[0]
        self.report = sp[1]
        self.skype_room = sp[2]
        self.columns = sp[3:]


    def get_title(self):
        return self.title

    def get_report(self):
        return self.report

    def get_skype_room(self):
        return self.skype_room

    def get_columns(self):
        return self.columns



def get_previous_reports(context):

    return context.get('previous', {})


def set_previous_reports(context, reports):

    context['previous'] = reports


def parse_report(reports):

    return dict((r['ticket'], r) for r in reversed(reports))



def push_report(skp, tr, setting, report):

    fp = StringIO.StringIO()

    tid = report['ticket']

    ticket = tr.get_ticket(tid)

    print >> fp, u'report from:', setting.get_title().decode('utf-8')
    print >> fp, u'summary:', ticket.get('summary')
    print >> fp, tr.get_ticket_url(tid)

    for col in setting.get_columns():

        if col not in report:
            continue

        print >> fp, col+u':', report[col]
        print >> fp

    value = fp.getvalue()
    room = setting.get_skype_room()

    skp.get_chat(room).send_message(value)



def check_report(skp, tr, setting, context):
    u'''
    レポート増えてたらチェック
    '''

    reports = parse_report(tr.get_report(setting.get_report()))

    prev = get_previous_reports(context)

    for ticket, report in reports.iteritems():

        if ticket in prev:
            continue

        push_report(skp, tr, setting, report)

    set_previous_reports(context, reports)



def run(skp, tr, settings, interval):

    sc = sched.scheduler(time.time, time.sleep)

    for setting in settings:
        utils.loop_event(sc, interval, check_report, skp, tr, setting, {})

    sc.run()



def parse_reports(reports):

    return [ReportSetting(x.strip()) for x in reports.strip().splitlines()]



def init_config(conf_addr):

    keys = ['reports', 'interval']
    conf_addr(keys, {})



def init_skype(skp, conf):
    u'''
    trac 用初期化
    '''

    # trac プラグインの設定から拝借
    tc = config.get_config('trac')

    tr = trac.Trac(tc.get('url'),
                   tc.get('realm'),
                   tc.get('user'),
                   tc.get('password'))

    interval = int(conf.get('interval'))
    reports = parse_reports(conf.get('reports'))

    utils.spawn(run, skp, tr, reports, interval)
