---
layout: post
title: "The 2FA app that tells you when you get `314159` - 「314159」を知らせる2FAアプリ"
date: 2026-03-14T22:13:45.107Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.jacobstechtavern.com/p/building-a-2fa-app-that-detects-patterns"
source_title: "The 2FA app that tells you when you get `314159`"
source_id: 382969720
excerpt: "時刻ベースのTOTPを先読みし、314159などのレア6桁到来を通知する遊べる2FAアプリ"
image: "https://substackcdn.com/image/fetch/$s_!K9t0!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb0f90b16-14b6-4c9d-9c34-5eb3f5b1bff5_1246x1202.png"
---

# The 2FA app that tells you when you get `314159` - 「314159」を知らせる2FAアプリ
Pi Day発の遊び心：あなたの2段階認証が“レアな番号”を見つけて通知するアプリ

## 要約
6桁TOTP（時刻ベースOTP）を先読みして、連続数字や素敵な並び（例：333333、314159）を検出し、到来時にプッシュで知らせるというプロジェクトの紹介。技術的にはTOTP生成の事前計算、正規表現によるパターン検出、iOSの通知スケジューリングが肝。

## この記事を読むべき理由
2FAは日常的な作業だが、その仕組みの理解と「遊べる」応用（パターン検出・通知）は、セキュリティ運用・アプリ開発双方で役立つ実践的な知見を与えるため。日本の開発者やセキュリティ愛好家にも応用の余地が大きい。

## 詳細解説
- TOTPの本質：共通の秘密鍵と時刻（通常30秒ごと）をハッシュして6桁を作る。カウンタは $counter = \left\lfloor\frac{t}{30}\right\rfloor$ で算出され、HMAC-SHA1で固定的にコードが生成されるため再現可能。  
- 事前計算（precompute）：TOTPは決定論的なので未来の時刻を列挙してコードを生成できる。これで「いつどのコードが出るか」を予測し、興味あるパターンを探す。  
- パターン検出：正規表現で「同一数字の連続（トリプル／クアッド／クインツ／セクス）」や「円周率の断片（314159）」などを判定し、興味度（enumで管理）を付ける。  
- 通知スケジューリング：iOSでは事前に通知をスケジュールしておき、該当時刻にUNCalendarNotificationTriggerでプッシュ。制約としてiOSは同時にスケジュール可能な通知数に上限（約64件）があるため、バッチ再計算やユーザー誘導で補う設計が必要。  
- 実装周辺：QR（otpauth://）から秘密鍵を読み取りKeychainに安全保存、複数アカウント管理、UIはSwiftUIのList等で軽量に。大量生成はCPU負荷が高いのでバッチ処理／ローカル永続化で最適化する。  
- プライバシーと安全性：秘密鍵は端末のKeychainに保管し、外部サーバへアップロードしない設計が重要。iCloudキーチェーン同期を使えば端末間での利便性も確保できる（ただし実装と運用ルールに注意）。

## 実践ポイント
- TOTPの基本を押さえる：$counter=\lfloor t/30\rfloor$ と HMAC-SHA1 による決定論的生成を理解する。  
- 未来分を事前計算してパターン検索：必要な秒数分（例：数万〜百万ステップ）だけ先読みしてフィルタをかける。  
- iOS通知の制約に対応：64件上限を考慮して、重要度の高い通知だけ先に登録し、残りはアプリ起動時に再スケジュールする。  
- 秘密鍵の取り扱い：Keychain保存＋可能ならiCloudキーチェーン同期。決してサーバ保存しない。  
- UX設計：ユーザーが検出したいパターンを選べる設定と、QRスキャン→保存→一括再計算のワークフローを用意する。  
- 性能対策：ハッシュ生成は重いのでバッチ化・並列処理・キャッシュ保存でボトルネックを回避する。

短くまとめると、「TOTPの決定論的性質を活かして未来を探索し、レアな6桁が来た瞬間に教える」――遊び心と実装上のトレードオフ（通知上限・鍵の安全管理・計算コスト）を理解すれば、日本の開発者にもすぐ試せるアイデアです。
