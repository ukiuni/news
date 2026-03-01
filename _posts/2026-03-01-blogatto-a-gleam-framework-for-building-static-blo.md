---
layout: post
title: "Blogatto - A Gleam framework for building static blogs - Blogatto：Gleamで作る静的ブログフレームワーク"
date: 2026-03-01T12:16:57.060Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blogat.to"
source_title: "Blogatto | A Gleam framework for building static blogs with Lustre and Markdown"
source_id: 1050105883
excerpt: "GleamでMarkdownから高速・安全な静的ブログを一括生成する軽量フレームワーク"
image: "https://blogat.to/og_preview.jpeg"
---

# Blogatto - A Gleam framework for building static blogs - Blogatto：Gleamで作る静的ブログフレームワーク
魅力的タイトル: Gleamで超軽量ブログを自作する——BlogattoでMarkdown＋Lustreの静的サイトを一気通貫生成

## 要約
BlogattoはGleam上で動く静的ブログ生成フレームワークで、Markdown（YAML frontmatter）とLustreビュー、Maudコンポーネントを組み合わせてサイト、RSS、サイトマップ、robots.txtを一括生成します。設定は単一のConfigで行い、ビルドパイプラインで完全な静的出力を作ります。

## この記事を読むべき理由
日本でも個人ブログ、技術ドキュメント、プロダクトのドキュメントサイトを低コスト・高速に運用したい開発者が増えています。Blogattoはランタイム不要の静的出力を標準で作れるため、国内の静的ホスティング（GitHub Pages、Netlify、国内クラウドの静的配信など）へ簡単デプロイでき、セキュリティや運用負荷が小さい点が魅力です。

## 詳細解説
- 基盤技術
  - Gleam：Erlang/BEAMエコシステム上の型付き関数型言語で、堅牢性や並行処理を重視するプロジェクトに向きます。
  - Lustre：Blogattoで静的ページの「ビュー」を定義するために使う軽量なテンプレーティング/ルーティングレイヤ。
  - Maud：HTMLを生成するコンポーネントシステム。Markdownの出力やポストラップ（テンプレート）をMaudでカスタマイズ可能。
- 入出力の流れ（ビルドパイプライン）
  1. 出力ディレクトリをクリーン再作成
  2. 静的アセット（CSS/画像等）をコピー
  3. robots.txt を生成
  4. Markdownファイルを解析し、frontmatterを抽出 → HTMLレンダリング → ポスト資産をコピー
  5. Lustreのビュー関数から静的ページをレンダリング（ビューは投稿リストを受け取れる）
  6. RSSフィード生成（フィルタやカスタムシリアライザ対応）
  7. sitemap.xml を生成
- 主要機能
  - Markdown投稿（YAML frontmatter）から自動生成
  - 多言語対応：index.mdの隣に index-ja.md / index-en.md を置く運用が可能
  - 静的ページとブログ投稿を同一設定で管理
  - RSS / sitemap / robots.txt の自動生成
  - Markdown要素ごとのカスタムレンダリング（Maudを用いてHTML出力をオーバーライド）
  - 静的アセットのコピー
  - 開発サーバー：ファイル監視・自動ビルド・ライブリロード（開発効率向上）
  - エラーハンドリングとAPIドキュメントはHexDocsで提供
- 設定方法（概念）
  - builderパターンでConfigを定義し、blogatto.build(config) を呼び出すだけでパイプラインが走る。
  - ルートはLustreのビュー関数にマップし、ビュー内で投稿一覧などを受け取ってレンダリングする。

## 実践ポイント
- はじめに：Gleamプロジェクトを作成し、Blogattoを依存に追加してConfigを用意する。最初は公式のExample blogを参考にすると早い。
- 投稿はMarkdown＋YAML frontmatterで作成。多言語化はファイル名で管理（index-ja.mdなど）。
- ページレイアウトやMarkdownレンダリングを細かく変えたい場合はMaudコンポーネントを実装して差し替える。
- 開発はローカルのdevサーバーでファイル監視→ビルド→ライブリロードを活用し、問題なければ静的ホスティングへデプロイ（CIで自動化すると運用が楽）。
- ドキュメント確認：APIや設定の詳細はHexDocsと公式Exampleリポジトリを参照して、まずは小さなサイトで試すこと。

参考：公式サイト（https://blogat.to）とGitHub/Codebergのリポジトリ、HexDocsのAPIを確認してから導入を進めると安心です。
