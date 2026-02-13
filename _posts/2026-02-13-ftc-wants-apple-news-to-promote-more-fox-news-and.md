---
layout: post
title: "FTC wants Apple News to promote more Fox News and Breitbart stories - FTCがApple NewsにFox NewsやBreitbartの記事をもっと目立たせるよう要求"
date: 2026-02-13T21:21:29.214Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/02/trump-ftc-denies-being-speech-police-but-says-apple-news-is-too-liberal/"
source_title: "Trump FTC wants Apple News to promote more Fox News and Breitbart stories - Ars Technica"
source_id: 443684965
excerpt: "FTCがAppleにFoxやBreitbartの掲載促進を要求、配信中立性が焦点に"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/02/apple-news-app-1152x648-1770927170.jpg"
---

# FTC wants Apple News to promote more Fox News and Breitbart stories - FTCがApple NewsにFox NewsやBreitbartの記事をもっと目立たせるよう要求
米FTCが「Apple Newsは保守系を抑圧している」と警告—プラットフォームの中立性と透明性が争点に

## 要約
米連邦取引委員会（FTC）委員長がAppleに対し、Apple Newsが保守系メディアを抑制している可能性を指摘する書簡を送付。根拠は親トランプ系の調査で、FTCは消費者保護法の観点から利用規約と実務の整合性を検証するよう求めている。

## この記事を読むべき理由
プラットフォームの推薦・編集方針が規制の対象になりうる点は、世界の大手プラットフォーム運用や日本のニュース配信サービス（例：LINE NEWS、SmartNews）にも波及する可能性があるため、プロダクト設計や法務・運用の実務担当者は動向を押さえておくべきです。

## 詳細解説
- 何が起きたか：FTC委員長アンドリュー・ファーガソンがティム・クック宛に書簡を送り、Apple Newsが「左派寄りの記事を優先、保守系を抑えている」との報告に基づき利用規約との矛盾を調査するよう要請しました。根拠として示されたのはMedia Research Center（保守系団体）の分析。
- 法的論点：FTCは「我々は言論の警察ではない」としつつ、消費者に対する誤認表示や重要な情報の不開示（material omission）があればFTC法違反となる可能性を指摘。Apple側の利用規約はコンテンツを「as‑is」と明記しており、同意の有無で争点が分かれる構図です。
- 関係者の反応：一部メディア擁護団体やFCC委員長は政府介入を支持。対して表現の自由や政府による恣意的な検閲を懸念する声もあり、First Amendment（米国憲法修正第1条）や行政の越権性が争点になります。
- 技術面の背景：ニュース配信は人による編集とアルゴリズム推薦のハイブリッドで動き、指標（露出回数、ランキング、キュレーションルール）次第で偏りが生まれる。調査は「朝のトップ20記事」など限定的なサンプルで行われており、測定手法の設計が結論に影響します。
- 波及事項：FTCの動きは「透明性の強制」「利用規約の明確化」「第三者監査」の方向につながる可能性があり、グローバルなプラットフォーム運用やローカルなニュースアグリゲーターにも適用されうる先例となり得ます。

## 実践ポイント
- プロダクト/法務：利用規約に「キュレーション方針」「アルゴリズムの役割」「ユーザーの期待値」を明示しておく。透明性報告の定期公開を検討する。  
- エンジニア：推薦パイプラインのログ、ソースごとの露出統計、A/Bテストのメタデータを保存し、外部監査に備える。バイアス検出用の簡易メトリクス（ソース分布の差分など）を導入する。  
- ジャーナリスト/利用者：複数のアグリゲーターを比較・参照し、出所の多様性を確保する。ソース信頼度評価ツールの活用を検討する。

以上。
