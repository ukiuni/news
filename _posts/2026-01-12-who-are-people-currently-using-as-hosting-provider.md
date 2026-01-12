---
layout: post
title: "Who are people currently using as hosting providers? - 今みんなが使っているホスティングプロバイダは？"
date: 2026-01-12T03:07:41.132Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lobste.rs/s/hcpnrj"
source_title: "Who are people currently using as hosting providers? | Lobsters"
source_id: 1222661071
excerpt: "HetznerやFastMail例で用途別最適化、メール信頼性と運用負荷を具体比較"
image: "https://lobste.rs/touch-icon-144.png"
---

# Who are people currently using as hosting providers? - 今みんなが使っているホスティングプロバイダは？

魅力的タイトル: ホスティング選びの今：自宅サーバーからHetzner、FastMailまで──日本のエンジニアが知っておくべき選択肢と落とし穴

## 要約
海外の技術フォーラムでの議論を元に、現実的に使われているホスティング／メール／静的サイトの選択肢と、それぞれのメリット・注意点を整理します。

## この記事を読むべき理由
プロジェクト規模や運用方針によって「どのホスティングが良いか」は変わります。日本の開発者や個人運営者が直面する「サポートの質」「メール配信の信頼性」「コスト」「運用負荷」といった課題にすぐ役立つ視点を提供します。

## 詳細解説
- トピックの背景  
  多くのユーザは「手軽さ」と「信頼性」の板挟みになる。DreamHostのような長期ユーザからはサポート品質低下やスパムフィルタによる誤判定（場合によってはメールがバウンスされる）の不満が出ており、これが移行や代替選定の動機になっています。

- 主なカテゴリと代表的プロバイダ（議論で挙がったもの）
  - 静的サイト／CDN: Cloudflare Pages、GitHub Pages、NearlyFreeSpeech.net、pico.sh  
    → メリット：無料〜低コストで簡単。デプロイが楽。デメリット：動的処理は不得手。
  - 汎用VPS / 仮想サーバ: Hetzner、Vultr、Scaleway、OVH、Oracle Cloud（無料枠）  
    → メリット：コスト対性能が良い。自由度が高い。デメリット：管理・運用負荷、プロバイダ依存の特性（例: UIや料金体系）。
  - 専用サーバ / ベアメタル: Hetzner、OVH、Datapacket  
    → 高性能・安価だが管理が重い。
  - メールホスティング / SMTP: FastMail、PurelyMail、Migadu、SMTP2Go、Migadu  
    → メール配信の信頼性と送信専用リレー（SMTP2Go等）を分ける運用が人気。SPF/DKIM/DMARC設定は必須。
  - 小規模／ニッチ：NearlyFreeSpeech（静的＋比較的柔軟）、Mythic Beasts（DNS/メール）、BinaryLane（地域特化）など。
  - 自宅ホスティング・ホームラボ：Tailscale/WireGuardで一部を自宅に置き、フロントをVPSにするハイブリッド運用が増加。

- 技術的注意点（初心者でも押さえるべき点）
  - メール信頼性: SPF, DKIM, DMARCを正しく設定し、送信IPのレピュテーションを管理する。大手受信側のallowlist問題で「大手プロバイダ経由の送信」が必要になるケースもある（特に企業や官公庁とのやり取り）。
  - バックアップと冗長性: DNSや重要サービスを一ヶ所に集中させない。支払いトラブルで一挙にダウンするリスクあり。
  - サポート品質: 価格だけでなく「迅速に人間と話せるか」「実務的に助けてくれるか」を評価する。海外プロバイダでも技術サポート重視の所はある。
  - レイテンシと法律/データ保護: 日本ユーザ向けなら東京拠点や近隣のリージョンを選ぶと遅延が小さい。個人情報やログ保存に関わる法規（国内データ保管要件など）も確認する。

## 実践ポイント
- まず要件を分解する：静的サイト、動的API、受信メール、送信メール、バックアップ—それぞれ最適な選択肢を分ける。
- メールは分離運用：受信は専門ホスティング（FastMail/Migadu等）、送信はSMTPリレー（SMTP2Go等）で信頼性を確保。
- 小規模ならCloudflare Pages / GitHub Pages + Cloudflare CDNで高速かつ低運用。
- コスト重視だが柔軟性も欲しいならHetznerやOVHのVPS／専用機を検討。ただし管理の手間を考慮。
- 日本向けサービスが必要なら、国内事業者（さくらのVPS、GMO、ConoHa等）も候補に入れる。言語サポート・決済・国内リージョンでメリットあり。
- すぐできるチェックリスト：
  - SPF/DKIM/DMARCが設定済みか
  - 自動バックアップとリストア手順があるか
  - サポートの連絡手段（チャット/電話/チケット）と応答時間
  - 料金の見通し（転送量、IO、スナップショット課金など）

短く結論：用途ごとに使い分けるのが現実解。完全自主管理は楽しいが運用コストとリスクがあるため、メールや重要サービスは信頼できる外部サービスを併用すると実務的に強い。
