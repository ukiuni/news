---
layout: post
title: "rpg.actor Game Jam - rpg.actor ゲームジャム"
date: 2026-03-28T18:20:13.373Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rpg.actor/jam"
source_title: "Game Jam - RPG Actor Registry"
source_id: 47556033
excerpt: "自分のキャラをどこでも使えるゲームを作る機会、rpg.actorゲームジャム（4/1–4/20）"
image: "https://rpg.actor/assets/cover.png"
---

# rpg.actor Game Jam - rpg.actor ゲームジャム
魅せる「持ち運べるキャラ体験」を作るチャンス：あなたのゲームがプレイヤーのキャラクターをネット上で読み書きする時代へ

## 要約
rpg.actorが主催するGame Jam（2026/4/1–4/20）は、AT Protocol上に保存されたプレイヤーのキャラクターデータ（.stats/.sprite等）を読み書きするゲームやツールを募集するイベントです。RPGツクールやGodot、Unity、Webアプリなど何でもOK、オープンソース化で信頼バッジが得られます。

## この記事を読むべき理由
- 日本ではRPGツクール／ドット絵文化が根強く、プレイヤーの「キャラを持ち運ぶ」体験はコミュニティと作品の広がりに直結します。  
- 技術的にはRESTとOAuthベースなので、HTTPが使える環境なら既存のゲームエンジンで容易に統合できます。

## 詳細解説
- コア概念：rpg.actorはAT Protocol（Bluesky等の分散ID/PDS）上にキャラ情報を保存するレジストリ。プレイヤーが自分のPDSを持ち、複数のゲームで同一キャラを持ち回れます。  
- データ仕様：主要なlexiconとして actor.rpg.stats（6つのステータス系）と actor.rpg.sprite（スプライト／服装）を提供。読み込みは認証不要、書き込みはOAuthでPDSに対して行います。カスタムシステムもあり任意のキー/値で拡張可。  
- 技術スタック：APIはPlain REST。RPG Maker MZ用プラグイン群（MZ 1.6.0+対応）やサンプルプロジェクト、開発者向けドキュメント／lexicon JSONが公開されています。対応エンジンに制限なし。  
- 審査と信頼：公開ソースでレビュー済みだとVerified、ソースありで確認済みはReviewed、未確認はUnvetted。ユーザーはテスト用Blueskyアカウントで安全にプレイ可能。  
- ルールの要点：ジャム期間中に新規にrpg.actor統合を実装すること。少なくとも1つのrpg.actor lexiconを読み書きすること。差別や有害コンテンツは禁止。  
- 賞品（抜粋）：優勝は日本語版RPGツクール2000のパッケージ＋Ultimate Creatorアカウント（100キャラ）とカスタム.worldドメイン等、上位にもCreatorアカウントが贈呈されます。

## 実践ポイント
- 今すぐできること：itch.ioのJamページに登録 → Dev GuideとSystems Referenceを読む → サンプルMZプラグインやAPIエンドポイントでプロトタイプを作る。  
- 安全なテスト：プレイヤー役は使い捨てのBlueskyアカウントを用意する。OAuthの権限は最小限に。  
- 開発上の注意：認証情報は永続保存しない／必要最小限のネットワークアクセスのみ行う。書き込みはユーザー許可を明示。  
- アイデア例：既存キャラでプレイ可能にするログインプラグイン、コンペンディウムからNPCを自動生成、衣装屋で.spriteを書き換える、.statsを使った占い・副作用ギミックなど。  
- 信頼獲得：公開リポジトリでソースを提示するとVerified取得の可能性が高まり、プレイヤーが安心してあなたの作品を試せます。

開催期間は2026/4/1–4/20。RPGツクール文化を活かす日本のインディー開発者には魅力的な機会です。興味があるならまず公式のDev Guideとitch.ioページをチェックして小さく動き始めましょう。
