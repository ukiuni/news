---
layout: post
title: "Patch Tuesday update makes Windows PCs refuse to shut down - Patch Tuesdayの更新でWindows PCがシャットダウンを拒否する"
date: 2026-01-17T01:22:15.790Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theregister.com/2026/01/16/patch_tuesday_secure_launch_bug_no_shutdown/"
source_title: "Patch Tuesday update makes Windows PCs refuse to shut down • The Register"
source_id: 425136102
excerpt: "Patch TuesdayでWindowsがシャットダウン不能に—業務端末の電源トラブルに要警戒"
image: "https://regmedia.co.uk/2022/08/16/hal_shutterstock.jpg"
---

# Patch Tuesday update makes Windows PCs refuse to shut down - Patch Tuesdayの更新でWindows PCがシャットダウンを拒否する
魅惑のタイトル案: 「シャットダウンしないWindows増殖中：Patch Tuesdayで“永遠に起動”になる不具合が来日中？」 

## 要約
Microsoftの1月Patch Tuesday適用後、Windows 11 23H2の一部で「シャットダウン／再起動／ハイバネートが完了しない」不具合が発生。原因はSecure Launchに関連するとされ、強制シャットダウンコマンドなどで回避可能だが、根本的な修正は次回以降の更新待ち。

## この記事を読むべき理由
日本でもノートPCのバッテリー消耗や業務端末の運用停止リスクにつながるため、個人ユーザーだけでなく社内PC管理者（Windows Updateポリシーを運用する担当者）は早急に影響範囲把握と対策が必要です。

## 詳細解説
- 何が起きているか：1月のセキュリティ更新適用後、影響を受けた端末は画面がオフになってもプロセスが止まらず、物理的に電源が落ちないケースがあります。見た目は通常通りシャットダウン処理が走るように見えても、実際にはOSが電源制御を完了しません。
- 原因の見立て：Microsoftはこの不具合をSecure Launch（起動時に信頼できるコンポーネントのみを読み込むための仮想化ベースの保護機能）に紐づく問題としている。Secure Launchが有効な環境で電源操作が失敗する事例が報告されています。
- 影響範囲：現時点で同社は詳細な発生件数を提示しておらず、主にWindows 11 23H2を実行する端末で報告されています。個人ノートPC、業務用ラップトップ、VDIや一部の仮想化設定を使う環境が想定されます。
- 対応状況：正式な修正パッチはまだ提供されておらず、Microsoftは「将来の更新で解決予定」と案内中。暫定対応として「shutdown /s /t 0」で強制シャットダウンが可能とされています。

bash
```bash
shutdown /s /t 0
```

（上記コマンドは管理者権限のコマンドプロンプト／PowerShellで実行）

## 実践ポイント
- 今すぐやること（個人ユーザー）
  - 作業中のデータはこまめに保存。突然電源が切れないことでバッテリー切れ→作業終了に失敗する可能性があるため。
  - シャットダウンできない場合は管理者権限で上記の強制シャットダウンコマンドを試す。
- 今すぐやること（IT管理者）
  - 社内のアップデート配布を一時的に保留（WSUS / Intuneの更新リングで遅延）し、まずは影響端末の有無を検証する。
  - テスト環境で今回の更新を先行適用し、Secure Launchが有効な構成で再現確認を行う。
  - 端末での発生ログ（イベントビューアの電源関連イベント）を収集し、Microsoftサポートへ報告する準備をする。
- 中長期的対応
  - MicrosoftのWindows release healthやセキュリティアドバイザリを定期的にチェックし、修正パッチ配布を待つ。
  - Secure Launchや仮想化ベースのセキュリティ設定は有効のままが望ましいため、安易に無効化しない。どうしても業務に差し支える場合は、影響範囲を把握した上で段階的に設定変更を検討する（その際はリスク評価を実施）。
- 日本固有の注意点
  - モバイルワークやハイブリッド勤務が普及している現場では、バッテリー消耗が続けば業務継続性に直結します。更新ポリシーの見直しや社内周知を早めに行うべきです。

短くまとめると、「重要なセキュリティ更新を適用する価値は高いが、運用側は今回のような副作用に備えて更新の遅延/テスト運用と迅速な回復手順を整備しておく必要がある」――という事態です。
