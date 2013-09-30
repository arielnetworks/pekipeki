==========
 PEKIPEKI
==========

PEKIPEKI is a bouldering gym in Shibuya.

必要なもの
==========

- Python 2.7


使い方
======

- config.ini.in をコピー
- 設定

- python bootstrap.py -d

  - bootstrap.py は http://downloads.buildout.org/1/bootstrap.py

- bin/buildout
- bin/skypebot --config-file=config.ini

  - 設定ファイルは任意


拡張方法
========

- pekipeki/handlers 以下に .py を置いておくと勝手に読み込む
- 読み込んだモジュールに `register_handlers(skp, args)` 関数があるとそれを呼ぶ

  - pekipeki/handlers/misc.py でも見てください


設定色々・機能色々
==================

trac
----

設定
~~~~

こんな感じで設定する。

.. code-block:: ini

   [trac]
   url = http://url.to/trac/root
   user = trac_user
   password = trac_password
   realm = trac_realm

機能
~~~~

- 発言に ``#12345`` とか入っていると trac にアクセスしてチケットのサマリとURLを書き込む
- 発言に ``r12345`` とか入っていると trac のリビジョンの URL を書き込む

みたいな。


log
---

ログとって検索します。

設定
~~~~
こんなかんじ。

db_uri は sqlalchemy に食わせる URI。
echo は実行した SQL を表示するかどうか。

.. code-block:: ini

   [log]
   db_uri = sqlite:///skype_log.db
   echo = True


機能
~~~~
``$search 文字列`` で検索


jenkins
-------

jenkins のビルドがこけたら通知します。

設定
~~~~

こんな感じ。

targets は改行区切りで ${jenkinsのジョブURL}, ${skypeの部屋名} を書いていく。

interval はチェック間隔(秒)


.. code-block:: ini

   [jenkins]
   targets =
        http://path.to.jenkins/job/name/, #skype/chat/name
        http://path.to.jenkins/job2/name/, #skype/chat2/name
   interval = 600


機能
~~~~

こけたら書きこまれます


misc
----

設定
~~~~

ありません

機能
~~~~

- ぬるぽをｶﾞｯする
- 「〇〇たく」という発言に拝承する

