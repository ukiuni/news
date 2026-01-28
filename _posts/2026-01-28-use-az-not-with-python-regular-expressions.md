---
layout: post
title: "Use “\A...\z”, not “^...$” with Python regular expressions - Python正規表現では \"^...$\" ではなく \"\A...\z\" を使おう"
date: 2026-01-28T16:03:41.097Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sethmlarson.dev/use-backslash-A-and-z-not-%5E-and-%24-with-python-regular-expressions"
source_title: "Use “\A...\z”, not “^...$” with Python regular expressions — Seth Larson"
source_id: 916996568
excerpt: "末尾改行で誤判定する^...$の罠と\A...\z／fullmatchで全体一致を安全に検証"
image: "https://github.com/sethmlarson.png"
---

# Use “\A...\z”, not “^...$” with Python regular expressions - Python正規表現では "^...$" ではなく "\A...\z" を使おう
末尾の改行に騙されない正規表現テク — Pythonで文字列全体を正確にマッチさせる方法

## 要約
Pythonでは`^...$`が期待どおり「文字列全体」を表さず、末尾の改行を無視してマッチすることがある。真に文字列全体をマッチさせたいなら`\A...\z`（または古い版では`\Z`）や`re.fullmatch()`を使うべき、という話です。

## この記事を読むべき理由
ファイルや標準入力から読み込んだ文字列は末尾に改行を含むことが多く、テストやバリデーションで「見た目は同じでも不整合になる」バグの原因になります。日本の開発現場でもログ／設定／テスト周りで遭遇しやすい典型的な落とし穴です。

## 詳細解説
- ^ と $ は「行境界（line boundary）」を扱うアンカー：デフォルトで`$`は文字列の終端の直前の改行にもマッチします。したがってパターン`^Hello$`は`"Hello\n"`にもマッチします（多くの人が驚く点）。
- 絶対位置を指定するには `\A`（文字列開始）と `\z`（文字列終了）を使います。これらは行末の改行を無視せず「文字列の先頭・末尾」を厳密に表します。
- Python 3.14 から `\z` がサポートされ、以前は `\Z` が代替として使える（記事によれば `\Z` が `\z` のエイリアスとして動作していた）。ただし他の言語実装ではサポート状況や意味が異なるため移植時は注意が必要です（例：ECMAScript/Go/Rustでは未対応、PHP/Java/.NETでは挙動が違うことがある）。
- 代替手段として `re.fullmatch()` を使うと「パターンが文字列全体にぴったり一致するか」を簡潔にチェックできます。

簡単な例：
```python
python
import re

print(bool(re.match(r'^Hello$', 'Hello')))    # True
print(bool(re.match(r'^Hello$', 'Hello\n')))  # True ← ここが罠

print(bool(re.match(r'\AHello\z', 'Hello')))    # True
print(bool(re.match(r'\AHello\z', 'Hello\n')))  # False

print(bool(re.fullmatch(r'Hello', 'Hello\n')))  # False ← fullmatch でも安全
```

## 実践ポイント
- 文字列全体を正確にマッチさせたいなら、`re.fullmatch()` をまず検討する。
- 正規表現でアンカーを使うなら、行境界を避けて `\A...\z` を使う（古いPythonでは`\Z`が使えるがバージョン差に注意）。
- ライブラリや複数言語で同じ正規表現を使う場合は、各実装のアンカーの挙動差を確認する（移植性のチェックをルール化しておくと安心）。
- 単体テストやファイル入出力の検証では末尾改行の有無を明示的に扱う（stripするか、改行を期待するかを明確に）。

これだけ押さえれば、末尾改行に起因する微妙なマッチ不一致でハマる回数がぐっと減ります。
