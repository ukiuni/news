---
layout: post
title: "A Couple Million Lines of Haskell: Production Engineering at Mercury - 数百万行のHaskell：Mercuryのプロダクション運用術"
date: 2026-03-30T22:11:23.075Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.haskell.org/a-couple-million-lines-of-haskell/"
source_title: "A Couple Million Lines of Haskell: Production Engineering at Mercury | The Haskell Programming Language's blog"
source_id: 410127988
excerpt: "数百万行のHaskellで金融システムを可観測・冪等・ロールバック可能に保つ実践運用術"
image: "https://blog.haskell.org/images/haskell-opengraph.png"
---

# A Couple Million Lines of Haskell: Production Engineering at Mercury - 数百万行のHaskell：Mercuryのプロダクション運用術
2百万行超のHaskellを金融サービスで動かす現場の「作り方」と「守り方」

## 要約
Mercuryが約2百万行のHaskellで大規模金融サービスを安定運用している実践知を共有する記事。言語の美しさだけでなく、運用・組織視点でどう信頼性を作るかに焦点を当てる。

## この記事を読むべき理由
日本でも金融・決済・大規模バックエンドを手がけるチームが増える中、実運用で有効な「型による作業の可視化」「不変条件を強制する設計」「運用上の境界の作り方」がそのまま役立つから。

## 詳細解説
- スケール感と前提  
  Mercuryは多数の非Haskell経験者を採用する組織で、コードベースは巨大。そこで問われるのは「個人の暗黙知」ではなく「組織が継続して扱える設計」。

- 信頼性の考え方：失敗防止ではなく適応能力  
  単にバグ列挙するのではなく、変化を吸収して劣化を段階的にする設計（graceful degradation）を重視。オペレータが理解しやすく、修正しやすいことを目標とする。

- 型システムを「運用ツール」として使う  
  Haskellの型は単なる正当性証明ではなく、運用手順（incantation）をコード化する手段。正しい手順を「唯一の実行経路」にしてしまえば、人為ミスを物理的に防げる。

- 純粋性は性質ではなく境界  
  実装内部でミューテーションや副作用があっても、境界（型）でそれを閉じ込めれば外部は純粋に扱える。runSTのようなパターンは小さな危険領域を型で隔離する良い例。

haskell
```haskell
runST :: (forall s. ST s a) -> a
```

- インターフェース設計で「正しい操作を最短経路にする」  
  トランザクションとイベント発行を分けて実装するとミスが起こる。代わりに、イベント発行を含む操作を不可分にしてしまえば、誤った使い方をコンパイル時に防げる。

haskell
```haskell
data Transact a -- 不透明にする
record :: Transaction -> Transact ()
emit :: Event -> Transact ()
commit :: Transact a -> IO a -- この経路しかコミット方法がない
```

- 長期実行処理と分散ワークフロー  
  金融処理は複数サービス・トランザクションを跨ぐため、可観測性・冪等性・ロールバック設計が必須。クラッシュや遅延時に局所的に吸収できる設計を心がける。

- 運用チームとの早期協働  
  安定性チームが設計初期に「blast radius」「どこを冪等にするか」「ロールバック手順」などを問うことで、後からの修正コストを下げる。

## 実践ポイント
- 重要な運用ルールはドキュメントだけでなく型で強制する（安全な経路を唯一にする）。  
- 不純性は完全否定せず「どこで生じるか」を明確にして境界で封じる。  
- 長期処理は可観測性・冪等性・ロールバックを最初から設計する。  
- 新人が読んで分かるモジュール設計を優先する（説明より型を頼る）。  
- 機能設計の初期に安定性チームと合意し、Blast radius/rollback/idempotency を定義する。

短く言えば：型を運用の友に変え、危険を狭い境界に閉じ込め、正しい手順を「書かないと進めない」形にする――これが大規模Haskellを現場で回す鍵です。
