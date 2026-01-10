---
layout: post
title: "I got tired of “TODO: remove later” turning into permanent production code, so I built this - 「TODO:later」が放置されるのを止めるために作ったツール"
date: 2026-01-10T15:27:27.396Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/jobin-404/debtbomb"
source_title: "GitHub - jobin-404/debtbomb: DebtBomb lets teams ship temporary hacks safely by attaching an expiry date to them. When the date passes, the bomb explodes and your CI fails — forcing the code to be cleaned up instead of rotting forever."
source_id: 467507582
excerpt: "期限付きTODOでCIを失敗させて技術負債を強制掃除するDebtBomb"
image: "https://opengraph.githubassets.com/8807a102eec2d7b84b0f26e90cee1f65d17707df18c705cdf4ce6b0161903764/jobin-404/debtbomb"
---

# I got tired of “TODO: remove later” turning into permanent production code, so I built this - 「TODO:later」が放置されるのを止めるために作ったツール
期限つきTODOで「腐ったコード」を撃退する――期限を過ぎたらCIを失敗させるDebtBombの使いどころ

## 要約
DebtBombはソースコメントに期限付きの「デットボム（@debtbomb）」を埋め、期限が過ぎるとCIを失敗させて強制的に掃除させるツール。臨時対応を安全に運用し、技術的負債の放置を防ぐ。

## この記事を読むべき理由
日本の多くの開発現場では「とりあえず直す」「TODO: remove later」が永遠に残る問題がある。小規模チームや運用重視のプロダクトでも、期限を明確にして自動で期限切れを検出すれば、負債管理が現実的になる。

## 詳細解説
- 何をするか：ソースコードのコメントに `@debtbomb` を付けて期限（expire）を指定。DebtBombはリポジトリをスキャンし、期限切れのデッドボムを検出すると終了コードを返してCIを失敗させる。
- インストール（Go環境があれば簡単）:
```bash
# bash
go install github.com/jobin-404/debtbomb/cmd/debtbomb@latest
```
- 使い方の基本:
  - CIで失敗させる: `debtbomb check`
  - 期限切れが近いものだけ警告にする: `debtbomb check --warn-in-days 7`
  - 一覧表示: `debtbomb list`（`--expired` や `--json` で絞り込み/出力形式変更）
- コメントの書き方（例）:
```go
// @debtbomb(expire=2026-02-10, owner=pricing, ticket=JIRA-123)
```
または読みやすいブロック形式も可:
```go
// @debtbomb
// expire: 2026-02-10
// owner: pricing
// ticket: JIRA-123
// reason: Temporary surge override
```
- 必須/任意フィールド：
  - expire（必須、YYYY-MM-DD）
  - owner（任意、担当チーム/個人）
  - ticket（任意、トラッカー参照）
  - reason（任意、背景）
- 除外設定：
  - プロジェクトルートに `.debtbombignore` を置き、.gitignore と同様の書式で除外可能。
  - デフォルトで node_modules、.venv、ビルド成果物、.git、.vscode 等や大きなバイナリは自動除外されるため大規模リポジトリでも高速。
- CI統合の狙い：期限を越えてマージされることを防ぎ、期限が来たら対応（チケット作成／リファクタ／期限延長の適切なレビュー）を強制する。

## 実践ポイント
- 今すぐ試す:
  1. ローカルで `go install` して `debtbomb check` を実行してみる。
  2. 代表的な臨時対応箇所に `@debtbomb` を付け、短い期限（例：2週間）を設定して挙動を確認する。
- 運用ルールの提案:
  - TODOに必ず owner と ticket を書く（誰が、いつまでに対応するか明確化）。
  - 期限延長はPRで必須レビュー対象にする（理由の明記を必須に）。
  - CIではデフォルトは警告モードで導入し、段階的に失敗モードへ移行する。
- 日本の現場での応用例:
  - レガシー改修が多いプロダクトで「応急対応だけど放置されがち」な箇所に効果的。
  - コンプライアンスや監査が厳しい業界では、期限管理のエビデンスとして使える。
- VS Codeでの導入ヒント:
  - 開発中は pre-commit やワークスペースタスクに `debtbomb check --warn-in-days N` を組み込み、PR作成前に警告を出す運用が現実的。

短期間で技術的負債の見える化と自動化ができるシンプルな仕組み。まずは短めの期限を入れ、チームの運用ルールと合わせて徐々に厳しくしていくのが成功のコツ。
