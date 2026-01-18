---
layout: post
title: "Tested a random APK with MobSF out of curiosity - 好奇心でランダムなAPKをMobSFで検査してみた"
date: 2026-01-18T06:06:11.240Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@web.pinkisingh/i-reverse-engineered-the-free-movie-app-i-used-for-2-years-the-results-were-terrifying-98796cef6837"
source_title: "Tested a random APK with MobSF out of curiosity"
source_id: 425210479
excerpt: "無料映画アプリをMobSFで60秒解析、スパイ機能や平文通信が丸裸に"
---

# Tested a random APK with MobSF out of curiosity - 好奇心でランダムなAPKをMobSFで検査してみた
2年使った「無料映画アプリ」がまさかのスパイ化――60秒で丸裸にしたMobSF検証レポ

## 要約
人気のないサードパーティAPKをMobSFで解析したら、署名不備・平文通信・マイクやインストール一覧の取得といった重大な問題が見つかった。ユーザーはAPKの取り扱いに注意し、開発者はリリース前に自動解析を必須にするべきだ。

## この記事を読むべき理由
日本でもAPKを直接ダウンロードして使うケースや海外アプリを試す機会は少なくない。個人情報保護や企業のBYOD運用、アプリ審査の観点で、こうした「無料アプリ」が招くリスクを理解しておくことは実務でも重要になる。

## 詳細解説
- MobSFとは  
  MobSF（Mobile Security Framework）は、APK（またはIPA）をドラッグ＆ドロップで解析して脆弱性やプライバシー問題を自動検出するツール。ローカルで動かすならDockerが手軽で、数十秒でレポートが出る。

  例：Dockerでの起動（Windows/Mac）
  ```bash
  docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf
  ```
  起動後、http://localhost:8000 にアクセスしてAPKをアップロードするだけ。

- 検出された代表的な問題と意味
  1. 署名がDebugキー（デバッグ証明書）  
     - 意味：アプリが開発時の公開鍵（誰でも使える）で署名されている。正規リリース用の秘密鍵で署名されていないため、第三者に改ざんされやすい。改変APKを同じキーで配布すると端末が更新を受け入れてしまう危険がある。
  2. 平文通信（Cleartext traffic）許可  
     - 意味：HTTPなど暗号化されない通信を許している。ネットワーク上の盗聴で閲覧履歴や認証情報が漏れる可能性が高い。Androidでは android:usesCleartextTraffic="false" を設定するなどで対策する。
  3. 余計な権限やAPI呼び出し（例：インストール済みアプリの列挙、RECORD_AUDIO）  
     - 意味：映画再生アプリに不必要なマイクアクセスや端末内のアプリ一覧取得は、行動プロファイリングや盗聴のリスク。多くは広告SDKやサードパーティライブラリが追加する場合がある。

- なぜこれが危険か（実用的な影響）  
  - 改ざんAPKの配布：ユーザーは知らずにマルウェア入りアプリをインストールする可能性。  
  - 通信の盗聴：公衆Wi‑FiやISPによる監視で何を見ているかが漏れる。  
  - プライバシー侵害：端末内アプリや音声などを収集され、広告会社や第三者に情報が渡る。

## 実践ポイント
- 一般ユーザー向け
  - 信頼できないサイトからのAPKは極力避ける。Google Playや公式配布を優先する。  
  - インストール前に要求権限を確認する。マイクや連絡先の権限を不自然に要求するアプリは避ける。  
  - 公衆Wi‑FiではVPNを利用する。重要な認証情報は送らない。

- 開発者/運用者向け
  - リリースは必ず署名済みのReleaseキー（.jks）で行い、デバッグキーでの配布は厳禁。Play App Signingの利用を検討する。  
  - android:usesCleartextTraffic="false" を設定し、HTTPSのみを許可する。Network Security Configでさらに細かく制御する。  
  - 権限は最小限の原則に従う。サードパーティSDKが不要な権限を追加していないか依存関係を精査する。  
  - CIにMobSFや他の静的解析を組み込み、リリース前に自動でスキャンする。難読化や改ざん検知（署名検証、tamper checks）も有効。

まとめ：無料だからといって安全とは限らない。日本のユーザーと開発者は、APKの出所とアプリの振る舞いを疑い、MobSFのような自動ツールで事前チェックを習慣化しよう。
