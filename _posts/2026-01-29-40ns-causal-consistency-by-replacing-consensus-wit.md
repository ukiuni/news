---
layout: post
title: "40ns causal consistency by replacing consensus with algebra - 合意を代数で置き換え、40nsの因果整合性"
date: 2026-01-29T05:19:15.038Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/abokhalill/cuttlefish"
source_title: "GitHub - abokhalill/cuttlefish: Coordination-free distributed state kernel"
source_id: 414712766
excerpt: "合意ではなく代数的不変量で因果整合性を40nsで実現、Rust実装で低遅延カーネル提供"
image: "https://opengraph.githubassets.com/14ceca927b4d6e594ebf4bee20fedd04aebe25af19beaa983c7b62a7963f6838/abokhalill/cuttlefish"
---

# 40ns causal consistency by replacing consensus with algebra - 合意を代数で置き換え、40nsの因果整合性
L1キャッシュ級の高速性で「整合性」を再定義する分散ステートカーネル — Cuttlefish が示す新しいトレードオフ

## 要約
Cuttlefish は「合意（consensus）ではなく代数的不変量で正しさを定義する」ことで、因果整合性をナノ秒オーダー（フルサイクルで約40ns）で実現する分散ステートカーネルです。通信／ロック／ヒープを避け、演算の可換性に基づいて協調を不要にします。

## この記事を読むべき理由
分散システムで低遅延かつ正確な整合性を求める日本のプロダクト（金融系マイクロサービス、IoTエッジ、ゲームサーバ、リアルタイム解析など）に対して、従来の1–50ms級の線形化書き込みとは異なる設計選択肢を提示します。実装はRustで公開されており、実ベンチマークや実験が可能です。

## 詳細解説
- コアアイデア：正しさを「代数的不変量（invariant）」として定義し、各操作がその不変量に対してどう作用するかを純関数で判定する。操作同士が可換（順序を変えても結果が等しい）なら協調（ロックや合意）は不要。
- 事実（Fact）：32バイトID、オプションの因果依存、ペイロードを持つ不変のステート遷移。事実はDAGを形成。
- 不変量（Invariant）：Δ_I(payload, state) → Result として定義され、O(1)、アロケーション不要、できる限り分岐を避ける実装を推奨。
- 因果クロック：512ビットのBloomフィルタを使った確率的ベクトルクロック（Bloom Clock）。優越判定が非常に速く（約700ps）飽和（40%超）したら正確トラッキングに切替。
  $$\Delta_I(a)\circ\Delta_I(b)=\Delta_I(b)\circ\Delta_I(a)$$
  が成り立てば協調不要。
- 性能（代表値）：フルアドミッションサイクル 40ns、カーネル単体アドミット（依存なし）13ns、25M causally-ordered ops/sec。耐久化経路は io_uring を使った非同期 fsync 等で高速化。
- 実装と制約：Rust実装。ホットパスでヒープ割当、ロック、システムコール（io_uring を除く）を禁止。ビット決定性（同入力は全ノードでバイト一致の出力）を重視。永続化機能は Linux の io_uring（カーネル 5.1+）が必要。
- 比較：etcd は線形化書き込みで一般に1–10ms、CockroachDB は1–50msを要する一方、Cuttlefish は因果＋代数的不変量ベースでナノ秒級を主張する。ただし用途は「カーネル（DBを作るための基盤）」であり、SQLや二次インデックス等の高レベル機能は提供しない。

## 実践ポイント
- 可換性を意識して不変量を設計する（合成可能な群・モノイド・ラティスを優先）。可換なら分散協調は不要。
- まずはリポジトリをクローンしてベンチを走らせる：`cargo bench`。永続化を試すなら io_uring（Linux 5.1+）環境を用意する。
- プロトタイプ用途：低遅延が重要なマイクロサービスやエッジノードのローカル整合カーネルとして有望。グローバルな総順序や高度なクエリは別レイヤで実装する設計を想定する。
- 小さな Rust サンプル（概念）：
```rust
use ctfs::prelude::*;
use ctfs::invariants::total_supply::{ConservationState, TotalSupplyInvariant};

let state = ConservationState::new(0i128, i128::MIN, i128::MAX);
let mut cell = StateCell::new();
cell.as_slice_mut().copy_from_slice(state.as_bytes());
let mut kernel = Kernel::with_state(TotalSupplyInvariant::new(), cell);
let fact_id: FactId = [0u8; 32];
let payload = 100i128.to_le_bytes();
kernel.admit_raw(&fact_id, &[], &payload).unwrap();
```

短所も明確：確率的時計の飽和点や限定的な機能セット、Linux/io_uring依存など運用上の制約があるため、用途をよく選ぶこと。興味があればリポジトリ（Rust実装）で手を動かして、どの不変量が自分のワークロードに合うか試してみると良い。
