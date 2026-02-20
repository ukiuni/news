---
layout: post
title: "Internationalise The Fediverse - フェディバースを国際化する"
date: 2026-02-20T10:07:01.670Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shkspr.mobi/blog/2024/02/internationalise-the-fediverse/"
source_title: "Internationalise The Fediverse – Terence Eden’s Blog"
source_id: 1243778866
excerpt: "非ラテン名を可能にするフェディバース実証とウェブフィンガー解決案"
---

# Internationalise The Fediverse - フェディバースを国際化する
Fediverseを本当に国際化する — Unicodeユーザー名を当たり前にするための提案

## 要約
ActivityPub/FediverseでUnicode（非ラテン文字）ユーザー名を当たり前に使えるようにすべきだ、という主張と実証（@你好@i18n.viii.fi のデモ）。技術的には仕様や実装上の障壁は小さく、WebFinger周りの調整とクライアント側のUX対応が鍵。

## この記事を読むべき理由
日本語（漢字・ひらがな・カタカナ・長音符など）を使うユーザーや日本向けサービスを作るエンジニアにとって、ユーザー名の国際化は利便性と多様性の基盤。国内外で広がるFediverseでの相互運用性に直接関わる話題です。

## 詳細解説
- 背景：著者は現代のネットは「Unicode everywhere」であるべきと主張。Mastodonなど一部サービスがユーザー名にUnicodeを許容しておらず、これが不公平・不便を生む。
- 仕様面：ActivityPubのpreferredUsernameは短い識別子として定義され、ActivityStreamsの自然言語サポートと言語マッピングがあるため、仕様上は非ラテン文字を想定できる。ActivityPubの例にも非ラテン名が含まれる。
- 実証：著者は小さなActivityPubサーバを立て、@你好@i18n.viii.fi を公開。GoToSocialや一部サーバはフォローや投稿受信ができるが、Mastodon等一部クライアント／サービスはWebFingerやURLエンコーディングの扱いで見えない／受信できない例がある。
- 主な技術的障壁と反論：
  - WebFingerのエンコード/仕様差（実装差が最大の障害）。関連イシュー：swicg/activitypub-webfinger の議論。
  - 同字体（homograph）攻撃や可読性の懸念：確かにあるがASCIIでも類似問題は存在。ドメインは punycodeで保護し、表示はクライアント側で警告や正規化・比較を行う対策が有効。
  - 入力・メンションのUX問題：キーボードが異なる／コピー＆ペースト必須は実運用上の課題。エイリアス、自動補完、検索でカバー可能。
  - 表示の怪しい合成（Zalgo）や双方向テキストはクライアントがレンダリング方針を決めるべき問題。
- 現状の取り組み：いくつかの実装は既にUTF-8ユーザー名を部分対応しており、仕様側（AP×WF）の正式化が進めば改善が加速する。

## 実践ポイント
- 実装者向けチェックリスト
  - UTF-8完全対応（NFC正規化を推奨）。
  - WebFingerリクエストの適切なURLエンコーディングを実装・テスト（例：非ASCII acct を％エンコード）。
  - preferredUsername を多スクリプトで取り扱い可能にし、ActivityStreamsの言語タグを扱う。
  - メンションUX：エイリアス、検索、コピー→貼り付け、オートコンプリートで補完。
  - セキュリティ：同字体検出や表示警告、重要操作（ログイン・決済）はドメイン検証やpunycode表示を併用。
- 運用・コミュニティ
  - 実装バグや仕様ギャップは swicg/activitypub-webfinger 等のイシューに報告・貢献する。
  - 日本市場向けサービスでは、ユーザー名のローカル表記とASCIIエイリアスを併用すると導入障壁が下がる。

短く言えば：仕様は許容しており、主要な障害は実装（特にWebFinger）とクライアントのUX。まずは自分の実装で非ラテンのActorをフォローできるか試し、WebFingerのエンコードや補助機能（エイリアス・正規化）を整備しましょう。
