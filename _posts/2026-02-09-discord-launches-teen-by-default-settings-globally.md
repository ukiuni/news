---
layout: post
title: "Discord Launches Teen-by-Default Settings Globally - Discord、未成年（ティーン）向けデフォルト設定を世界展開"
date: 2026-02-09T16:45:20.350Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discord.com/press-releases/discord-launches-teen-by-default-settings-globally"
source_title: "Discord Launches Teen-by-Default Settings Globally"
source_id: 808376255
excerpt: "Discordが世界展開、未成年向けデフォルト設定で顔認証やDM制限など安全機能を標準化"
---

# Discord Launches Teen-by-Default Settings Globally - Discord、未成年（ティーン）向けデフォルト設定を世界展開
Discordが“10代優先”に—プライバシー重視の年齢認証でゲームチャットの安全が変わる

## 要約
Discordは全世界で「ティーン向けをデフォルト」にする安全強化を展開。年齢保証（顔年齢推定、ID、推論モデル等）を軸に、未成年向けの通信制限やコンテンツフィルタを標準化します。

## この記事を読むべき理由
日本でもゲーム／コミュニティ系サービスの利用は若年層が多く、運用側（コミュニティ管理者・開発者）や保護者に直接影響します。設定変更や年齢確認の導入に備えて挙動と対策を押さえておくべきです。

## 詳細解説
- ロールアウト時期：段階的に3月初旬から全ユーザーへ適用。既存ユーザーも対象。
- 年齢保証の仕組み（Privacy‑forward）
  - 顔年齢推定（video selfie）は端末内で処理、サーバに送られない設計。
  - ID提出はベンダーへ送付後、確認後速やかに削除（多くは即時）。
  - バックグラウンドで動く年齢推論モデルで、常に検証を要求しない運用。
  - 必要時は複数手法での確認を求める場合あり。認証状況は他ユーザーに非表示。
- 新しいデフォルト安全設定（未成年向け）
  - 敏感コンテンツの自動ぼかし：成人と確認されるまで解除不可。
  - 年齢制限スペース：成人認証済みのみアクセス可能なチャンネル/サーバ/コマンド。
  - DM受信：見知らぬ相手からのメッセージは別受信箱へルーティング。設定変更は成人認証者のみ。
  - フレンド申請やステージ発言に警告・制限を導入。
- 参加とガバナンス：13–17歳の意見を反映する「Teen Council」設置（10–12名、応募は〜2026/5/1）。

## 実践ポイント
- ユーザー（保護者・ティーン）：アカウントの「My Account」で年齢保証の方法と結果を確認・再申請可能。プライバシー設計は端末処理／短期削除を謳うが、提出前に利用規約・削除ポリシーを確認。
- サーバ管理者・コミュニティ運営者：サーバの年齢制限チャンネルやBot権限設定を見直し、成人向けコンテンツの管理ポリシーを更新。
- 開発者／プロダクト担当：Discord APIや認証フローに影響が出る可能性があるため、連携アプリや自動モデレーションの挙動を検証しておく。
- 学校・団体・保護者向け：Family CenterやGuardian向け資料を確認し、子どものオンライン利用ルールを再整備する。

（原題: "Discord Launches Teen-by-Default Settings Globally"）
