---
layout: post
title: "Hobby coder accidentally creates vacuum robot army - 趣味プログラマーが掃除ロボ軍団を誤って作ってしまった"
date: 2026-02-17T15:49:02.688Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.malwarebytes.com/blog/news/2026/02/hobby-coder-accidentally-creates-vacuum-robot-army"
source_title: "Hobby coder accidentally creates vacuum robot army | Malwarebytes"
source_id: 440765447
excerpt: "趣味プログラマーがAIで解析し約7000台の掃除ロボの映像・音声を閲覧可能に"
image: "https://www.malwarebytes.com/wp-content/uploads/sites/2/2026/02/robot-vacuum.jpg"
---

# Hobby coder accidentally creates vacuum robot army - 趣味プログラマーが掃除ロボ軍団を誤って作ってしまった
驚愕：AIで解析したら7,000台のロボット掃除機があなたの家を“見ていた”

## 要約
趣味でロボットを操作しようとした開発者が、AI支援でメーカーのプロトコルを解析した結果、約7,000台の掃除ロボットや家庭用バッテリーのライブ映像・音声や家の間取りを閲覧できる状態を発見した。

## この記事を読むべき理由
AIコーディング支援ツールで誰でも高度な解析が可能になり、普段使っているスマート家電の「見えない」リスクが急速に現実化しています。日本でも同様の製品が広く使われているため、消費者・開発者ともに知っておくべき重要な教訓です。

## 詳細解説
- 何が起きたか：開発者はAnthropicのCode系AIを使ってメーカーのモバイルアプリをリバースエンジニアリングし、プロトコルと自分の認証トークンを抽出。カスタムクライアントで接続すると、約24か国にある約7,000台の機器が応答し、カメラ映像・マイク音声・間取り生成が可能になった。  
- 技術的原因：DJIのMQTTブローカーにトピック単位のアクセス制御がなく、1つのデバイストークンで他デバイスのプレーンテキスト通信を参照できた。TLSは使われていたが、通信路の暗号化は接続を守るのみで、トピック権限管理の不備を補わない。  
- 拡大する脅威：AIツールでリバースエンジニアリングのハードルが下がったため、IoTプロトコルの検査・悪用が容易に。過去の類似事例（カメラ遠隔起動やPIN検証の欠如）と合わせ、製品の設計ミスが繰り返されている点が指摘される。  
- 規制動向：EUのCyber Resilience Actや英国のPSTI法などセキュリティ規制が強化されつつあるが、実効性や国際的な執行は課題が残る。

## 実践ポイント
- 購入前：独立したセキュリティテスト結果や評価を確認する（メーカーの説明だけでなく第三者レビュー）。  
- ネットワーク分離：IoTはゲストVLANや別SSIDに置く。管理機器と分離するだけで被害範囲が大幅に減る。  
- ソフト更新：ファームウェアとアプリを常に最新に保つ。自動更新設定を確認。  
- 最小権限：不要なカメラ・マイク機能はオフにする。物理的にレンズを覆うのも有効。  
- 購入判断：カメラ不要ならLiDARのみの機種を検討する（多くの機能は映像なしで十分）。  
- 企業向け：製品設計者はトピック／認可レイヤーのアクセス制御とサーバ側での認証検証を必須にすること。

（参考元：Malwarebytes「Hobby coder accidentally creates vacuum robot army」）
