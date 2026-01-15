---
layout: post
title: "New Social Web Working Group at W3C - W3Cで新設：ソーシャルウェブ作業部会"
date: 2026-01-15T20:20:05.402Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://socialwebfoundation.org/2026/01/15/new-social-web-working-group-at-w3c/"
source_title: "New Social Web Working Group at W3C |  Social Web Foundation"
source_id: 1417714468
excerpt: "W3CがActivityPub改訂へ新作業部会を設立、LOLA統合でマストドン運営に大影響"
image: "https://s0.wp.com/_si/?t=eyJpbWciOiJodHRwczpcL1wvaTAud3AuY29tXC9zb2NpYWx3ZWJmb3VuZGF0aW9uLm9yZ1wvd3AtY29udGVudFwvdXBsb2Fkc1wvMjAyNFwvMDlcL2Nyb3BwZWQtbG9nby0xLnBuZz9maXQ9NTEyJTJDNTEyJnNzbD0xIiwidHh0IjoiU29jaWFsIFdlYiBGb3VuZGF0aW9uIiwidGVtcGxhdGUiOiJlZGdlIiwiZm9udCI6IiIsImJsb2dfaWQiOjIzNzA2NDQyOH0.SUMDBRSsSSdefaRCQvW4_4tqRF7b5zVVG8glFADLWgkMQ"
---

# New Social Web Working Group at W3C - W3Cで新設：ソーシャルウェブ作業部会
ActivityPubの次世代改訂へ—日本のマストドン／フェデレーション運営者が注目すべき変化

## 要約
W3Cに新しい「Social Web Working Group」が立ち上げられ、ActivityPub と Activity Streams の後方互換を保った改訂版を2026年第3四半期に出すことを目標に作業が始まりました。Social Web Foundation や既存の Community Group と連携し、データ移行（LOLA）など実務に直結する規格の整理が進みます。

## この記事を読むべき理由
ActivityPubはマストドンなどフェデレーション型SNSの基盤技術で、日本でも多くのユーザーとサーバーが稼働しています。仕様の明確化とデータポータビリティ標準化は、サービス運営・開発・ユーザ利便性に直接影響するため、日本の開発者や運営者は今から準備する価値があります。

## 詳細解説
- 背景：Activity Streams（2017年）と ActivityPub（2018年）は普及した一方、実装や運用の蓄積で「わかりにくい箇所」や「不足機能」が顕在化しました。いくつかはerrataで修正されていますが、根本的な文書の整理が必要になっています。
- 新ワーキンググループの目的：既存の実装に影響を与えない「後方互換」を維持しつつ、仕様を読みやすく、実装しやすく改訂すること。目標リリースは2026年第3四半期。
- 役割分担：Social Web Community Group（これまで拡張や実験的機能を担ってきた）と密に連携し、Community Group は拡張機能（地理情報やスレッド化など）を引き続き扱い、Working Group はコア文書の改訂に注力します。
- データポータビリティ（LOLA）：Community Group 発の「LOLA」（ライブなデータ移行仕様）が Working Group に取り込まれる予定。LOLAはユーザーがサーバー間でコンテンツ、つながり、リアクションを保ったまま移動できる仕組みを目指すもので、実運用での利便性を大きく高めます。
- コミュニティ参加：ワーキンググループはW3C会員組織の代表や外部専門家で構成され、議事は公開。Darius Kazemi 氏がチェアを務め、作業は ActivityPub の GitHub レポジトリで追跡できます。
- 影響範囲：ActivityPubは既に何百万の利用者、何十億の投稿・メディアを扱う実装が存在します。したがって今回の作業は漸進的（evolutionary）であり、破壊的な変更は予定されていません。

## 実践ポイント
- 今すぐやること
  - 現行の実装を継続して問題ありません。破壊的変更の心配は不要です。
  - ActivityPub の GitHubリポジトリ（Issuesの「Next Version」タグ）を定期的にチェックして、議論されている改善点を把握する。
  - Social Web Community Group の動きをフォローし、興味ある拡張（例：LOLA）にコメントや提案で参加する。
- 運営者向け
  - サーバー間のデータエクスポート/インポート機能を整理し、LOLAに対応する準備を始める（ユーザーデータ・つながり・リアクションの完全移行を意識）。
  - 互換性テスト（既存クライアント／サーバーとの相互運用性）を自動化しておく。
- 開発者向け
  - SDKやクライアントライブラリは、将来の仕様の細かい文言変更に対応しやすいテストと抽象化を取り入れる。
  - 日本語コミュニティ（MastodonやMisskeyのローカル運営コミュニティ）で情報共有し、実運用で見つかった問題をフィードバックする。

W3Cワーキンググループの動きはオープンで追いやすく、今から関わることで仕様形成に影響を与えられます。日本のフェデレーションエコシステムを安定・発展させるために、関心のある開発者や運営者は参加と準備を始めましょう。
