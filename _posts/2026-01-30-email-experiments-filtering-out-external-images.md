---
layout: post
title: "Email experiments: filtering out external images - 外部画像をフィルタするメール実験"
date: 2026-01-30T12:48:40.577Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.terracrypt.net/posts/email-experiments-image-filtering.html"
source_title: "Email experiments: filtering out external images — Terracrypt"
source_id: 1654707076
excerpt: "外部画像で自動配信メールを自動振り分けし重要メールを見逃さない簡単Sieve手法"
---

# Email experiments: filtering out external images - 外部画像をフィルタするメール実験
魅力的な受信箱を取り戻す：外部画像で自動通知メールだけを自動振り分けする小さな工夫

## 要約
外部ホストから読み込む画像（トラッキング画像）を検出し、手作業で送られたメールとシステム／ニュースレター等の自動送信メールを簡易に分離する手法を紹介します。

## この記事を読むべき理由
多くのニュースレターや自動メールは外部画像を使って配信状況を把握します。日本でも業務通知やマーケティングメールが増える中、重要な手作業メールを見逃さないための簡単で効果的なフィルタ手法はすぐ役立ちます。

## 詳細解説
- 背景: HTMLメールは画像を外部参照することが多く、利便性（画像を添付しない）とトラッキング（画像読み込みで開封を記録）という両面があります。多くのメールクライアントは既定で外部画像をブロックする理由はここにあります。
- アイデア: 「外部画像を含むメール＝自動生成メール」の近似を使う。著者は手動で送るメールは画像を添付する傾向があり、外部参照画像は自動配信で多いと観察しました。
- 実装: サーバ側のSieveフィルタ等で本文中に外部画像のURL（https）を含むか正規表現でチェックし、自動フォルダに振り分けます。HTML解析を正規表現で行うのは厳密には脆弱ですが、単純なマッチなら実用的です。
- 注意点: 正規表現でHTMLを解析するのは万能ではない／誤振り分けが起きる可能性／自分の連絡先や重要な送信元は除外するべき。

## 実践ポイント
- 基本のSieveルール例（Sieve対応サーバ向け）:
```sieve
if body :regex "<img[^>]*src=\"https" {
  fileinto "Inbox.Automated";
}
```
- 連絡先を除外する例（送信元アドレスは適宜置換）:
```sieve
if allof (body :regex "<img[^>]*src=\"https",
          not address :all :is ["From"] ["alice@example.com", "bob@example.jp"]) {
  fileinto "Inbox.Automated";
}
```
- 実運用のヒント:
  - まずは「自動振り分けフォルダ」を積極的にチェックする運用を習慣化する。
  - 誤振り分けがあれば正規表現を緩める／ブラックリスト・ホワイトリストで調整する。
  - Sieve非対応ならメールゲートウェイ（Mailgun、Postfixフィルタ等）やクライアント側フィルタで同様の条件を設定する。
  - プライバシー向上と受信箱のノイズ削減が狙い。日本の企業メールや購読サービスでも効果が期待できます。
