---
layout: post
title: "AGENTS.md as a dark signal - AGENTS.md はダークシグナルとして"
date: 2026-01-23T14:54:06.373Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://joshmock.com/post/2026-agents-md-as-a-dark-signal/"
source_title: "AGENTS.md as a dark signal // Josh Mock"
source_id: 811660774
excerpt: "AGENTS.mdで自動化の利便と人間検査不足のリスクを両立させる運用法"
---

# AGENTS.md as a dark signal - AGENTS.md はダークシグナルとして
AGENTS.mdが示す「自動化の恩恵」と「ヒューマンチェック喪失」の境界線

## 要約
GitHub Copilotなどのエージェントに学習のメモを残すためのAGENTS.mdは、将来の自動化のために有益だが、同時に「このリポジトリはAI任せで人間の検査が薄いかも」という警告サインにもなり得る。

## この記事を読むべき理由
AI支援コーディングが普及する今、OSSや社内プロジェクトの信頼性を保つには、エージェント運用ルールと実務的な防御策が必須。日本の開発現場（Windows利用者比率やガバナンス重視の企業文化）にも直結する話題です。

## 詳細解説
- 背景：著者はCopilotの「エージェント」に日常の雑務を任せた実験を実施。エージェントは自動でユニットテストを書いたが、テストが実行されないCI設定（テストのglobbingパターン等）に気づかず、OS差異（Windowsで失敗する可能性）を見落とした。
- AGENTS.mdの意図：エージェントに「学習したこと」や「注意点」を永続的に残し、後続のエージェントが文脈を継承できるようにする。簡潔で賢いアイデア。
- ダークシグナル論：一方でリポジトリにAGENTS.mdやCLAUDE.mdがあると、シニアエンジニアには「人間の検査が乏しい」「vibe coding（雰囲気で動くコード）」の痕跡に見える。実際には無自覚に補完機能で“vibe”している貢献者もいるため、AGENTS.mdは批判の対象にも防護策にもなる二面性がある。
- メンテナ視点：外部PRを受けるOSSや社内公開プロジェクトでは、AGENTS.mdでエージェントの挙動制限やチェックポイントを明示しておくことが、誤った自動変更を未然に防ぐ最良策になり得る。

## 実践ポイント
- AGENTS.mdを設置して、エージェントに残すべき情報（実行環境、苦手なパターン、CIの注意点）を明確にする。
- CIは必ずWindows/Linuxで実行し、テストglobパターンが意図通りテストを拾うことを検証する。
- エージェント生成のPRはラベル付け＆必須の人間承認を設定する。
- エージェントに与える権限を絞り、変更ログ（何を学んだか）をAGENTS.mdに書かせる運用にする。
- リポジトリのREADMEやCONTRIBUTINGで「エージェントガイドライン」を公開し、外部貢献者に周知する。

短いAGENTS.md例（テンプレート）:
```md
# AGENTS.md
- agent-name: github-copilot
- allowed-actions: lint, tests, draft-pr
- disallowed-actions: merge, modify-ci
- env-notes: CI runs on ubuntu-latest + windows-latest; tests use glob "**/*test*.py"
- learnings: Windows path separator issues; avoid altering binary blobs
```

このバランスを取れば、エージェントの利便性を活かしつつ「ダークシグナル」を信頼できるガードレールに変えられます。
