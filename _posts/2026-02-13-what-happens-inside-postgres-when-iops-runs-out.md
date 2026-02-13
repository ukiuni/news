---
layout: post
title: "What happens inside Postgres when IOPS runs out - IOPSが枯渇したときPostgresの内部で何が起きるか"
date: 2026-02-13T16:54:58.822Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://frn.sh/bio/"
source_title: "What happens inside Postgres when IOPS runs out"
source_id: 442599818
excerpt: "IOPS枯渇でPostgresが連鎖的に停止する原因と即効対策を解説"
---

# What happens inside Postgres when IOPS runs out - IOPSが枯渇したときPostgresの内部で何が起きるか
Postgresが「IOPS天井」にぶつかるときに起きる自己増殖的パニックの正体

## 要約
悪いインデックスや大規模スキャンでディスク要求が一気に増えると、カーネルのブロック層でI/Oリクエストがキュー化され遅延が急増。遅い読み込み→ロック長期化→コネクション増加、というループでI/O飽和が自己持続してしまうのが主因です。

## この記事を読むべき理由
多くのクラウド環境（プロビジョンドIOPSや共有ディスク）や日本企業のリアルタイムサービスで同様の現象が起きやすく、原因把握と対策を知らないと運用障害が長時間化してコストと可用性に直結します。

## 詳細解説
- レイヤ構造：Postgresはまずshared_buffers→OSページキャッシュ→ブロック層→デバイスという複数キャッシュ/キューを経てページを読む。read(2)は直接ディスクには行かず、blk-mq（ソフトウェア／ハードウェアキュー）で管理されます。  
- キュー溢れ：デバイスがプロビジョンドIOPS（例：3000 IOPS）に達すると、ハードウェアディスパッチが受け付けられないリクエストをdispatchリストに積む。キューが深くなるほど各readは待ち時間が増える（1ms→10ms→50ms）。  
- Postgres側の振る舞い：遅延したreadでバックエンドが長時間スリープすると、各種ロック（バッファマッピングや行ロック等）を保持したまま待機するため、別プロセスがロック待ちになり、pg_stat_activityではLock waitに見えるが実態はI/O待ちの派生現象。  
- コネクションプールとの相互作用：アプリのコネクションプールは応答が戻らないと新しい接続を開く→Postgresがさらにバックエンドをフォーク→さらにI/O要求が増える、という負の連鎖で飽和が自己持続。  
- Autovacuumの落とし穴：vacuumは多数のインデックスページを読み、ページ数ベースでスリープするがキュー深度や実際のI/O待ちを参照しないため、既存負荷と合わさると一気に天井を越えることがある。  
- 典型的なトリガー：索引が不足していて「account_idで索引走査→ヒープを大量フェッチ→JSONBや列フィルタでほぼ廃棄」というパターンは、1クエリだけで数千IOPSを消費し得る。  
- ロードアベレージの誤解：多くのバックエンドがI/O待ち（S/D状態）に入り、CPU使用率は低くてもload averageが高く見えるためボトルネック判定を誤るケースがある。

## 実践ポイント
- まず緊急対応：問題時は不要な接続を切る（pg_terminate_backend）か負荷源のスケジュールを止める。これはキューの到着率を下げる唯一確実な即時策。  
- インデックス改善：フィルタ条件（特にJSONB／式条件）に合ったインデックスやパーティショニングで「ヒープを大量に辿る」パターンを潰す。部分インデックスや式インデックスを検討。  
- Autovacuum運用：vacuum_cost_limit / autovacuum_vacuum_cost_delay を見直すだけでなく、vacuumのスケジューリングを低負荷時間帯に移す／テーブルごとの閾値を調整。  
- コネクション制御：アプリ側プールの最大接続数を厳格に制限し、DB側のmax_connectionsと整合させる。負荷制御（レート制限）を導入。  
- 監視と診断：iostat/blktrace、/sys/block/<dev>/queue/scheduler、pg_stat_activityのwait_event、pg_buffercacheやpg_stat_io的な指標でI/Oキュー深度・待ち時間・バックエンド状態を継続監視。  
- インフラ対策：ディスクのIOPSを増やす／より大きなインスタンス（RAM増でキャッシュヒット向上）／リードレプリカに重いスキャンを分散。  
- 検証運用：負荷テストで典型クエリを再現し、IOPS限界に近い状況での挙動と回復手順を確認しておく。

以上の点を押さえれば、単発の「遅いクエリ」から運用全体を巻き込むIOPS飽和事故を未然に防げます。
