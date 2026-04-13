---
layout: post
title: "I Couldn’t Afford Earth, So I Built Something Better - 地球が買えなかったので、もっと良いものを作りました"
date: 2026-04-13T18:44:22.915Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/konark_13/i-couldnt-afford-earth-so-i-built-something-better-1506"
source_title: "I Couldn’t Afford Earth, So I Built Something Better - DEV Community"
source_id: 3487110
excerpt: "地球が買えないなら火星を買う？AI×Reactで作る宇宙不動産の裏側と実装トラブル"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fr1hqypa84cifpqf3zyeg.png"
---

# I Couldn’t Afford Earth, So I Built Something Better - 地球が買えなかったので、もっと良いものを作りました
火星にマイホーム？冗談めいたアイデアを本気で作った「SpaceEstate」の裏側と学び

## 要約
DEV投稿「SpaceEstate」は、地球が高すぎるからというジョークから生まれた“宇宙不動産”デモアプリ。React＋TypeScriptで作られ、AI（Google Gemini）やWeb3風の仕立てで遊び心あるUXを提供するプロジェクトです。

## この記事を読むべき理由
技術習作としての完成度とユーモアが両立しており、フロントエンド実装、AI連携、プロダクト設計の学びが詰まっています。日本の高騰する不動産マーケットや宇宙関連スタートアップへの関心が高い読者にも刺さる題材です。

## 詳細解説
- コンセプト：ユーザーが火星・金星・月など“惑星の土地”を閲覧・購入できるUI。ジョーク要素（異星人レビュー、限定セール、所有証明書生成）で遊び心を演出。
- 技術スタック：React + TypeScript、Vite（高速開発）、Google Gemini API（AIによる説明・推薦）、カスタムUIコンポーネント。Web3風の仕組みや証明書発行を取り入れている点も特徴。
- サーバー側のフロー（物語的）：銀河銀行接続→酸素権利確認→現地エイリアンと交渉→銀河当局への賄賂（冗談表現）→所有証明書発行、という“手続き”を擬似実装してUXを盛り上げる。
- 開発での苦労話：TypeScriptの型エラー、Reactが特定の惑星追加でクラッシュ、AI（Gemini）が存在しない月を生成する“幻覚”、重力差でUIが壊れるなど実運用で起きるバグや検証不足が題材に。
- プロダクト感：遊び・学習・見せ場が混ざった“ポートフォリオ向けプロダクト”で、デモ性・拡散力を重視した作り。

## 実践ポイント
- ポートフォリオに最適：短期間で魅せるデモを作るなら、React＋TypeScript＋Viteの組合せが速く安定。AIは説明生成やレコメンドに使うと効果的。
- 外部APIは“幻覚”や例外を想定：AIや未整備データは誤出力をする前提で検証・フェイルセーフを用意する。
- モックで早く回す：実際の「銀河銀行」など外部依存はモック化してUXを先に磨く。
- ユーモアで信頼を得る手法：レビューや証明書をジョークとして見せることでSNS拡散が狙えるが、法的・倫理的表現は注意。
- 日本向けの応用：東京の住宅高騰や若手の“資産遊び”ニーズを踏まえ、キャンペーンや学習ワークショップ（例：宇宙不動産ハッカソン）に落とし込むと受けが良い。

短く言えば——遊び心あるアイデアを技術スタックで素早く形にし、外部APIの不確実性やUXのエッジケースを丁寧に扱うことが、このプロジェクトから学べる主要な教訓です。
