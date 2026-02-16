---
layout: post
title: "Hardware TOTP authenticator with 8-layer security architecture (ESP32) - 8層セキュリティ構成のハードウェアTOTP認証器（ESP32）"
date: 2026-02-16T12:54:01.138Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/makepkg/SecureGen"
source_title: "GitHub - makepkg/SecureGen: 🔐 Hardware TOTP Authenticator &amp; Password Manager | 8-layer security | AES-256 | BLE Keyboard | Offline | ESP32 T-Display"
source_id: 1041647198
excerpt: "ESP32ベースの低コストハードウェアTOTPが8層セキュリティでオフライン運用・BLE送信とWeb管理を実現"
image: "https://opengraph.githubassets.com/e3369991eb74c70b37206e8b5ec484346dad9bdd8999e1ed59ca8fa4f51b3b05/makepkg/SecureGen"
---

# Hardware TOTP authenticator with 8-layer security architecture (ESP32) - 8層セキュリティ構成のハードウェアTOTP認証器（ESP32）
ポケットで使える“軍用級”二段階認証＆パスワードマネージャ──SecureGenで始めるオフライン運用

## 要約
SecureGenはESP32（TTGO T-Display）上で動くオープンソースのハードウェアTOTP認証器兼パスワードマネージャで、AES-256やECDHなどを組み合わせた「8層」防御で通信・保存データを保護します。BLEキーボード送信やオフライン運用、ウェブ管理UIも備え、低コストで自己管理できるセキュアトークンを実現します。

## この記事を読むべき理由
日本でもリモートワークや個人運用のセキュリティ需要が高まる中、安価なESP32ベースで自己管理できるハードウェア認証器は、企業の2FA導入や個人の機微情報保護に即戦力となるため。

## 詳細解説
- ハードウェア基盤：LILYGO TTGO T-Display（ESP32、ST7789 TFT、Li-Po対応）。PlatformIO＋VS Codeでビルド・書き込み可能。ソースはGitHubで公開。
- 機能：
  - TOTP生成（Google Authenticator互換）
  - オフラインパスワードボールト（AES-256で保存）
  - BLEキーボードによるパスワード送信（LE Secure Connections、ペアリング＆ボンディング）
  - Web UI（AP/Clientモード）で管理・QRインポート・暗号化バックアップ
- セキュリティ設計（主な8層）：
  1. ECDH（P-256）による鍵交換（前方秘匿性）
  2. セッション毎の暗号化（メッセージカウンタ/リプレイ保護）
  3. URLの動的難読化（SHA-256ベースでエンドポイントを回転）
  4. ヘッダ動的マッピング（メタデータ漏洩軽減）
  5. フェイクヘッダ注入（トラフィック解析攪乱）
  6. メソッドトンネリング（HTTPメソッドを隠蔽）
  7. タイミング保護（ランダム遅延でサイドチャネルを緩和）
  8. ハニーポット／偽エンドポイント（侵入検知と時間稼ぎ）
- 保管側：AES-256、PBKDF2-HMAC-SHA256での鍵導出、ハードウェア由来の一意鍵、セキュアブート／安全なワイプ機能を想定。
- 実装スタック：mbedTLSを利用した暗号処理、ESP32のハードウェア暗号アクセラレーション、独自セッション管理。ネットワーク負荷は概ね1リクエストあたり約50msのオーバーヘッドと報告。
- 電源・運用：スリープ／ライトスリープ、NTP同期（TOTP精度のため）、ファクトリリセットと管理者パスワード/起動PIN（4–10桁）。

## 実践ポイント
- まずリポジトリをクローンしてPlatformIO（VS Code拡張）でビルド→TTGOに書き込んで動作確認する。
- 最小権限で運用するなら「オフライン（エアギャップ）モード」を選び、必要時のみAPまたはClientモードで管理。
- BLEで送信する場合は必ずペアリング＋ボンディング、PIN設定、古い結合の削除を徹底する。
- 管理者パスワードとバックアップの暗号化パスフレーズは強固にし、定期的に暗号バックアップを行う。
- 日本の現場では、社内ポリシーや資産管理と合わせて「個人利用→チーム展開」の段階的導入を検討すると導入コストと運用リスクが抑えられる。

元記事（実装・ドキュメント）はGitHub: https://github.com/makepkg/SecureGen を参照してください。
