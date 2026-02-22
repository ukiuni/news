---
layout: post
title: "A Botnet Accidentally Destroyed I2P - ボットネットが偶然I2Pを破壊した"
date: 2026-02-22T02:52:28.972Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.sambent.com/a-botnet-accidentally-destroyed-i2p-the-full-story/"
source_title: "A Botnet Accidentally Destroyed I2P (The Full Story)"
source_id: 47106985
excerpt: "IoTボットネットの“誤爆”で匿名網I2Pが壊滅、緊急PQ暗号導入の顛末とは"
image: "https://www.sambent.com/content/images/size/w1200/2026/02/A-Botnet-Accidentally-Destroyed-I2P--The-Full-Story-.jpg"
---

# A Botnet Accidentally Destroyed I2P - ボットネットが偶然I2Pを破壊した
ボットネットが“誤って”匿名ネットワークを壊滅させた――その舞台裏と日本への教訓

## 要約
2026年2月3日、I2Pが約70万の敵対ノードにより壊滅的なSybil攻撃を受けた。攻撃元はIoTボットネット「Kimwolf」で、開発側は6日後にポスト量子暗号を既定で有効にしたI2P 2.11.0を緊急リリースした。

## この記事を読むべき理由
匿名通信や分散ネットワーク、そして国内のIoTセキュリティやプライバシーツールの信頼性に直結する事件だから。日本の開発者・運用者・一般ユーザーにとって、被害の原因と対処は他人事ではない。

## 詳細解説
- 何が起きたか：通常1.5万〜2万台で運用されるI2Pに対し、約70万の偽ノードが一斉に参加。実効比は約39対1で、ルーティングやサービス発見が麻痺した（Sybil攻撃）。
- 攻撃者の正体：以前は国家系の妨害と見られていたが、今回の実行者はIoTボットネット「Kimwolf」。2025年末に史上最大級の31.4Tbps DDoSを記録した勢力で、Discord上で「I2PをバックアップC2に使おうとしたら偶発的に壊した」と自白したという報告がある。
- 背後の技術：過去の攻撃はマリシャスな「floodfill」ルーターを使う手口だったが、今回は数そのものによる圧倒。I2P側は短期間で複数対策を実施し、6日で2.11.0を公開。注目点は「ハイブリッドML-KEM＋X25519」のポスト量子暗号をデフォルトで導入したこと（古典と量子耐性の組合せで将来のリスクを低減）。
- 追加改修：Sybil緩和策、SAMv3 APIの改善、インフラ強化などが合わせて実装された。匿名ネットワーク実運用でのPQ暗号標準化の先駆的事例とも言える。

## 実践ポイント
- I2Pユーザーは速やかにI2P 2.11.0以降へ更新する。
- IoT管理者はルータやSTBなどの未更新機器を洗い出し、ファームウェア更新・セグメント隔離を徹底する。
- ネットワーク運用者はノードの急増に対するアラートやレート制限、Sybil検知を導入する。
- 開発者はポスト量子暗号の検討を早め、ハイブリッド運用や鍵更新方針を策定する。
- 個人はプライバシーツールに依存しすぎず、複数手段（TorやVPN等）の併用や最新情報の確認を習慣化する。

（出典：Sam Bent「A Botnet Accidentally Destroyed I2P」要約・再構成）
