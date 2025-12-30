---
layout: post
title: Beautiful reprs - 美しいrepr（表現）
date: 2025-12-26 11:24:59.247000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://pomponchik.org/notes/beautiful-reprs/
source_title: Beautiful reprs | blinov
source_id: 1102099719
excerpt: 再現性ある美しいrepr生成と機密マスクでログを安全にする小型ライブラリprinto
---
# Beautiful reprs - 美しいrepr（表現）

## 要約
REPLやログでオブジェクトが読みやすいことはライブラリの使い勝手を左右する。元記事は、再現可能で安全な __repr__ を自動生成する小さなライブラリ printo を紹介している。

## この記事を読むべき理由
日本の現場では、中央ログや監査系ストレージに出力される文字列から機密が漏れるリスクや、OSS/社内ライブラリの初見体験（REPLでの見え方）が製品品質に直結する。短い実装で「見た目」と「安全性」を両立できる手法は即戦力になる。

## 詳細解説
- __repr__ の役割
  - PythonのREPLやデバッグ出力はオブジェクトの __repr__ を使って文字列化する。理想的にはその文字列を eval すれば同じオブジェクトが得られる（再現可能性）。
  - 初心者に多いミス：単に f-string や str() を使って人間向けに整形してしまい、再現性やネスト表現が損なわれる点。正しくは内部の要素にも repr() を使って再帰的に表現する。

- printo の考え方（元記事の要点）
  - 名前は printo。主な関数 descript_data_object にクラス名・位置引数タプル・キーワード引数辞書を渡すと、再現可能な形式の文字列を返す。
  - デフォルトで各要素に repr() を使うため再帰的な表現となり、他のオブジェクトが同ルールを守っていれば出力はコードとして有効になる。
  - 追加機能：
    - placeholders：特定の引数の値をマスクして出力（ログや監査向けに機密を伏せる）。
    - filters：デフォルト値と同じなら出力を省くなど、表示するかどうかの条件を指定。
    - serializator（元記事は serializator）：特定値に対して独自ロジックで表示を変えるフック。

- 実務的注意点
  - dataclasses や attrs の自動 __repr__ とどう違うか：printo は「再現文字列のカスタム生成」と「マスク／フィルタ」を簡単に追加できる点が特徴。dataclass の repr を補完する用途に向く。
  - ログ出力ポリシーと併用して、マスクをチームルールにすることで機密漏洩リスクを下げられる。

## 実践ポイント
- インストールと基本利用
```python
# python
# pip install printo
from printo import descript_data_object

print(descript_data_object(
    'MyClassName',
    (1, 2, 'some text'),
    {'variable_name': 1, 'second_variable_name': 'kek'},
))
# -> MyClassName(1, 2, 'some text', variable_name=1, second_variable_name='kek')
```

- クラスの __repr__ に組み込む（簡単なパターン）
```python
# python
from printo import descript_data_object

class MyClass:
    def __init__(self, a, b=2, secret=None):
        self.a = a
        self.b = b
        self.secret = secret

    def __repr__(self):
        return descript_data_object(
            self.__class__.__name__,
            (self.a,),
            {'b': self.b, 'secret': self.secret},
            placeholders={'secret': '***'},  # ログに出したくない値をマスク
            filters={'b': lambda x: x != 2}   # デフォルトの b=2 は省略
        )
```

- ログ運用での実用例
  - 中央ログに送る前に placeholders を設定しておくと、開発者のミスや運用時の流出リスクを低減できる。
  - filters を使って冗長なデフォルト値を抑え、ログ行長を短く保つ。

