---
layout: post
title: "GitHub backs down, kills Copilot pull-request ads after backlash - GitHubが撤回、反発でCopilotのプルリク広告を削除"
date: 2026-03-31T07:09:28.317Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theregister.com/2026/03/30/github_copilot_ads_pull_requests/"
source_title: "GitHub backs down, kills Copilot PR ‘tips’ after backlash • The Register"
source_id: 47582984
excerpt: "GitHubがCopilotのPRに広告を自動挿入、反発で即撤回"
image: "https://regmedia.co.uk/2024/05/21/github1_shutterstock.jpg"
---

# GitHub backs down, kills Copilot pull-request ads after backlash - GitHubが撤回、反発でCopilotのプルリク広告を削除
開発者のPRにAIが「広告」を差し込む時代への警鐘 — あっという間に機能撤回へ

## 要約
GitHub Copilotの「tips（プルリク内に挿入されるメッセージ）」が、開発者のプルリクエスト（PR）に第三者サービスの案内を自動で差し込んだとして批判が殺到。GitHubは該当のtipsをPRコメントから削除すると発表した。

## この記事を読むべき理由
AIエージェントがリポジトリ上の説明やコメントを書き換えうる現実は、権限管理・信頼性・企業コンプライアンスに直接関わります。日本の企業やOSSコントリビュータも同様のリスクに備える必要があります。

## 詳細解説
- 何が起きたか：オーストラリアの開発者が、同僚のPRのタイポ修正をCopilotに頼んだところ、CopilotがPRコメントに「Raycastを使えばここからエージェントを起動できる」等の案内（いわゆるtip）を挿入。検索すると11,400件超のPRに同様のtipが見つかった。
- 技術的背景：Copilotのレビュー統合は、特定条件で「エージェントがPRを操作・コメントする」機能を持つ。今回の挙動は「あるPRでCopilotが言及された場合に、そのPR（作成者が人間でも）にtipsを差し込む」仕様変更が影響した模様。
- 反応と対応：コミュニティの反発を受け、GitHubのCopilot担当者は「人の書いたPRに無断で変更を加えるのは判断ミスだった」と認め、該当tipsをPRコメントから無効化。後日、GitHubはロジックの誤りとして公式声明を出した。
- 問題点の本質：自動化エージェントが「誰の意図で」「どのPRを」「どの範囲で」編集できるかは、信頼・監査証跡・広告・プロンプト注入といった複数の懸念を同時にもたらす。

## 実践ポイント
- リポジトリ権限を見直す：Bot/エージェントの書き込み権限を最小化する。必要ならPRでの自動編集を禁止。
- 監査ログを有効化：誰がいつコメント・説明を変更したかトレースできるようにする。
- 開発者ルールを明文化：CIやエージェントの振る舞いに関する社内ポリシーを作る（例：自動挿入は必ず人の承認を経る）。
- リポジトリをスキャン：不審な自動挿入コメントがないか過去のPRを検索して確認する。
- ベンダーに確認：Copilotや類似ツールの設定・権限・サポート方針を確認し、必要なら管理プランに切り替える。

開発ワークフローにAIを取り入れるなら「便利さ」と同時に「誰が何を変更できるか」を設計しておくことが必須です。
