---
layout: post
title: "Gwtar: A static efficient single-file HTML format - 静的で効率的な単一ファイルHTMLフォーマット「Gwtar」"
date: 2026-02-15T18:07:26.873Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gwern.net/gwtar"
source_title: "Gwtar: a static efficient single-file HTML format · Gwern.net"
source_id: 47024506
excerpt: "GwtarはHTTP Rangeで巨大資産を遅延読み込みする単一自己完結HTML"
image: "https://gwern.net/doc/cs/algorithm/information/compression/2026-01-23-dbohdan-gpt5imagemini-gwtarlogo-guitar.png"
---

# Gwtar: A static efficient single-file HTML format - 静的で効率的な単一ファイルHTMLフォーマット「Gwtar」

単一の自己完結HTMLファイルで「大容量アセットを遅延読み込み」できる新しいアーカイブ形式。ギガバイト級のページをそのまま配布しつつ、閲覧時には必要な部分だけダウンロードさせる仕組みです。

## 要約
GwtarはHTMLヘッダ＋追記されたtarアーカイブを1ファイルに結合し、ヘッダ内のJavaScriptがHTTP Rangeを使って必要なアセットだけを取り出すことで、静的・単一ファイル・効率（遅延読み込み）の三つを同時に実現します。

## この記事を読むべき理由
- ウェブアーカイブや長期保存で「単一ファイルにまとめたいが巨大化してしまう」問題に直面している人に有効。  
- 日本のミラー運用や研究系サイトで「軽快に公開しつつ完全な自己完結アーカイブを配りたい」場面に直結します。

## 詳細解説
- 背景（HTMLトリレンマ）: 望まれる性質は「静的（自己完結）」「単一ファイル」「効率（必要な部分だけ読み込む）」。従来は2つしか同時に満たせなかった（例: SingleFileは静的＋単一だが効率が低い）。
- Gwtarの設計:
  - 基本は「HTMLヘッダ（HTML+JS+JSONメタ）を先頭に置き、その後ろにtarボールを連結」したファイル（拡張子例: .gwtar.html）。
  - ヘッダのJSはまず表示に必要な元HTMLだけを読み込み、その後の資産要求をインターセプトしてHTTP Rangeリクエストでファイル内の該当バイト範囲を取得する。
  - ダウンロード停止に window.stop() を利用するトリックで、ブラウザがヘッダ以降を先読みしないよう制御している。
  - ヘッダ内には各ファイルのサイズ・Content-Type・SHA-256等のJSONインデックスが入るため、クライアント側で正確に取り出せる。
- 実装／運用面:
  - Gwernは SingleFile で作ったスナップショットを変換するための参照スクリプト（deconstruct_singlefile.php）を提供し、画像再圧縮やPAR2によるFEC（冗長データ）付与も行える。
  - 必須条件: サーバー／CDNがHTTP Rangeリクエストを透過すること。Rangeが無効化される環境（例：一部のCDN設定やプロキシ）は問題を起こす。
- 制限と注意点:
  - Range非対応環境では本来の効率性が失われる（全体をダウンロードすることになる）。
  - 一部のCDNや中継が追記データを扱えない／切る場合がある（実運用で要確認）。
  - バイナリ資産やMIME整合、署名・メタデータの拡張など追加作業は残る。

## 実践ポイント
- SingleFileで保存したHTMLをGwtar化する参考コマンド例：
```bash
php ./static/build/deconstruct_singlefile.php --create-gwtar --add-fec-data 2010-02-brianmoriarty-thesecretofpsalm46.html
```
- 配布前チェック:
  - サーバーが Range をサポートしているかを確認（例: curl -I で Accept-Ranges: bytes を確認）。
  - CDN利用時はRangeパススルーや追記許容の設定を確認する（Cloudflare等で問題報告あり）。
  - ブラウザで実際に遅延読み込みが効くかを検証する（大きなメディアが即ダウンロードされないか等）。
- 運用上のおすすめ:
  - 画像等は再圧縮して容量削減、PAR2で壊れ対策、SHA-256で整合性を確保する。
  - 検索エンジンで普通に公開したいページは .gwtar.html を正しくHTMLとして配信し、メタ情報をヘッダに含める。

Gwtarは「将来の互換性を壊さない」標準的なブラウザ機能だけで三重の要件を満たす実用的な解決策です。大容量や長期アーカイブを扱う日本のサイト運営者や研究者には試す価値が高い手法です。
