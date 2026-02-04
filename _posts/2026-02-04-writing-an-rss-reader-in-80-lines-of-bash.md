---
layout: post
title: "writing an RSS reader in 80 lines of bash - 80行のbashで作るRSSリーダー"
date: 2026-02-04T10:29:00.879Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://yobibyte.github.io/yr.html"
source_title: "writing RSS reader in 80 lines of bash"
source_id: 1052911413
excerpt: "80行のbashで作る、すぐ試せる軽量RSSリーダー（並列取得・重複除去・フィルタ付き）"
---

# writing an RSS reader in 80 lines of bash - 80行のbashで作るRSSリーダー
たった80行で作れる「自分専用」RSSハック — Newsboat に頼らない軽量ワークフロー

## 要約
作者は curl/awk/grep/sed/w3m などUNIXの基本ツールだけで、並列取得・重複除去・フィルタを備えた簡易RSSリーダーを80行ほどのbashスクリプトで実装しています。軽量でハックしやすく、自分用の情報パイプラインを作る例です。

## この記事を読むべき理由
RSSを自分好みに最小限の依存で運用したい日本のエンジニア／テック愛好家にとって、既存ツールに頼らずに動く実用的な「簡易実装」の考え方と実践テクニックが学べます。職場や自宅の小型サーバー、Raspberry Pi上で使える点も魅力です。

## 詳細解説
- 主要アイデア：curlでフィードを取得し、awkで<item>／<entry>ごとに分割。各アイテムの改行を潰して1行化し、grep -oPでタイトル・URL（2種類の書式に対応）を抽出します。  
- 重複防止：link+title のハッシュ（md5sum）を作り、既出リスト(downloaded.txt)にないものだけ処理します。  
- コンテンツ処理：description等は cut で文字数制限してから w3m -dump でテキスト化し、本文にもフィルタを適用できます。  
- フィルタ：filters.txt を CSV（feed,type,regex）で管理。`*` を使すると全フィード対象、正規表現にヒットしたら「除外」する単純な仕組みです。  
- 並列実行と安全性：複数フィードを xargs -P で並列実行し、ファイル追記は flock でロックして競合を防ぎます。  
- 注意点：XMLを正則表現で扱うため壊れるフィードがある、コンテンツが変わると重複検出が漏れるなどの限界あり。堅牢さが必要なら xmlstarlet 等や専用パーサに置き換えるのが良い、という設計トレードオフです。

## 日本市場との関連性
- 日本語フィード（文字コード、エンコーディング）を扱うなら環境変数 LANG を UTF-8 に設定し、ツール群がマルチバイトを正しく扱えることを確認してください。  
- Qiita／Hatena／note／はてブ流入の多い日本向けフィードに対して、ドメイン固有のフィルタを作ると実用性が上がります。  
- 小規模な社内ニュース集約や研究論文（arXiv等）巡回の自動化など、日本のワークフローにも応用しやすい構成です。

## 実践ポイント
- 必要な依存：bash, curl, awk, grep(-P), sed, w3m, md5sum, flock, xargs。まずローカルで動かして動作確認。  
- 設定例：MAX_ITEMS, MAX_CHARS を調整してダウンロード量を制御。filters.txt を作って除外ルールを段階的に追加。  
- 運用案：cron / systemd-timer で定期取得、取得結果を links.md に追記して Newsboat/vim で読む、長文は e-inkへ送るパイプに接続。  
- 改良候補：XMLの正確なパースに xmlstarlet を導入、重複判定に更新検出を加える、フィルタをブラックリスト→ホワイトリストへ変更するなど。

気軽に自分専用のRSSパイプラインを作ってみたいなら、この記事のスクリプトは良い出発点です。
