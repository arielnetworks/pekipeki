#-*- coding:utf-8 -*-

import setuptools
import pekipeki as pkg

pkgname = pkg.__name__

setuptools.setup(
    name=pkgname,
    version=pkg.__version__,
    packages=[pkgname],
    install_requires=[
        'Skype4Py',
        'lxml',
        'tweepy',
        'sqlalchemy',
        'PyMySQL',
        ],
    author=pkg.__author__,
    license=pkg.__license__,
    long_description=pkg.__doc__,
    entry_points=dict(
        ),
    classifiers='''
Programming Language :: Python
Development Status :: 2 - Pre-Alpha
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Programming Language :: Python :: 2
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Utilities
'''.strip().splitlines())

