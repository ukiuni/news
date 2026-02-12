---
layout: post
title: "Microsoft's Notepad Got Pwned (They Added AI To It, So...) - MicrosoftのNotepadが乗っ取られた（AIを追加したせいで…）"
date: 2026-02-12T15:16:58.154Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://foss-daily.org/posts/microsoft-notepad-2026/"
source_title: "Microsoft's Notepad Got Pwned (They Added AI To It, So...) | FOSS Daily!"
source_id: 443581836
excerpt: "Markdownプレビューの欠陥でNotepadがRCE被害、即座に11.2510へ更新を"
---

# Microsoft's Notepad Got Pwned (They Added AI To It, So...) - MicrosoftのNotepadが乗っ取られた（AIを追加したせいで…）
Notepadの一クリックで全システムが危険に――Markdownプレビューが招いたRCEの真相

## 要約
Microsoft製の「モダンNotepad」（Microsoft Store版）に、Markdownハンドラの不備を突くRCE脆弱性（CVE-2026-20841、CVSS 8.8）が見つかり、特製の.mdファイル＋リンククリックでフル権限のコード実行が可能でした。11.2510で修正済み。

## この記事を読むべき理由
日本の企業や開発者はWindows依存が高く、社内で共有されるREADMEやメモがMarkdown形式で回ることが多い。無害に見える.mdファイルが入口になり得る点は、即座に対処すべき実務上のリスクです。

## 詳細解説
- 何が起きたか：NotepadのMarkdownプレビューはリンクの中身を十分に検証せず、特定のプロトコル（スキーム）を含むリンクをクリックすると外部実行を行ってしまう。これによりユーザー権限で任意コード実行（RCE）が可能に。
- 技術情報：CVE-2026-20841、CVSS 8.8（High）。影響バージョンは Notepad 11.0.0〜11.2509。修正は 11.2510（2026-02-10公開）。利用にはユーザーのクリックが必要だが、クリック誘導はフィッシングで簡単に可能。PoCが公開済み。
- 影響範囲：モダンNotepad（Microsoft Store配布）のみ。従来の legacy Notepad.exe（古いOS組み込み版）は影響外。開発者やIT管理者は特に注意。
- 根本原因の示唆：単純なエディタに機能（Markdown/AI/リンク実行）を追加すると攻撃面が増え、基本的な検証が抜けると致命的になる典型例。

## 実践ポイント
- 今すぐやること：
  - NotepadをMicrosoft Storeで更新→バージョン11.2510以降にする（Notepadのメニュー → Aboutで確認）。
  - 見つけ次第、社内のWindows端末に対してパッチ適用を優先課題にする。
- 設定で攻撃面を減らす：
  - Markdownプレビューを無効化
  - AI提案やリンクの自動実行をオフに
- 運用面の注意：
  - 不明な送信者からの.mdファイルは開かない、リンクをクリックしない
  - 開発環境や共有フォルダに入ってくる外部ファイルの取り扱いポリシーを見直す（サンドボックスで確認する等）
- 参考値（簡易）：CVE-2026-20841 / CVSS 8.8 / 影響版 11.0.0–11.2509 / 修正 11.2510+

以上。迅速なアップデートと設定見直しを推奨します。
