---
layout: post
title: "We pushed a Docker image change that took down prod for 40 minutes. The fix was a comment that nobody read. - Dockerイメージ差分で本番が40分ダウン。直したのは誰も読まなかったコメントだった"
date: 2026-02-20T10:06:08.436Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/DecispherHQ/decision-guardian"
source_title: "GitHub - DecispherHQ/decision-guardian: Prevent institutional amnesia by surfacing past architectural decisions"
source_id: 437132682
excerpt: "Docker差分で本番40分停止、PR上の設計意図自動表示で事故を防ぐ"
image: "https://opengraph.githubassets.com/0b44c4d46e5b3dec26b82dcd150c69871cb577f3476a397f09646ee0b139e3b0/DecispherHQ/decision-guardian"
---

# We pushed a Docker image change that took down prod for 40 minutes. The fix was a comment that nobody read. - Dockerイメージ差分で本番が40分ダウン。直したのは誰も読まなかったコメントだった

魅力的なタイトル: 「設計判断をコードレビューで自動表示するツールで“忘却”を防ぐ — Decision Guardianが教える現場の痛みと解決策」

## 要約
Decision Guardianは、過去のアーキテクチャ判断（ドキュメント化された「決定」）をPR上に自動で表示し、設計の意図や注意点を見落とさせないツール。重要ファイルが変更されたときに該当する意思決定をコメントしてチームの“経営記憶欠如”を防ぐ。

## この記事を読むべき理由
設計判断がドキュメント化されずに人から人へと伝承されると、離職や新規参画で同じ議論を繰り返し重大な事故を招く。日本の製品開発現場でも発生しやすい「過去判断の喪失」を技術的に補強できるため、エンジニア／リード／SREすべてに有益。

## 詳細解説
- コアアイデア：.decispher/decisions.md のような「Decisionファイル」に設計判断（ID・ステータス・重大度・該当ファイルパターン・根拠など）を記述し、Pull RequestやCIで差分と照合して該当する決定を自動で提示する。
- マッチング：glob（minimatch）や正規表現、ファイル内容・行範囲・JSONパスなど複数モードでマッチ。複雑ルールはJSONで定義可能。ReDoS対策やタイムアウト（例：regex 5s）も組み込まれている。
- パフォーマンス設計：決定索引はプレフィックストライ等で高速検索、数千ファイルのPRでも耐える設計。コメントは冪等（ハッシュで更新検出）で重複を避け、段階的トランケーションやリトライ実装あり。
- 運用形態：GitHub Action（PRトリガー）として使えるほか、ローカル/他CI向けにCLI（check / checkall）を提供。fail_on_critical 等の入力でブロッキング挙動を制御可能。
- セキュリティとプライバシー：ソースコードやパスは外部に送られず、匿名集計のみ送信。外部コールを完全に遮断したい場合は環境変数でテレメトリを無効化（DG_TELEMETRY=0）。

主要コンポーネント（概要）
- Parser：Markdown→構造化データ（remarkベース）
- Decision Index：高速ファイルルックアップ
- Matcher & Rule Evaluator：glob／contentルール評価
- Comment Manager：IDempotentなPRコメント管理

簡単なDecisionファイル例（要点）
```markdown
<!-- DECISION-DB-001 -->
## Decision: Database Choice for Billing
**Status**: Active
**Date**: 2024-03-15
**Severity**: Critical
**Files**:
- `src/db/pool.ts`
### Context
Postgresを選定した理由（ACID等）。変更前に負荷試験を必須とする旨を明記。
```

GitHub Actionの簡単な導入例
```yaml
name: Decision Guardian
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DecispherHQ/decision-guardian@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          decision_file: '.decispher/decisions.md'
          fail_on_critical: true
```

## 実践ポイント
- 最初の一歩：プロジェクトルートに .decispher/decisions.md を置き、重要な設計判断を1つずつ登録する（ID・Status・Files・Contextを必ず記載）。
- CI導入：上記のGitHub Actionを追加し、まずはfail_on_critical=falseで検出ログを確認。安定したらtrueにしてガードを強化する。
- ローカルワークフロー：npx decision-guardian check を使い、プルリク前に手元で確認する習慣を付ける（pre-commitフックへの組み込み推奨）。
- プライバシー設定：組織ポリシーで外部通信が禁止なら DG_TELEMETRY=0 を設定してテレメトリを無効化。
- 運用Tip：並列実行による重複コメントを避けるためWorkflowにconcurrencyを追加。重要な決定は必ずStatus: Activeで管理し、Deprecated/Supersededの変化を明示する。

短くまとめると、Decision Guardianは「なぜそのコードはそうあるべきか」をPRの文脈で自動提示してくれるツールで、設計判断の見落としや同じ議論の再発を防げる。まずは小さなDecisionを一つ登録してCIで動かしてみることが導入成功の近道。
