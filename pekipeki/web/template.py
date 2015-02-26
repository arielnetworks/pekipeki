#-*- coding:utf-8 -*-

import jinja2


def render(template, **params):

    loader = jinja2.PackageLoader('pekipeki.web', 'templates')
    env = jinja2.Environment(loader=loader)

    tmpl = env.get_template(template)

    return tmpl.render(**params)
