---
layout: post
title: "Mozilla accuses Microsoft of sabotaging Firefox with Windows and Copilot tactics - マイクロソフトがWindowsとCopilotでFirefoxを妨害と告発"
date: 2026-04-10T14:53:31.412Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.mozilla.org/en/mozilla/ai/microsoft-copilot-ai-user-choice/"
source_title: "Old habits die hard: Microsoft tries to limit our options, this time with AI"
source_id: 365356977
excerpt: "Mozilla告発：MicrosoftがCopilotでFirefoxの選択肢を奪い支配を狙う"
image: "https://blog.mozilla.org/wp-content/blogs.dir/278/files/2026/04/Browsing_1920x1080-1080x720.jpeg"
---

# Mozilla accuses Microsoft of sabotaging Firefox with Windows and Copilot tactics - マイクロソフトがWindowsとCopilotでFirefoxを妨害と告発
Windowsが“強制AI”キーで選択を奪う？Mozillaが暴いたCopilotの実態

## 要約
Mozillaは、MicrosoftがCopilotの自動導入や物理キーの追加、タスクバー固定などで利用者の選択肢を狭め、競合ブラウザやプライバシーを圧迫していると告発。Mozillaはこれに対し、Firefoxに一括でAI機能を無効化できる「AI Controls」を導入して対抗している。

## この記事を読むべき理由
日本でもWindowsは広く使われており、企業や個人のデフォルト体験が操作されると競争やプライバシーに直結します。AI統合がデフォルトで押し付けられる流れは、日本の開発者やユーザーにも影響します。

## 詳細解説
- Microsoftの手法（Mozillaの主張）
  - M365 Copilotアプリがユーザーの許可なく自動的にインストールされる事例が報告された。
  - ノートPCに専用の物理キーを追加し、押すとCopilotが起動するように設定（簡単にリマップできない場合あり）。
  - WindowsのタスクバーにCopilotが既定でピン留めされ、通知領域・設定アプリ・エクスプローラーなどOSの主要領域へ統合しようとした。
  - これらはユーザーの明示的な同意を得ずに短期間でデータ収集・学習を促す設計だったと指摘される。
- 「ダークパターン」の常態化
  - Mozillaの研究は、既定ブラウザの変更を難しくするUIや、Windows Searchが強制的にEdgeを開くなどの事例を挙げ、選択を妨げる設計が繰り返されていると警告。
- Mozillaの対抗策
  - FirefoxはAI機能を「人が主導」で使えるよう設計。翻訳やPDFのaltテキスト生成などローカル処理の機能を強調。
  - Firefox 148で「AI Controls」パネルを導入。全AI機能を一括オフにする「Block AI Enhancements」と、個別のオン／オフを保持する仕組みを実装し、アップデート後も設定が保持されるようにしている。

## 実践ポイント
- 自分の環境を確認：タスクバーやスタートアップに見慣れないAIアプリがないかチェックする。  
- 既定アプリを確認・固定：ブラウザやメールの既定設定を定期的に確認する。  
- キーのリマップ：Copilotキーが勝手に動く場合はキーボードソフトやOS設定でリマップ／無効化を検討。  
- ブラウザ選びでコントロールを優先：AI機能のオンオフやローカル処理を重視するなら、FirefoxのAI Controlsなど設定性の高いブラウザを使う。  
- 企業管理者はMDM/GPOを活用してデフォルト設定を管理し、ユーザーの選択権を守る方針を検討する。

（出典：Mozilla公式ブログ「Old habits die hard: Microsoft tries to limit our options, this time with AI」）
