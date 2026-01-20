---
layout: post
title: "The challenges of soft delete - ソフトデリートの課題"
date: 2026-01-20T22:39:26.922Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atlas9.dev/blog/soft-delete.html"
source_title: "The challenges of soft delete | atlas9"
source_id: 46698061
excerpt: "ソフトデリートが長期運用で招く落とし穴とPostgreSQLでの現実的代替案を実例付きで解説"
---

# The challenges of soft delete - ソフトデリートの課題
なぜ「消さない」設計が後でシステムを壊すのか？実運用で困るソフトデリートの落とし穴と現実的な代替案

## 要約
ソフトデリート（deletedフラグやarchived_at）には「復元できる」という利点がある一方で、クエリ複雑化・デッドデータ肥大・マイグレーションやオペレーションの難化といった長期的コストがある。PostgreSQLではトリガ／WALベースCDC／アプリ層イベントなど、アーカイブを本体データと分離する手法が有効なことが多い。

## この記事を読むべき理由
日本のプロダクトでも「誤削除対応」「監査保持」「サポート負荷軽減」は頻出要件。初期は簡単に見える設計が数年で運用負担を招くケースを避け、現場で使える代替設計と実践チェックリストを知る価値がある。

## 詳細解説
- なぜarchived_atは危険か  
  - ライブテーブルに「死んだ」行が残り続け、インデックスやクエリ効率が落ちる。Terraform等で再作成されるたびにゴミ行が増える運用例もある。多くのプロジェクトは保持期間（retention）や定期クリーンを設定せず、バックアップや復元時に大規模なリストアコストが発生する。

- マイグレーションと復元の複雑さ  
  - 古い行に対するバックフィルやデフォルト修正が困難。復元処理がCreate APIのロジックを再実装するような形になるとバグだらけになりやすい。復元は可能なら既存の作成APIを通す方が安全。

- 代替案（PostgreSQL中心）
  1. アプリケーション層イベント  
     - 削除時にイベントを投げ、別サービスがS3等にシリアライズして保管。利点はDBがシンプルで、外部リソースのクリーンアップを非同期化できること。欠点はインフラ複雑化と、アーカイブ探索が難しい点。
  2. トリガでアーカイブテーブルへコピー（推奨スタート地点）  
     - 削除前に行をJSONBとして別テーブルへ保存。ライブテーブルは常にクリーンに保てる。例：
```sql
-- sql
CREATE TABLE archive (
  id UUID PRIMARY KEY,
  table_name TEXT NOT NULL,
  record_id TEXT NOT NULL,
  data JSONB NOT NULL,
  archived_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  caused_by_table TEXT,
  caused_by_id TEXT
);
```
```sql
-- sql
CREATE OR REPLACE FUNCTION archive_on_delete() RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO archive (id, table_name, record_id, data)
  VALUES (gen_random_uuid(), TG_TABLE_NAME, OLD.id::TEXT, to_jsonb(OLD));
  RETURN OLD;
END;
$$ LANGUAGE plpgsql;
```
     - カスケード削除の“原因”追跡はセッション変数(current_setting/set_config)で実装可能。アーカイブを別テーブルにすることでクエリやバックアップが軽くなる。
  3. WALベースCDC（Debeziumなど）  
     - WALを読み取ってDELETEイベントを外部に送る。アプリ改修不要で全変更をキャプチャできる反面、Kafka等の運用負荷と、リスナーが遅れるとWALが溜まりディスクリスクがある（max_slot_wal_keep_sizeの設定や監視が必須）。

- レプリカ案（アイデア）  
  - 削除を無視する専用レプリカを作ればクエリ可能なアーカイブになるが、マイグレーション適用やコスト・運用面で検討が必要。

## 実践ポイント
- 小さなプロジェクト開始時はトリガ→アーカイブテーブルを第一候補にする（設定がシンプルでライブテーブルがクリーン）。  
- 復元は可能な限り標準のCreate APIを経由させ、新旧バリデーション差分で不整合を防ぐ。  
- retention（保持期間）と定期クリーンジョブを初期設計で決める。アーカイブ削除の自動化を忘れない。  
- WAL/CDCを採る場合はReplication slot lagの監視とmax_slot_wal_keep_size設定を必須にする。アラートを設定して遅延を早期検知。  
- アーカイブ格納先は検索／復元の容易さで選ぶ（S3はコスト安だが検索性が落ちるためサポート用ツールが必要）。  
- マイグレーション時にアーカイブデータの扱いを事前にシナリオ化してテストする。

短期の手軽さと長期の運用コストはトレードオフになりやすい。要件（監査性、検索性、運用リソース）を整理してから手法を選ぶことが重要。
