---
layout: post
title: "You can just port things to Cloudflare Workers - Cloudflare Workersへそのまま移植できるって話"
date: 2026-01-26T07:52:18.420Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sigh.dev/posts/you-can-just-port-things-to-cloudflare-workers/"
source_title: "You can just port things to Cloudflare Workers • sigh.dev - Scott Cooper&#39;s dev blog"
source_id: 46761239
excerpt: "Codexで自動生成しTypeScript化、DatasetteやRailsをCloudflare Workersへ低コスト移植する実例"
---

# You can just port things to Cloudflare Workers - Cloudflare Workersへそのまま移植できるって話
無料枠で動く本格的サービスを、AIで“さくっと移植”する現場レポート

## 要約
作者はGPTベースのCodexを活用して、Datasette相当とRails製のメール管理ツールをTypeScriptでCloudflare Workersへ移植し、実用レベルで動かせることを示した。Worker固有の制約（Pythonサポートの欠如やルーティングの注意点）を踏まえつつ、Hono／Drizzle／D1／Alchemyなどで解決している。

## この記事を読むべき理由
Cloudflare Workersは低コストでグローバル配信できるため、日本のスタートアップや副業開発者に魅力的。AIでのコード生成が現実的な移植ワークフローになりつつある点は、即戦力の知見になる。

## 詳細解説
- なぜ移植が必要か：Workersは安価だがPythonエコシステムが弱く、既存のPython/ Rubyプロジェクトはそのまま動かせない。そこでTypeScriptでの再実装が現実解になる。  
- 使った主要技術：
  - Hono：軽量なCloudflare向けフレームワーク。JSXでサーバー側テンプレート風レンダリングも可能で、SPAにせずに済ませられる。
  - Drizzle：TypeScript向けORMでD1（CloudflareのSQLite互換）と相性が良い。
  - Alchemy：Cloudflareへのデプロイ補助ツール。
  - D1：軽量なデータベースとしてWorkers上で利用。
  - Codex (GPT-5.2 Codex)：リポジトリ解析とタスク分割、コード生成の主要ドライバー（ただし人手による修正必須）。  
- 事例：
  - datasette-ts：DatasetteをTypeScriptで再実装、HonoのJSXでサーバー側レンダリング。デモとソースあり（scttcper/datasette-ts）。
  - sesnoop：RailsのSessyをCloudflare Workerへ移植し、SES/SNSの受信→D1保存を実装。フロントは別途React SPAを提供（scttcper/sesnoop）。  
- ハマりどころ：
  - AIが余計なフロント実装を生成しがちで、デザイン/コンポーネント差し替えが必要。
  - Cloudflareのバインディング（例：Workerが/apiにバインドされている場合、/webhookが静的アセット扱いされうる）などルーティング設計ミス。
  - テスト環境構築・CIでのエミュレーションに手間がかかる。

## 実践ポイント
- 小さく始める：機能を絞ってまずTypeScriptで動く最小実装を作る。  
- 推奨スタック：Hono + Drizzle + D1、デプロイにAlchemy。  
- AI活用の心得：Codexでボイラープレートを生成→必ず手でレビューして美化・安全対策を施す。  
- Cloudflare特有の注意：
  - Workerのバインドされたパスと静的アセットのルールを確認する（/api など）。  
  - 実行時間・メモリ制限を意識した設計にする。  
- すぐ試すコマンド例：
```bash
npx datasette-ts@latest serve ./legislators.db
```
- 参考リポジトリ：scttcper/datasette-ts、scttcper/sesnoop（実際の実装を参照して学ぶと早い）。

以上。
