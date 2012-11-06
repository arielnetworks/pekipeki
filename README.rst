==========
 PEKIPEKI
==========

PEKIPEKI is a bouldering gym in Shibuya.

必要なもの
==========

- Python 2.7


使い方
======

- python bootstrap.py -d

  - bootstrap.py は http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py

- bin/buildout
- bin/skypebot --trac-url=${trac_root_url} "--trac-realm=Trac Realm" --trac-user=${trac_username} --trac-password=${trac_pasword}

  - trac の設定は任意

拡張方法
========

- pekppeki/handlers 以下に .py を置いておくと勝手に読み込む
- 読み込んだモジュールに `register_handlers(skp, args)` 関数があるとそれを呼ぶ

  - pekppeki/handlers/misc.py でも見てください

