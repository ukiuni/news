---
layout: post
title: "Go Made Me Fast. Rust Made Me Care. AWS Made Me Pay. - Goは速さをくれ、Rustは気を遣わせ、AWSは請求書を見せつけた"
date: 2026-02-13T13:34:09.316Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/art_light/go-made-me-fast-rust-made-me-care-aws-made-me-pay-2f82"
source_title: "Go Made Me Fast. Rust Made Me Care. AWS Made Me Pay. - DEV Community"
source_id: 3240298
excerpt: "Goで迅速に出し、Rustで効率化し、AWSの請求で現実を知る運用の教訓。"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fvloswy13v4nzij0o8khx.png"
---

# Go Made Me Fast. Rust Made Me Care. AWS Made Me Pay. - Goは速さをくれ、Rustは気を遣わせ、AWSは請求書を見せつけた
Goで高速に出荷し、Rustで効率と可視性を取り戻し、AWSの請求書で現実を知った話 — 「速さ」→「効率」→「コスト」の教訓

## 要約
Goは開発スピードと運用の安定感を与えるが、クラウドでは小さな無駄が積み重なって請求に現れる。Rustは効率を強制し、コストやレイテンシの予測性を改善する。最適解は用途に応じた言語配置と可観測性の徹底。

## この記事を読むべき理由
日本のスタートアップやSRE/バックエンドエンジニアは、短期の開発速度と長期のクラウドコストのトレードオフを避けられない。言語選択が技術的な美学だけでなく運用コストに直結する点を、実例を踏まえて理解できる。

## 詳細解説
- Goの強み
  - コンパイルが速く、単純な並行モデルと豊富な標準ライブラリで開発効率が高い。
  - 小さなバイナリはLambdaやコンテナのコールドスタートに有利。オンコール運用も「退屈な失敗」が多く扱いやすい。
- クラウドでの「ゆっくり来る罰」
  - 個々は小さな判断（+10% CPU、+200MBメモリ、余分なインスタンス）が累積して請求額を押し上げる。
  - GoのGCは低レイテンシだが追加のメモリ・CPUヘッドルームを要求し、コンテナ密度低下や早期水平スケールの原因になる。
- Rustがもたらす変化
  - Rustは「速い」だけでなく、メモリ配置・所有権・アロケーションを明示的に扱わせることで設計を変える。
  - 高スループット、ストリーミング、CPUバウンドな熱い経路でメモリ使用とレイテンシが安定し、より小さなインスタンスタイプや高いコンテナ密度が可能に。
  - 初期コスト（開発時間・学習曲線）は高いが、運用での予測性が向上する。
- AWSでの実例的差分
  - EC2/ECS/EKS：Rustはより高いパック率、OOM減少、安定したスケーリング特性を実現。
  - Lambda：Goよりもメモリ対性能比がよく、コールドスタートとコストで有利になるケースがある。
- 運用と観測
  - メトリクス（メモリ曲線、ティールレイテンシ、CPU飽和度、スケール挙動）が最終的に差を暴露する。
  - 言語は価値観をコード化する（Go＝高速出荷、Rust＝正確性・効率、AWS＝利用率に厳しい課金）。

## 実践ポイント
- 初期はGoで迅速にプロダクトを出し、トラフィックやコストが伸びてきたら「物理的に重い」箇所をRustで書き換える。
- 対象に応じた言語配置：APIやビジネスロジックはGo、データ取り込み/ストリーミング/Hot pathはRust。
- observabilityを最初から整備：メモリ使用、tail latency、コンテナ密度を継続監視して「請求のサイン」を早期検出。
- AWSのコスト構造を理解し、垂直効率（より少ないインスタンスでより多く処理）を優先する設計を検討。
- 小さな最適化を積み重ねる（バッファ再利用、ストリーミング処理、明示的なアロケーション削減）が大きな請求削減に直結する。

以上。
