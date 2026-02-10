---
layout: post
title: "Better Python tests with inline-snapshot - inline-snapshotでより良いPythonテスト"
date: 2026-02-10T04:34:45.679Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pydantic.dev/articles/inline-snapshot"
source_title: "Better Python tests with inline-snapshot | Pydantic"
source_id: 1423263295
excerpt: "inline-snapshotで期待値を自動埋め込み、Pythonテストの保守と差分確認を高速化"
image: "https://pydantic.dev/articles/inline-snapshot/og.png"
---

# Better Python tests with inline-snapshot - inline-snapshotでより良いPythonテスト
もう手動で期待値を更新しない：inline-snapshotでPythonテストが劇的に楽になる

## 要約
inline-snapshotを使うと、テスト内に空のスナップショットを書くだけでpytest実行時に期待値が自動でソースコードに埋め込まれ、複雑なデータ構造のテスト保守が格段に楽になります。

## この記事を読むべき理由
日本の開発チームでも、AIやWebサービスの仕様変更でテスト期待値の更新が頻発します。inline-snapshotは手作業を減らし、レビューやCIでの差分確認をシンプルにするため、生産性と品質の両方を改善します。

## 詳細解説
- 問題点：個別フィールドでassertを書くと冗長、全体比較にしても値が増えれば全テストを手動更新する必要がある。外部スナップショット（syrupy等）は可読性の分離を招く。
- 解法（inline-snapshot）：テストでまず空のスナップショットを置く。
```python
from inline_snapshot import snapshot

def test_user_creation():
    user = create_user(id=123, name="test_user")
    assert user.dict() == snapshot({})
```
- 実行するとソースが書き換えられ、期待値が直接埋め込まれる。更新は次で自動適用：
```bash
pytest --inline-snapshot=fix
```
- 動的データの扱い：timestampや乱数IDはnormalizeしてからスナップショットするか、dirty-equalsのIsInt/IsNowなどを使って条件マッチにする。
```python
from dirty_equals import IsInt, IsNow

assert user.dict() == snapshot({
    "id": IsInt(),
    "created_at": IsNow(),
    "name": "test_user",
})
```
- 型付きオブジェクトの扱い：pydanticのTypeAdapterを使い再帰的に組み込み型へ変換しておくと、コンストラクタ変更でテストが無駄に壊れるのを防げる。
```python
from pydantic import TypeAdapter
_adapter = TypeAdapter(object)

def as_dicts(value: object):
    return _adapter.dump_python(value)
```
- ネストしたJSON文字列や特殊ケースはparse_inner_jsonのような正規化ユーティリティであらかじめパースしておくと相性が良い。
- 仕組み（裏側）：inline-snapshotは呼び出し位置を特定してソースを書き換えるためにexecutingライブラリを利用している。この手法により、ソース内でスナップショットを直接更新できる。

## 実践ポイント
- まずは試験的に1〜2ファイルに snapshot({}) を入れて pytest --inline-snapshot=fix を実行してみる。大量の期待値埋め込みが一度で生成できる。
- 動的フィールドは dirty-equals (IsInt/IsNow 等) で許容するか、as_dicts()/parse_inner_jsonで正規化してから比較する。
- Pydantic/Dataclassを多用するプロジェクトは TypeAdapter.dump_python を使って組み込み型に変換してから snapshot する。
- CIでは自動fixはしない運用がおすすめ（レビューで差分を確認）。必要ならローカルでfix→PR作成のフローにする。
- 依存：inline-snapshot / dirty-equals / pydantic_core(or json) / executing。OSSメンテナの支援も活発なので商用利用でのスポンサー検討も一案。

この手法は日本企業の短いリリースサイクルやAI系プロダクトの頻繁な仕様変更にも合致します。まずは小さく試して効果を確かめてください。
