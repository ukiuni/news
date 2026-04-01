---
layout: post
title: "SQLite DB: simple, in-process, reliable, fast - SQLite DB：シンプル、プロセス内、信頼できて高速"
date: 2026-04-01T16:07:47.220Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://binaryigor.com/sqlite-db-simple-in-process-reliable-fast.html"
source_title: "SQLite DB: simple, in-process, reliable, fast"
source_id: 1518952565
excerpt: "単一ファイルで数千RPSを実現、運用コストを劇的に下げるSQLite再評価ガイド"
image: "https://binaryigor.com/assets/og-image.png"
---

# SQLite DB: simple, in-process, reliable, fast - SQLite DB：シンプル、プロセス内、信頼できて高速
小さな単一ファイルDBで運用コストを下げ、読み性能を劇的に稼ぐ――SQLite再評価ガイド

## 要約
SQLiteはアプリ内で動作する単一ファイルの埋め込み型RDBで、ネットワークや外部DBサーバを排しつつ高い読み性能と十分な書き性能を低運用で実現する。設定次第で数千RPSのAPIを単一VMで捌けるケースが現実的。

## この記事を読むべき理由
日本のスタートアップ／SaaS開発、社内ツール、エッジ/組み込み開発で「運用コストを下げつつ性能を確保したい」場面が増えている。SQLiteは初期導入／運用負荷を劇的に下げる現実的な選択肢になるから知っておくべき。

## 詳細解説
- 基本特性  
  SQLiteはライブラリとしてプロセス内で動作し、ほぼ単一ファイルへ読み書きする。ネットワークを介さないためレイテンシと障害面で有利。ただし「単一ライター」制約があり、同一DBへの同時書き込みは直列化される。

- 性能実測（抜粋）  
  - 単体クエリベンチ：読みでは数万QPS（例: ~49,547 qps）、書きで数百〜千qps（例: ~808 qps）。  
  - REST API実運用系（PRAGMA調整、WAL有効、1.25M行テーブル、読み90%/書10%）では：  
    - 2CPU/2GB環境で約2000 RPS、4CPUで約3000 RPSを継続処理。  
  これらはローカルI/Oとインデックスを効かせた条件下の数値で、多くのWeb/内部サービスの要件を満たす。

- チューニングポイント（元記事の推奨設定）  
  ```sql
  PRAGMA cache_size=100000;
  PRAGMA journal_mode=WAL;
  PRAGMA busy_timeout=5000;
  ```
  - WALモードで読みと書きの並行性が改善（ライターは1つでも、読者は妨げられにくい）。  
  - cache_sizeでページキャッシュを増やしIOを削減。busy_timeoutでロック待ちを許容。

- スケーリング戦略  
  - モジュール毎やシャーディング（ユーザID・アカウント・国別）で複数DBに分散すれば単一マシン内で数倍〜10倍程度のスループット拡張が可能。制約はOS/ディスクI/Oがボトルネックになる点。

- 可用性設計  
  クラウドVPSは多くで99.9%〜99.99%のSLAを提供し、短時間の停止はクライアント側リトライで吸収可能。長時間障害対策としては次が有効：  
  1) ブロックストレージを用いてボリュームを別VMへアタッチして復旧（プライマリ/セカンダリ構成でスイッチ）  
  2) リアルタイムなレプリケーション／バックアップツール利用（SQLite Backup API, sqlite3_rsync, Litestreamなど）で差分を送って複製を保持しフェイルオーバーする。  
  可用性計算例：$$\text{1日あたりのダウンタイム} = 86400 \times (1 - \text{可用性率})$$
  例：99.9% → $86400\times0.001=86.4\ \mathrm{秒/日}$。

## 実践ポイント
- まず負荷特性を把握：読み/書き比率とピーク負荷をベンチマークする。  
- 小〜中規模のサービスや社内ツールはSQLiteを第一候補に：運用負荷とコストが劇的に下がる。  
- 本番設定は必ずWALを有効にし、cache_sizeとbusy_timeoutを調整する。  
- 書き頻度が高い場合はシャーディング（DBを分割）か、別DBを検討。  
- 災害対策はLitestreamやsqlite3_rsyncで増分ストリーミングを用意し、ボリューム切替や二重構成でフェイルオーバー計画を準備する。  
- 最終判断は実環境での負荷試験と運用コストの比較で行うこと。

以上。SQLiteは「シンプルさ」を活かして多くのケースで有効な選択肢になり得る。
