---
layout: post
title: "The Recent 0-Days in Node.js and React Were Found by an AI - AIが発見した、Node.jsとReactの最近の0-day脆弱性"
date: 2026-02-03T07:35:49.424Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://winfunc.com/blog/recent-0-days-in-nodejs-and-react-were-found-by-an-ai"
source_title: "The Recent 0-Days in Node.js and React Were Found by an AI | winfunc"
source_id: 410496761
excerpt: "AIが発見したNode.jsのUDS権限突破とRSCの資源枯渇で即時パッチ必須"
image: "https://winfunc.com/blog/recent-0-days-in-nodejs-and-react-were-found-by-an-ai/opengraph-image?d32e9bdd7ccaab4f"
---

# The Recent 0-Days in Node.js and React Were Found by an AI - AIが発見した、Node.jsとReactの最近の0-day脆弱性

AIが突き止めた「サンドボックス突破」と「RSCの暴走」──あなたのサービスにも忍び寄る現実的リスク

## 要約
AIシステムが自律的に発見した2件の0-day（CVE-2026-21636, CVE-2026-23864）は、Node.jsの権限制御の抜け穴とReact Server Components（RSC）のリクエストデコーダの資源枯渇を突くもので、実運用に直接影響する深刻な脆弱性だった。

## この記事を読むべき理由
Node.js/Reactは日本のウェブサービスやスタートアップで広く使われており、今回の発見は「ローカルソケット経由の権限逸脱」や「RSCプロトコルの悪用でサービス死」を招く具体的な攻撃手法を示す。パッチ適用や設計見直しが急務となるため、技術者・運用者は動向と対策を押さえておく必要がある。

## 詳細解説
- CVE-2026-21636（Node.js）
  - 問題点：Node.jsのPermission Modelは --allow-net フラグでTCP/IPのネットワークアクセスを制御するが、Unix Domain Sockets（UDS）への接続を検査しておらず、サンドボックスをすり抜けられた。
  - 影響例：/var/run/docker.sock やデータベースのソケットへ接続されると、コンテナの起動やDBへのアクセス、ローカル権限昇格が可能になる。
  - 改善：UDSパスに対する権限チェックを導入してアクセス制御を強化するパッチが適用された。
  - 再現（概念例）：
  ```javascript
  // javascript
  const net = require('net');
  // 本来ブロックされるはずのローカルソケット接続が許されてしまう
  const sock = net.connect({ path: '/var/run/docker.sock' });
  sock.on('connect', () => { /* Dockerデーモンにアクセス可能 */ });
  ```

- CVE-2026-23864（React Server Components）
  - 問題点：RSCの返信デコーダが特殊な参照トークン（例: $K）を扱う際に、特定の入力で繰り返し展開・参照解決が発生し、CPU高負荷・メモリ急増・プロセスクラッシュを引き起こせる。
  - 影響範囲：Next.js（複数バージョン）やRSC対応するライブラリ群が対象。認証不要でHTTPエンドポイントに悪意あるリクエストを投げるだけで攻撃可能。
  - 対策：パーサの入力検査・サイズ制限、参照解決ループの検出・防止、各RSC実装の修正パッチが必要。

- AIがどう見つけたか
  - 単なるランダム・ファジングではなく、コードベースの「意味的インデックス（呼び出しグラフ、データフロー、制御フロー）」を作り、脅威モデルを自動生成して仮説→攻撃ペイロード生成→検証まで自動で実行。
  - 重要点：論理的な抜け穴（設計差異や仕様未定義箇所）を見つける能力があり、従来のシグネチャ系ツールでは見逃しがちな欠陥を炙り出す。

## 実践ポイント
- 今すぐやること
  - Node.js / React / Next.js 等の公式パッチを確認し、該当バージョンは速やかに更新する。
  - Dockerソケット（/var/run/docker.sock）や他のUDSを不必要に公開しない。コンテナへマウントを避け、UNIXソケットのパーミッションを厳格化する。
  - RSCを使うサーバはリクエストサイズ上限・タイムアウト・メモリ制限を設ける（reverse proxyやWAFでの制限包含）。
- 中長期的対策
  - 依存ライブラリの脆弱性監視（SBOM・自動アップデート）を整備する。
  - 単なる静的検査だけでなく、プロトコル理解を加えたセマンティック解析／脅威モデリングを導入する。
  - AI支援ツールを採用する場合、生成されたPoCや報告は必ず手動で検証し「誤検知（AIスロップ）」への対処ルールを作る。

この記事は、AIが脆弱性発見の流れを「自動化」しうる現実を示すと同時に、運用上の基本（最小権限・入力制御・迅速なパッチ適用）が重要であることを改めて示している。
