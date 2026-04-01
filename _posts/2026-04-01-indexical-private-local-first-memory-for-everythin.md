---
layout: post
title: "Indexical: Private, local-first memory for everything you read on the web - Indexical：ウェブで読んだものをローカルに安全保存する「記憶」ツール"
date: 2026-04-01T20:26:34.434Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/deejayy/indexical"
source_title: "GitHub - deejayy/indexical: Indexical - Private, local-first memory for everything you read on the web. Browser history is time-based. Bookmarks require effort. Notes require discipline. Indexical aligns with how people actually remember: vaguely, semantically, and after the fact. · GitHub"
source_id: 764743408
excerpt: "ブラウザで読んだ全ページをローカルでMarkdown保存し高速検索する自分専用のプライベート記憶ツール"
image: "https://opengraph.githubassets.com/3c3cc357227c74f43802dd567dab7c6b37950f7b77e8ce2bb9a03b6e1a164890/deejayy/indexical"
---

# Indexical: Private, local-first memory for everything you read on the web - Indexical：ウェブで読んだものをローカルに安全保存する「記憶」ツール
魅力的なタイトル: ブラウザ履歴を超える「自分専用の検索エンジン」——読んだページを全部ローカル保存してすぐ検索できるIndexical

## 要約
Indexicalはブラウザ拡張＋ローカルサーバーで、訪問したウェブページの本文を自動で抽出・Markdown化してSQLiteに保存し、ローカルだけで全文検索（BM25、スペル補正、フィルタ等）できるツール。データはマシン外に出ない「local-first」設計でプライバシーを守る。

## この記事を読むべき理由
ブラウジング履歴やブックマークは「後で探す」には弱く、日本のエンジニア／リサーチャー／情報消費者にとって、読んだ情報を確実に再利用できる仕組みは生産性向上とコンプライアンス（企業内秘匿情報の扱い）に直結するため。

## 詳細解説
- 全体構成：ブラウザ拡張（Manifest V3、Plain JS）＋ローカルDaemon（Node.js/TypeScript、SQLite）で構成。拡張がReadabilityで本文抽出→TurndownでMarkdown化→ローカルサーバへPOST。
- 検索機能：BM25に基づくランキング、スニペット強調、SQLiteのspellfix1でスペル補正、Google風の検索演算子（"フレーズ"、-除外、site:、intitle:、lang: など）をサポート。
- プライバシー＆安全性：デフォルトで127.0.0.1バインド、ローカルSQLiteに保存、外部通信なし。ドメイン単位のブラックリスト（例：facebook, tiktok, translate.google 等）で自動除外。
- キャプチャ挙動：SPA検知（MutationObserver）でページ遷移を追跡、コンテンツ重複はハッシュで除去、1ページあたり最小250文字要件、レートリミットあり（最大60 ingests/min 等）。
- デプロイ：単一実行ファイル（Windows/macOS/Linux）、Docker compose、ソース（Node.js 22+）。拡張はAMOや配布ZIPから導入可。Windowsサービス化（NSSM推奨）も説明あり。
- 運用面：APIはX-API-Keyでスコープ分離。/ingest, /search, /pages/:id/markdown 等エンドポイント。構造化ログ（pino）、Prometheusメトリクス対応で企業運用もしやすい。

## 実践ポイント
- まずは単一実行ファイルかDockerでサーバーを起動し、拡張をインストールして数ページを閲覧→検索して挙動確認。
- 企業利用ではローカルのみの点を利用して、社内ポリシーに沿った監査ログやブラックリスト設定を整備する（外部送信ゼロが強み）。
- 研究・調査用途なら「Markdownプレビュー＋保存されたスナップショット」で、元ページが消えた後の参照や引用が簡単に。
- カスタム要望（例：別のデータベースや外部連携）を入れるならソースビルドが可能。拡張はビルド不要でローカル開発も容易。

Indexicalは「読んだものを記憶する」新しいアプローチで、個人の知識管理や企業のローカル検索基盤にすぐ活用できるツール。まずはローカルで試し、日常の情報収集ワークフローに組み込むと効果が実感しやすい。
