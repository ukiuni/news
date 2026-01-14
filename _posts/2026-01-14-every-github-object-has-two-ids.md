---
layout: post
title: "Every GitHub Object Has Two IDs - GitHubのオブジェクトは2つのIDを持っている"
date: 2026-01-14T00:30:15.155Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.greptile.com/blog/github-ids"
source_title: "Every GitHub Object Has Two IDs | Greptile Blog"
source_id: 46602591
excerpt: "GraphQLのnode IDをmsgpack復号でDBの数値IDに変換する実践ガイド"
image: "https://greptile.com/opengraph/opengraph-blog.webp"
---

# Every GitHub Object Has Two IDs - GitHubのオブジェクトは2つのIDを持っている
思わず確認したくなる！GraphQLの「node ID」とURLで見かける数値ID、その関係をたった数行のコードで解き明かす

## 要約
GitHubにはGraphQLが返す“node ID”（例: PRRC_kwDOL4aMSs6Tkzl8）と、URLやRESTで使われる整数の「データベースID」（例: 2475899260）があり、最新フォーマットのnode IDは内部でMessagePack化されていて末尾にデータベースIDを含む。これを復号すれば既存データを移行せずにリンク生成できる。

## この記事を読むべき理由
GraphQL中心の実装で「リンク生成」や「既存DBとの紐付け」に困った経験はありませんか？日本の開発現場でも、GitHubデータを使ったツールやCI連携、コードレビュー支援で同じ壁にぶつかります。短時間で確実に実用的な解法を得られます。

## 詳細解説
- 二つのID体系
  - legacy（古い）形式：base64でデコードすると "010:Repository2325298" のような文字列が出る。古いリポジトリや特定オブジェクトに残る。
  - 新形式（現行の多く）：「プレフィックス_」の後ろがbase64で、さらにMessagePackの配列をデコードすると [0, repository_db_id, object_db_id] のような構造が得られる。
- なぜ混在しているか
  - GitHubは段階的にID体系を移行しており、リポジトリ作成時期やオブジェクト種別でフォーマットが分かれる。そのためAPI利用者は両方を扱う必要がある。
- 実務での発見
  - node IDを単純にbase64デコードして下位32ビットを取り出すとデータベースIDが得られるケースが多い（短いハック）。ただし安全なのはMessagePackで配列を取り出す方法。
- 簡単な流れ
  1. node ID をプレフィックス（例: PRRC_）で分割
  2. base64デコード → MessagePack unpack
  3. 配列の末尾要素が目的のデータベースID

コード例（Python）:
```python
# python
import base64
import msgpack

def node_id_to_database_id(node_id: str) -> int:
    # node_id は "PRRC_kwDOL4aMSs6Tkzl8" のような形式
    prefix, encoded = node_id.split('_', 1)
    packed = base64.b64decode(encoded)
    arr = msgpack.unpackb(packed)
    return arr[-1]  # 多くのオブジェクトでは最後が DB ID
```

簡易ハック（下位32ビットを抽出）:
```python
# python
import base64

def node_id_to_db_via_bitmask(node_id: str) -> int:
    encoded = node_id.split('_', 1)[1]
    decoded = int.from_bytes(base64.b64decode(encoded), byteorder='big')
    return decoded & ((1 << 32) - 1)
```

注意点：
- legacyフォーマットには上の手法は当てはまらない。
- GitHub公式はnode IDを不透明（opaque）として扱うことを推奨しており、内部実装に依存するコードは将来壊れるリスクがある。

## 実践ポイント
- まずは msgpack を使って node ID をデコードしてみる（安全性が高い）。
- レガシーなリポジトリやユーザーオブジェクトに対する例外処理を用意する（両フォーマットを判定する簡単なデコード試行を入れる）。
- 既存DBを無理に移行する前に、上記デコードでリンクや表示を生成できるか検証する。
- 将来の保守のために、可能ならGraphQLのnode IDとRESTのデータベースIDの両方を保存しておく設計を検討する。
- 日本のCI/コードレビュー自動化ツールや社内ダッシュボードでGitHubリンクを生成する場合、メンテ性を考えて上記の「msgpackでの復号＋フォールバック」を実装しておくとトラブルを減らせる。

短いまとめ：GraphQLのnode IDは「見た目は不透明」だが解析すれば実用的にDB IDを取り出せる。移行やリンク生成で悩んだら、まずMessagePackデコードを試してみよう。
