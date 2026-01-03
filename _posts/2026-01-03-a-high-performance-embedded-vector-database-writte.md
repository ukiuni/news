---
  layout: post
  title: "A high performance embedded vector database written in rust - Rustで書かれた高性能組み込みベクトルデータベース"
  date: 2026-01-03T13:42:04.985Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/nubskr/satoriDB"
  source_title: "GitHub - nubskr/satoriDB: High performance embedded vector database"
  source_id: 472120285
  excerpt: "メモリ超え1B対応のRust製組み込みベクトルDB、SatoriDBで予測可能な高速検索"
  image: "https://opengraph.githubassets.com/be50301a87185ff92dfa64c17da88c899adf279ee2de2089f2d0d9c421a36d73/nubskr/satoriDB"
---

# A high performance embedded vector database written in rust - Rustで書かれた高性能組み込みベクトルデータベース
魅せる日本語タイトル: メモリ越え1B規模を狙うRust製「SatoriDB」──オンプレで高速＆予測可能なベクトル検索を実現する新星

## 要約
SatoriDBは、メモリ容量を超える大規模（数億〜10億規模）のベクトル検索を想定した組み込み型ベクトルDB。RAM上の小さなルーティング層とディスク上の並列スキャンで低遅延と高リコール（95%超）を両立することを狙うRust実装だ。

## この記事を読むべき理由
日本のSaaS/エンタープライズやオンプレ運用、データ主権を重視するプロダクトでは、外部クラウド依存を避けつつ大規模埋め込み検索を安定して運用できるソリューションが必要になる。SatoriDBは「プロセス内で動く」「ディスク主体でスケール」「予測可能なレイテンシ」という要件にフィットするため、RAGや大規模レコメンデーション基盤の選択肢として注目に値する。

## 詳細解説
- アーキテクチャ（2層構成）
  - Hot tier（ルーティング）: メモリ上に量子化されたHNSW（近傍探索グラフ）を保持し、クエリはまず上位Kのバケット（クラスタ）にルーティングされる。中心点は f32 → u8 のスカラー量子化で圧縮し、数十万スケールのバケットでもRAMに収まる設計。
  - Cold tier（スキャン）: 選択されたバケットのみをディスクから並列スキャン。GlommioベースのCPUピン留めワーカーが各自io_uringリング／LRUキャッシュ／プリ割当ヒープを持つ共有無しの設計で、クエリパス上のコア間同期を排除する。
- 性能最適化
  - SIMD経路（AVX2／AVX-512）を多用し、L2距離、内積、量子化、k-means割当てなど計算集約処理を高速化。
  - キャッシュミスはストリーミングでディスクから処理し、ブロッキングを避ける。
- 自動クラスタリングと再バランス
  - k-meansでベクトルをバケット化し、バックグラウンドで再バランサがバケットサイズが閾値（デフォルト約2000）を超えたら分割。バケットサイズの予測可能性がレイテンシ安定化に寄与する。
- ストレージ
  - Walrus: バケット単位のトピックでのappend-onlyストレージ（io_uring活用）。
  - RocksDB: IDによるポイントルックアップや重複検出用インデックス。
- 実測と制約
  - BigANNベンチで1B級データに対して95%超のリコール報告（デフォルト設定）。
  - Linux限定（io_uringが必須、kernel 5.8+）。AVX命令サポートがあるCPUで最大性能。
- APIと運用
  - 組み込みライブラリ（Rust crate）。プロセス内で動作し外部サービス不要。
  - 同期／非同期API、fsync間隔やワーカー数等を設定可能。耐久性は設定でトレードオフ調整。

簡単な利用例（ビルダーAPIのイメージ）:

```rust
use satoridb::SatoriDb;

fn main() -> anyhow::Result<()> {
    let db = SatoriDb::builder("my_app")
        .workers(4)
        .fsync_ms(100)
        .data_dir("/tmp/mydb")
        .build()?;
    db.insert(1, vec![0.1, 0.2, 0.3])?;
    let results = db.query(vec![0.15, 0.25, 0.35], 10)?;
    for (id, dist) in results { println!("id={} dist={}", id, dist); }
    Ok(())
}
```

## 実践ポイント
- 環境要件確認: Linux（kernel ≥ 5.8）、io_uringサポート、AVX2/AVX-512の有無を事前に確認する。クラウドVMでもホスト側カーネル要件に注意。
- 小規模から評価: まずはローカルや小規模データ（数万〜数百万）で挙動確認。BigANNのフルベンチは1TB級のディスクが必要でコストがかかる。
- パラメータチューニング:
  - SATORI_REBALANCE_THRESHOLD（デフォルト2000）でバケットサイズを調整し、レイテンシ安定性を確保。
  - workers や fsync_ms でスループット/耐久性のトレードオフを設定。
- ハードウェア最適化: NVMe + 高IOPSディスクとCPUのSIMD対応で性能が伸びる。メモリはルーティングとワーカーキャッシュ分を確保。
- 運用用途の検討: オンプレRAG、社内検索、ログ類似検索、レコメンドの高速サーバ内ストアとして導入検討。データ主権／低遅延要件がある日本企業には特に有用。
- 実装上の注意: 早期段階のプロジェクト（v0.1.x）でAPI変更の可能性あり。運用前に安定版と互換性を確認する。

短評：SatoriDBは「組み込みで、ディスク中心にスケールさせ、CPU最適化でレイテンシを抑える」アプローチを取る実践的なベクトルDB候補。オンプレ／エッジで大規模埋め込み検索を実現したい日本のプロジェクトは、まず小規模検証→ハードウェア最適化→運用試験の流れで評価する価値が高い。
