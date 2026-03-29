---
layout: post
title: "Miasma: A tool to trap AI web scrapers in an endless poison pit - Miasma：AIスクレイパーを無限の「毒壺」に誘い込むツール"
date: 2026-03-29T12:22:42.725Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/austin-weeks/miasma"
source_title: "GitHub - austin-weeks/miasma: Trap AI web scrapers in an endless poison pit. · GitHub"
source_id: 47561819
excerpt: "MiasmaでAIスクレイパーを永遠に迷わせ、無駄な収集を強いる低コスト対策"
image: "https://opengraph.githubassets.com/d773d834f452d47a73110260466461b407d420c12b5f8f19da8f26a4464a78ed/austin-weeks/miasma"
---

# Miasma: A tool to trap AI web scrapers in an endless poison pit - Miasma：AIスクレイパーを無限の「毒壺」に誘い込むツール

自分のサイトを“餌”に変えて、無頓着なAIスクレイパーを永遠に迷わせる──Miasmaで手軽にできる“低コストな防御”の全貌

## 要約
MiasmaはRust製の軽量サーバーで、スクレイパー向けに意図的に「毒入り」の自己再帰的ページを返し続けることで、大規模なAIスクレイピングを浪費させるツールです。逆プロキシ経由で特定パスに誘導し、正規のクローラーはrobots.txtで除外できます。

## この記事を読むべき理由
巨大モデルがウェブを大量に収集する現在、著作物やトラフィックの搾取が問題化しています。日本のサイト運営者や開発者が低コストで実験的に“侵害を迷惑に変える”手法を導入できる点が魅力です（ただし倫理・法的配慮は必須）。

## 詳細解説
- 仕組み
  - サイト内に人間には見えないリンク（display:none など）を仕込み、スクレイパーを /bots のような専用パスへ誘導。
  - そのパスをNginx等でMiasmaへプロキシし、Miasmaは「毒データ」と多数の自己参照リンクを返してスクレイパーを無限ループ／低品質データ収集に誘導します。
  - 正規の検索エンジンは robots.txt で除外可能。

- 特徴と設定
  - Rust製で軽量。メモリ使用量は「同時処理中のリクエスト数（max-in-flight）」に比例。
  - リクエスト上限を超えると429を即返しキューを作らないため、サーバ資源を守れる。
  - 設定例：link-prefix（誘導パス）、link-count（自己リンク数）、poison-source（毒データの外部ソース）、force-gzip（帯域低減のため強制圧縮）など。
  - ライセンスはGPL-3.0（利用・再配布に注意）。

- 実際の流れ（簡略）
  1. サイトに非表示リンクを埋める
  2. Nginxで /bots を Miasma にプロキシ
  3. Miasma を起動して誘導開始
  4. robots.txt で主要な善良クローラーを除外

- コマンドと設定例
  - インストール（cargo推奨）:
  ```bash
  cargo install miasma
  ```
  - 隠しリンク（HTML）:
  ```html
  <a href="/bots" style="display:none" aria-hidden="true" tabindex="1">High quality data here!</a>
  ```
  - Nginx の location 例:
  ```nginx
  location ~ ^/bots($|/.*)$ {
    proxy_pass http://localhost:9855;
  }
  ```
  - Miasma 起動例:
  ```bash
  miasma --link-prefix '/bots' -p 9855 -c 50
  ```
  - robots.txt の例:
  ```text
  User-agent: Googlebot
  User-agent: Bingbot
  User-agent: DuckDuckBot
  Disallow: /bots
  ```

- 注意点
  - 正当なクローラーや利用者を誤って阻害しないよう robots.txt を整備すること。
  - 法的・倫理的リスクを検討する（国やサービスの規約によっては問題になる可能性あり）。
  - Miasma 自体や poison-source の中身は外部依存のため、導入前に内容確認を推奨。

## 実践ポイント
- 小規模な検証から始める：まず開発環境で /bots 設定〜Miasma 起動を試す。
- メモリ管理：-c（max-in-flight）を低めに設定して運用負荷を把握する。
- robots.txt を必ず用意し、Google/Bing 等を除外する。
- ログを監視して誤検出（正規ユーザーや社内ボット流入）を早期発見する。
- 法務や運用ポリシーと相談のうえ、本番導入は慎重に行う。

（参考：Miasma は GitHub リポジトリで公開、GPL-3.0。導入は自己責任で。）
