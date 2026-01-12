---
layout: post
title: "we rolled our own documentation site - 独自のドキュメントサイトを構築した"
date: 2026-01-12T15:12:09.956Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.tangled.org/docs"
source_title: "we rolled our own documentation site"
source_id: 1203946421
excerpt: "PandocでJS不要の軽量ドキュメントを作り、Nixで簡単に配備する手法"
image: "https://blog.tangled.org<no value>"
---

# we rolled our own documentation site - 独自のドキュメントサイトを構築した
なぜ「Pandoc + No‑JS」でドキュメントを自作するのが小規模プロジェクトに最適なのか

## 要約
Tangled は Mintlify や Docusaurus を使わず、Pandoc の chunkedhtml 出力で軽量かつスタイラブルなドキュメントサイトを自作した。結果として「JS不要」「検索はブラウザの Ctrl+F」「Nix／colmena で簡単にビルド・デプロイ」が実現できた。

## この記事を読むべき理由
日本の企業やスタートアップでは、ドキュメントの軽さ・保守性・セキュリティ（JS最小化）が重要です。社内向けや小規模 OSS のドキュメント運用で、外部サービスに頼らず安価に始められる具体手法が学べます。

## 詳細解説
- なぜ自作したか  
  要件はシンプル：モノレポ内に収まり、JS を不要にし、検索はブラウザで事足りる、ビルド／デプロイの複雑さを避ける。既存ツール（Mintlify/Docusaurus/MkDocs/MdBook）はそれぞれ利点はあるが、Tangled の要件には過剰・あるいは手間が残った。

- Pandoc の利点  
  Pandoc は汎用のマークダウン変換器で、chunkedhtml 出力を使うとドキュメント内の各セクションを個別ページに分割しつつ自動TOCが作れる。テンプレートをカスタムすればサイドバーや Tailwind の prose クラスを適用して本体サイトと統一した見た目にできる。

- 実装の要点  
  1. 個別 markdown を一つに結合（DOCS.md）。  
  2. template.html を編集して各ページにサイドバー（TOC）を表示。  
  3. Tailwind の prose クラスを挿入してスタイル統一。  
  4. Pandoc コマンドで出力。

  代表的なコマンド（chunkedhtml）:
  ```bash
  pandoc docs/DOCS.md \
    -o out/ \
    -t chunkedhtml \
    --variable toc \
    --toc-depth=2 \
    --css=docs/stylesheet.css \
    --chunk-template="%i.html" \
    --highlight-style=docs/highlight.theme \
    --template=docs/template.html
  ```

  単一ページ版（ブラウザの検索をサイト全体で使いたい場合）:
  ```bash
  pandoc docs/DOCS.md \
    -o out/index.html \
    -t html \
    --variable toc \
    --toc-depth=2 \
    --css=docs/stylesheet.css \
    --highlight-style=docs/highlight.theme \
    --template=docs/template.html
  ```

- モバイルでのサイドバー折畳み  
  JS を避けるために選んだ手法は複数：`<details>`/`<summary>`、新しい Popover API、あるいは CSS の :checked トリック（MkDocs が採用）。Popovers はクリック外で閉じられる利点があるが、ブラウザの「ページ内検索」がポップオーバー内を検索しない点に注意。

- 検索戦略  
  組み込み検索エンジンを入れず、フォームで Google site: 検索にリダイレクトする簡易方式を採用（htmx のやり方を参考）。内部利用ならブラウザの Ctrl+F や単一ページ出力で十分という判断。

- ビルドとデプロイ（Nix / colmena）  
  Tangled は Nix で生成物を作り、Nginx で配信、colmena で適用。更新は flake を更新して colmena を実行するだけ。
  例:
  ```bash
  nix flake update tangled
  nix run nixpkgs#colmena -- apply
  ```

- 注意点  
  Pandoc の Markdown レンダリングは goldmark（Hugo など）の出力と微妙に差が出る場合がある。将来的に機能要件が増えるなら MkDocs/MdBook や専用 SSG を再検討する余地あり。

## 実践ポイント
- 小さく始める：まずは全 Markdown を結合し、Pandoc の chunkedhtml で出力してみる。見た目はテンプレートで調整。  
- 検索は実務でブラウザ検索が効くなら無理に検索エンジンを入れない。大量ページなら単一ページ版か検索プラグインを検討。  
- JS を避けたいなら Popover API や details の活用を検討。UX とブラウザ互換のトレードオフを評価する。  
- CI/CD：Nix を使えるなら derivation を作って colmena 等で配布すると再現性が高い。小規模チームではこのシンプルさが運用コスト低減につながる。  
- 将来の拡張：TOC の自動管理や全文検索を要するなら MkDocs/MdBook、あるいは専用のドキュメントプラットフォーム導入を検討する。

以上を踏まえ、まずは数ページ分で試作してみることを薦めます。Pandoc とテンプレートの組合せは、制約がある環境での「十分に良い」選択肢です。
