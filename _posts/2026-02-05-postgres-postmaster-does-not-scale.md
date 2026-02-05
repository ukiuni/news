---
layout: post
title: "Postgres Postmaster does not scale - PostgresのPostmasterはスケールしない"
date: 2026-02-05T05:12:41.958Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.recall.ai/blog/postgres-postmaster-does-not-scale"
source_title: "Postgres Postmaster does not scale"
source_id: 46887893
excerpt: "接続バーストでpostmasterが致命的に飽和しPostgresが数秒停止"
---

# Postgres Postmaster does not scale - PostgresのPostmasterはスケールしない
Postgresの"postmaster"が詰まるとクラスタ全体が10秒止まった話 — 会議録音バーストで露呈した知られざるボトルネック

## 要約
Recall.aiが大量のミーティング録音を同時に開始した際、Postgresの単一スレッドな親プロセス（postmaster）が接続スパイクに追いつけず、接続確立で10〜15秒の遅延が発生した。

## この記事を読むべき理由
日本でもSaaSやメディア処理で「同時接続のバースト」や「バッチ同時開始」は珍しくありません。Postgresは広く使われるため、この現象を理解すると本番での致命的な遅延を未然に防げます。

## 詳細解説
- 問題点の本質  
  Postgresはpostmasterという親プロセスが子プロセス（バックエンド）をforkして接続を処理する設計。postmasterは単一スレッドでイベント（接続受付、子プロセスのreap、並列ワーカー起動など）を順次処理するため、大量の接続/ワーカーの発生（churn）があるとループが枯渇し、接続応答が遅れる。

- 再現と解析  
  Recall.aiは3000台以上のEC2から同時接続を再現し、約1400接続/s付近でpostmasterが飽和。perfプロファイリングで大半の時間がfork/子プロセスの生成・回収に費やされていることを確認した。

- forkコストとHuge pages  
  LinuxのforkはCopy-on-Writeを使うが、ページテーブルエントリ（PTE）のコピーコストが残る。Huge pagesを使うとPTE数が減り、forkのオーバーヘッドが下がる。実運用で huge_pages = on により接続スループットが約20%改善したという観察がある。

- 背景ワーカー（並列クエリ）との相互作用  
  postmasterは並列クエリ用のバックグラウンドワーカー起動も担うため、並列ワーカーが大量だとさらに負荷が増す。記事は並列動作を強制してワーカーを大量発生させるテスト関数を示している（要約）：

```sql
-- sql
CREATE OR REPLACE FUNCTION bg_worker_churn(iterations integer) RETURNS void LANGUAGE plpgsql AS $$
BEGIN
  PERFORM set_config('force_parallel_mode','on', true);
  PERFORM set_config('max_parallel_workers','512', true);
  PERFORM set_config('max_parallel_workers_per_gather','128', true);
  -- 大量の並列ワーカーを生むような処理を繰り返す...
END;
$$;
```

- RDSやマネージド環境の制約  
  RDSでは低レベル設定やメトリクスが制限されるため調査が難しい。Huge pagesやカーネル設定が直接触れない場合は別の対策が必要。

## 実践ポイント
- まず観測：接続スパイク時の接続確立時間（TCPハンドシェイク〜Postgres認証応答）を監視する。  
- 接続プーリング導入：pgbouncer等で接続数を平準化（transactionモード推奨）。  
- Huge pagesを試す：オンにできる環境なら効果あり（※RDSでは不可な場合あり）。  
- 並列ワーカーを制限：max_parallel_workers* 関連パラメータを見直し、短時間で大量ワーカーを起こさない。  
- 起動タイミングを分散：同期的に大量ノードが一斉接続する設計ならジッタを入れて分散。  
- 代替アプローチ：接続前に軽量プロキシ（ローカルpgbouncer）を置く、バックエンドを事前フォークするなどの設計変更を検討。

短くまとめると、Postgres自体は「接続を素早くさばくこと」を前提とした設計ではなく、極端に同期した接続バーストではpostmasterの単一ループがボトルネックになり得る。実運用では接続プーリング＋並列ワーカー制御＋環境依存のカーネル設定で対策を組み合わせるのが現実的。
