---
layout: post
title: "Show HN: Double blind entropy using Drand for verifiably fair randomness - Drand を使ったダブルブラインド乱数（検証可能な公平性）"
date: 2026-02-12T02:49:42.956Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blockrand.net/live.html"
source_title: "Roll Verifiably Random Dice with Blockrand Audit"
source_id: 46984083
excerpt: "Drandと事前コミットで第三者検証可能な改ざん不能サイコロ実装法を図解で解説"
---

# Show HN: Double blind entropy using Drand for verifiably fair randomness - Drand を使ったダブルブラインド乱数（検証可能な公平性）

ドランド（Drand）を使って「誰も改ざんできない」検証可能なサイコロ振りをウェブで実現する方法を、図式と手順でわかりやすく紹介します。

## 要約
プレイヤーとサーバーがそれぞれ事前コミット（ハッシュ）し、公開ランダム性（Drand）の署名と合わせて種を公開・結合することで、第三者検証可能な公平な乱数（サイコロ）が得られる仕組みです。

## この記事を読むべき理由
オンラインゲームやギャンブル、ランダム抽選の公正性を証明するニーズは日本でも高まっており、規制対応やユーザー信頼獲得のために即実装可能な手法だからです。

## 詳細解説
仕組みは大きく2段階です。

1. コミット（Future Locked）  
   - プレイヤーとサーバーそれぞれが秘密のシードを用意し、そのハッシュ（Committed Player-Hash / Committed Server-Hash）を事前に公開して「将来の公開内容」をロックします。  
   - ターゲットとなるDrandのラウンド（Target Drand Round）も決めておき、どの公開ビークンを使うかを固定します。  

2. リビール（公開）と検証  
   - 各当事者がシードを公開し、事前に出したハッシュと一致するか検証します。  
   - Drandの公開ビークン（署名付きエントロピー）を取得・検証します（Drandは分散ビコンで署名が付くため改ざん困難）。  
   - 最終乱数はプレイヤーシード・サーバーシード・Drand署名を連結してハッシュ化し、その出力を使います。例（サイコロ）：  
$$
Result = (Hash(player\_seed \mathbin{+} ':' \mathbin{+} server\_seed \mathbin{+} ':' \mathbin{+} drand\_signature) \bmod 6) + 1
$$
   - これにより、どちらか一方だけが不正を働いても結果を支配できず、外部の誰でも再現検証が可能です。

技術的ポイント：安全なハッシュ関数（例：SHA-256）を使う、Drandの署名検証を必ず実行する、ターゲットラウンドを先に固定してタイムラインを守ることが重要です。

## 実践ポイント
- 事前チェックリスト：コミット値のタイムスタンプ保存、Drandラウンドの明示、ハッシュ関数とエンコーディングの明文化。  
- 実装：公開APIでDrandのビークンを取得し、署名検証ライブラリで検証 → シードを結合してSHA-256でハッシュ → 必要な範囲にモジュロ演算。  
- 日本向け提案：ギャンブルや懸賞サービスはログ公開で監査対応、ゲーム運営はユーザー向けに検証ページを用意して信頼性をアピール。  
- 注意点：シードを安全に生成・保存し、リプレイや前方露出を防ぐ運用を組むこと。

元実装・ドキュメントは公開リポジトリ（BlockRand 等）や Drand の公式ドキュメントを参照して再現検証してください。
