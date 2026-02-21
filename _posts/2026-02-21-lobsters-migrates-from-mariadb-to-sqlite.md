---
layout: post
title: "lobste.rs migrates from MariaDB to SQLite - lobste.rs が MariaDB から SQLite へ移行"
date: 2026-02-21T22:38:44.635Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/oz7ebk"
source_title: "lobste.rs migrates from MariaDB to SQLite | Lobsters"
source_id: 1002723262
excerpt: "lobste.rsがMariaDBからSQLiteへ移行、遅延で即ロールバックされた真相"
image: "https://lobste.rs/story_image/oz7ebk.png"
---

# lobste.rs migrates from MariaDB to SQLite - lobste.rs が MariaDB から SQLite へ移行
人気ニュースサイトのDBが「サーバレス化」へ――移行で露呈した性能と運用の現実

## 要約
コミュニティニュースサイト lobste.rs が一時的に読み取り専用にして MariaDB から SQLite へ移行を試みたが、移行直後に「極端な遅さ」が発生してロールバックされた。移行候補には PostgreSQL も挙がっており、最終的な選定と運用改善を詰め直す段階にある。

## この記事を読むべき理由
データベース選定は運用コストと性能に直結する日本のスタートアップやOSS運営者にとって重要。小規模・自己ホスト運用で注目される SQLite の利点と落とし穴を、実際の失敗例から学べるため。

## 詳細解説
- 背景：lobste.rs は読み取り専用モードで本番データ移行を実施。GitHub の議論では最初に PostgreSQL の検討があり、その後 SQLite に傾いたことが見える。
- SQLite の長所：サーバ不要・単一ファイルで配布・セットアップが簡単。小さなサービスやローカル開発、Raspberry Pi や軽量セルフホストに適する。
- SQLite の短所と今回の問題点：ファイルベースのロックや書き込み並列性の制約により、高頻度の書き込みや同時接続が多い環境では性能が劣化しやすい。I/O パターンやトランザクションの長さで顕著になり、実運用で「遅すぎる」症状が出たため即時ロールバックとなった可能性が高い。
- 移行で注意する点：スキーマ差分、インデックスの適合、トランザクション設計、接続プーリング（サーバ型DBと挙動が異なる）、バックアップとリカバリ手順の再設計が必要。運用チェックリストやIRCでの問題報告が移行前後に重要な情報源となる。

## 実践ポイント
- 小規模ならまず試す：開発環境やステージングで本番ワークロードを再現してベンチマークすること。
- パラメータ調整：SQLite は journal_mode=WAL、適切な PRAGMA（synchronous, cache_size など）で改善することがある。
- 書き込み負荷に注意：高頻度の書き込みや多数の同時接続があるサービスは PostgreSQL / MariaDB を優先検討。
- 段階的移行：読み取り専用モード→部分切替→監視で問題発生箇所を特定してから本番切替。
- 監視とロールバック計画：性能劣化時の即時ロールバック手順と切り分けログを用意する。

短い実例として、lobste.rs のケースは「手軽さに惹かれた選択が運用負荷で跳ね返ってきた」典型。実運用では必ず実トラフィックでの検証と段階的な導入を。
