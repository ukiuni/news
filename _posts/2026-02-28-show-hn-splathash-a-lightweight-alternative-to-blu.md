---
layout: post
title: "Show HN: SplatHash – A lightweight alternative to BlurHash and ThumbHash - Show HN: SplatHash — BlurHash/ThumbHashの軽量代替"
date: 2026-02-28T12:29:41.697Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/junevm/splathash"
source_title: "GitHub - junevm/splathash: compress any image to 16 bytes and reconstruct a blurry preview. Like blurhash and thumbhash, but smaller."
source_id: 47193832
excerpt: "16バイトで32×32の高速ぼかしプレビューを復元、BlurHashより劇的に軽いSplatHash"
image: "https://opengraph.githubassets.com/349766881bdec129d9f1ffb3e70fcbe485f7a669a0a79c2658afb2533e33e895/junevm/splathash"
---

# Show HN: SplatHash – A lightweight alternative to BlurHash and ThumbHash - Show HN: SplatHash — BlurHash/ThumbHashの軽量代替
たった16バイトでサクッと表示。画像プレビューを劇的に軽くする「SplatHash」の正体

## 要約
SplatHashは任意の画像を「16バイト（22文字のbase64url）」に圧縮し、32×32のブラー付きプレビューを超高速で復元する軽量フォーマット。BlurHashやThumbHashより出力が小さく、デコードが非常に速いのが特徴。

## この記事を読むべき理由
モバイルや大量画像を扱う日本のサービス（EC、ニュース、SNS、広告配信など）では、ページロードごとに大量のサムネイルをデコードするため「デコード性能」と「ストレージ効率」が直接UXとコストに効く。本記事はSplatHashがその課題にどう応えるかを端的に示します。

## 詳細解説
- 基本性能
  - 出力サイズ：固定16バイト（128ビット）、base64urlでは22文字
  - 復元サイズ：32×32ピクセルのぼかしプレビュー
  - 実装：Go（リファレンス）、TypeScript、Python。全実装がビット単位で一致。

- ベンチマーク（リポジトリの計測値）
  - デコード時間（Intel Core i5-9300H）：SplatHash 0.067 ms、ThumbHash 0.50 ms、BlurHash 6.55 ms
  - エンコード時間：SplatHash 3.53 ms、ThumbHash 0.86 ms、BlurHash 445 ms
  - メモリ/文字列長：SplatHash は最小（デコードの割当も少ない）

- アルゴリズムの要点（ALGORITHM.md）
  - 表現：背景色 + 6個のガウスブロブ（局所化基底）
  - 選択方法：matching pursuitでブロブ位置を決定
  - 色空間：知覚に基づくOklabで最適化
  - 最終調整：Ridge回帰で重みをグローバル最適化
  - 格納：128ビットにパックして固定長で保存

- 機能比較
  - 固定出力サイズ、128ビット整数として保存可、Oklab対応、ガウス基底、Ridge回帰、アルファ対応、クロス言語でビット一致。
  - 欠点：品質とサイズのトレードオフの細かな調整は不可（可変品質はBlurHashに分がある）。

## 実践ポイント
- 試す（例）
```bash
# Go (参照実装)
go get github.com/junevm/splathash/src/go

# TypeScript
npm install splathash-ts

# Python
pip install splathash-py
```
- 運用方針
  - エンコードはアップロード時にサーバ側で1回実行、デコードはクライアントでページ読み込み時に実行する設計が効果的（デコード最適化が目的）。
  - ストレージ：22文字のbase64url文字列か128ビット整数でDBに格納。固定長なのでインデックスやキャッシュに向く。
  - アルファ対応：透過PNGなどを扱う場合でもサポートがあるため、アイコンや合成プレビューに使える。
  - フォールバック：高画質が必要な場面では元画像または従来のサムネイルを併用。

SplatHashは「小さく・速く・再現性あり」を求める場面で特に魅力的。まずはリポジトリのデモ／実装で簡単な導入検証をしてみてください。
