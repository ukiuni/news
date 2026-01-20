---
layout: post
title: "I decided to make a worse UUID for the pettiest of reasons. - 「つまらない理由で“より悪い”UUIDを作った話」"
date: 2026-01-20T04:18:43.063Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gitpush--force.com/commits/2026/01/meet-smolid/"
source_title: "I decided to make a worse UUID for the pettiest of reasons. | git push --force"
source_id: 422402491
excerpt: "8バイトの短縮UUID「smolid」—URL美化と時系列性を保ちつつ衝突リスクを実用視点で解説"
---

# I decided to make a worse UUID for the pettiest of reasons. - 「つまらない理由で“より悪い”UUIDを作った話」
魅力的な短いIDでURLを美しくするために、あえてUUIDを切り詰めた「smolid」という8バイトIDの紹介

## 要約
著者は標準UUIDを意図的に“悪く”して（短くして）学習と利便性を得る目的で、Go実装のsmolidを作った。短くURLフレンドリーで、タイムオーダ性や簡易型埋め込みなど実用的な妥協をしている。

## この記事を読むべき理由
- URLやログで見たときにIDが長すぎて煩わしいと感じる開発者に向く設計思想が学べる。  
- 「短さ」と「衝突確率（エントロピー）」のトレードオフを、実用的な数式と具体例で理解できる。  
- 日本のスタートアップや個人サービスでの採用可否を判断する材料になる。

## 詳細解説
smolidの要点（要約・意訳）
- サイズ：8バイト（uint64）。Postgresのbigintにそのまま格納できる設計。  
- 目的：短くURLに馴染む文字列（unpadded base32）で、時系列にソート可能、かつ「十分にユニーク」なIDを目指す。  
- 構成（合計64ビット）：  
  - タイムスタンプ（41ビット、ミリ秒精度） — エポックは 2025-01-01。有効範囲はおよそ 2025 ～ 2094。  
  - バージョン（2ビット） — 将来の互換性用。v1は `01`。  
  - タイプフラグ（1ビット） — 埋め込み型識別子の有無を示す。  
  - ランダム（計末尾で合計20ビット程度） — 残りビットは疑似乱数または型IDとして使われる。  
- 埋め込み型ID：v1では7ビットを型識別子に割り当てられ、ID自身から「これはユーザーID／投稿ID／コメントID」などを判別できる。  
- 実装面：Go向けにjson/textのマーシャラ／DBのValuer/Scanner実装が用意され、既存のUUIDライブラリに倣った扱いやすさを目指している。

設計上の主な妥協点と注意点
- エントロピー不足：16バイトのUUIDと違い衝突確率は上がる。smolidは「多くのユースケースで十分」だが、グローバル一意性を厳密に保証する用途（金融や高頻度分散生成）には不向き。  
- 時刻依存：タイムスタンプで衝突を軽減しているため、生成マシンの時計信頼性に依存する。NTPやクロックのジャンプに注意。  
- PostgreSQLの符号付き整数問題：bigintは符号付きのため、最上位ビットが反転する年（2059年付近）でインデックス順の扱いが変わるリスクがある（実運用での影響を要確認）。

衝突確率の概算（概念式）
- 1ミリ秒あたりの生成数を $n$、キー空間のサイズを $d$ とすると、そのミリ秒内での衝突確率は概ね
$$
p \approx 1 - e^{- \frac{n(n-1)}{2d}}
$$
- スパイクが $T$ ミリ秒続くとき総合確率は
$$
P = 1 - (1 - p)^T
$$
- 例：smolidの可用エントロピーが約 $2^{20}$（およそ百万）に相当するとして、1msあたり100件、1秒（1000ms）続く負荷では衝突確率が非常に高くなる（本文では約99%と試算）。対してUUIDv7（充分なエントロピー）なら事実上ゼロに近い衝突確率となる。

実務インパクトの読み替え
- ピークが数千件/秒以下、または生成元が単一サービスで時計が安定している用途ならsmolidは有効。  
- 大量並列生成や分散無調整環境ではUUIDv7などの標準仕様を選ぶべき。

簡単な利用例（Go）
```go
package blog

import (
  "context"
  "github.com/dotvezz/smolid"
)

const (
  TypeUser = iota
  TypePost
  TypeComment
)

type User struct {
  ID    smolid.ID
  Name  string
  Email string
}

func CreateUser(ctx context.Context, u User) (User, error) {
  u.ID = smolid.NewWithType(TypeUser)
  query := `insert into users (id, name, email) values ($1, $2, $3)`
  _, err := pool.Exec(ctx, query, u.ID, u.Name, u.Email)
  return u, err
}
```

（実装はオリジナルのGoライブラリに依存。適宜READMEとgodocを参照して下さい。）

## 実践ポイント
- 小〜中規模のウェブサービスで「短いURLが欲しい」「ログで識別しやすくしたい」なら試す価値あり。  
- 導入前に負荷テストでピーク時のID生成レートを確認する（$n$ を測って上の式で衝突リスクを評価）。  
- 型埋め込み機能は運用上便利だが、型数は128未満に抑えること。  
- DB列はbigintで保存できるが、2059年の符号ビット問題など長期互換の影響を理解しておく。  
- 分散環境・高スループットなら標準UUID（特にv7）を優先する判断を推奨。

参考：オリジナル記事（Ben Vezzani）の実装「dotvezz/smolid」。興味があればリポジトリと godoc を参照して実装の細部を確認してください。
