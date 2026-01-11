---
layout: post
title: "Sophisticated Simplicity of Modern SQLite - モダンSQLiteの洗練されたシンプルさ"
date: 2026-01-11T21:59:29.817Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shivekkhurana.com/blog/sqlite-in-production/"
source_title: "Sophisticated Simplicity of Modern SQLite"
source_id: 430503763
excerpt: "SQLiteをWALやPRAGMA調整で本番運用可能にする実践チューニング指南"
image: "https://shivekkhurana.com/img/content/posts/sqlite-benchmarks.png"
---

# Sophisticated Simplicity of Modern SQLite - モダンSQLiteの洗練されたシンプルさ
小さなDBで大きな効果を出す：本番系でSQLiteを速く安全に動かすための実践チューニングガイド

## 要約
SQLiteは「古いデフォルト設定」から現代ハードに合わせてチューニングすれば、中〜小規模アプリでネットワークDBに引けを取らない性能を発揮する。本記事はベンチマークに基づく実用的な設定とトレードオフをまとめる。

## この記事を読むべき理由
日本のスタートアップや社内ツール、多くのローカル開発ワークフローでは、簡素な運用・高速なデプロイが重視される。Postgresのフル運用が負担になる場面で、SQLiteを安全かつ実用的に使う手法はすぐに役立つ。

## 詳細解説
- 背景と狙い  
  SQLiteは2004年設計のまま後方互換性を強く保っているため、デフォルト設定は当時のハード想定（回転ディスクなど）になっている。SSDや高コアCPUが一般化した現在は、設定（PRAGMA）を現代基準に合わせることで「同一マシン内の組み込みDB」として非常に強力に使える。

- 実験の前提  
  著者はブログ型スキーマ（Users, Posts, Tags）と現実的なクエリ群を用い、Node.js + PiscinaでマルチプロセスのWebサーバを模してベンチマーク。マシンは8コア（論理16スレッド）/32GBのMacBookで、実ワークロードに近い混合読書き（例：80%読／20%書）を想定している。

- 主要な挙動と問題点  
  SQLiteは「シングルライタ・マルチリーダ」設計。デフォルトのDELETEジャーナルや短い busy_timeout のままだと、並列書き込みで即座にロックエラーが発生する。書き込み比率が20%以下なら良好だが、それ以上ではチューニングが必須。

- 有効なチューニング（理由と効果）
  1. PRAGMA busy_timeout = 5s–10s  
     - ロック時にリトライする待機時間を伸ばし、lock errors を減らす。5〜10秒が実運用で妥当な目安。
  2. PRAGMA journal_mode = WAL（Write-Ahead Logging）  
     - 書き込みを *.wal へ順次追記し、読者はメインDB + WALから一貫したビューを読む。結果として読者はブロックされず、複数ライタ環境で書き込みレイテンシとスループットが大幅改善（複数接続では p99 が30〜60%改善した例あり）。
  3. PRAGMA synchronous = NORMAL  
     - WALと組み合わせると、fsync をトランザクション経路から外し若干の耐久性（最後数msのコミットが失われる可能性）を犠牲にして速度向上。Web APIやキャッシュ、イベント取込系ではNORMALが推奨される。厳密に最後のコミットも失えないならFULLを選択。
  4. PRAGMA wal_autocheckpoint = 4000（例）  
     - チェックポイント（WAL→DB）頻度を下げて書き込み性能を平滑化。チェックポイントは少なめの頻度（大きめの閾値）でまとめて実行すると効率的だが、WALが大きくなると読者への負担が増える点に注意。
  5. PRAGMA mmap_size = 1073741824（1GB） & PRAGMA temp_store = MEMORY  
     - MMAPでファイルをメモリ空間にマップし syscalls を削減、temp_store をメモリにして一時構造のディスクI/Oを回避。読み主体や複雑クエリで有効（メモリに余裕があることが前提）。

- ベンチマークからの洞察  
  - WAL有効化で、2接続以上の並列書き込み時に劇的な改善。1～2接続では逆に劣化するケースもあるため、接続数とワークロード特性を基に判断すること。  
  - 書き込み比率が低い（例：20%未満）ならSQLiteは非常に有力。高頻度の書き込み中心なら専用サーバDBも検討する。

## 実践ポイント
- まずやること（安全で効果的）
  - busy_timeout を 5000–10000 ms に設定する。例: PRAGMA busy_timeout = 5000;
  - journal_mode を WAL に切り替える。例: PRAGMA journal_mode = WAL;
  - synchronous を NORMAL に設定（用途によっては FULL）。例: PRAGMA synchronous = NORMAL;

- 追加改善（環境に合わせて）
  - wal_autocheckpoint を 2000–4000 に調整してチェックポイント頻度を下げる。負荷試験で WAL サイズと読者レイテンシを観察すること。
  - mmap_size を増やす（例: 1GB）と読み負荷でCPU/syscallを削減。メモリ余裕があるか確認する。
  - temp_store = MEMORY にして一時作業をRAMで処理する。

- 運用と運用ツール
  - バックアップとレプリケーションには Litestream 等を検討（ファイルベースDBはファイル保護が重要）。  
  - モニタリング指標：lock errors（SQLiteエラー）、WALサイズ、P99レイテンシ、IOPS、fsync時間。  
  - 本番投入前に実ワークロードに近い負荷テストを必ず行う（マルチプロセス/多スレッド実行を模す）。

- いつPostgres等に移すべきか（判断基準）
  - 地理的分散やマルチリージョン、数百万ユーザー規模のスループット、複雑な並列トランザクションが必須なら移行を検討。  
  - 移行は成功の一つの指標にすべきで、まずはSQLiteで迅速に価値を出す選択も合理的。

短くまとめると：SQLiteは「チューニングすれば強い」。WAL + busy_timeout + synchronous の組合せはまず試す価値が高く、MMAPやチェックポイント調整でさらに伸びる。日本の開発現場でも、小〜中規模アプリの迅速な開発・簡易運用という観点から即効性のある選択肢になる。
