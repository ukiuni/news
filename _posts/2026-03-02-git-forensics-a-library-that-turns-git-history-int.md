---
layout: post
title: "git-forensics - a library that turns git history into actionable architectural signals for your dev tooling - git履歴を開発ツール向けのアーキテクチャシグナルに変えるライブラリ"
date: 2026-03-02T12:16:36.255Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/itaymendel/git-forensics"
source_title: "GitHub - itaymendel/git-forensics: A TypeScript library for providing insights from git commit history."
source_id: 392821912
excerpt: "git履歴からホットスポットや共変化を抽出し、PRで修正優先を提示する"
image: "https://opengraph.githubassets.com/12c58d719d7e57893f82ebf592de9ae57f8050b2034ec7d03311b5376faceb7e/itaymendel/git-forensics"
---

# git-forensics - a library that turns git history into actionable architectural signals for your dev tooling - git履歴を開発ツール向けのアーキテクチャシグナルに変えるライブラリ
「履歴を味方にする」Gitログで設計の弱点を自動検出するgit‑forensics

## 要約
git‑forensicsはTypeScript製のライブラリで、コミット履歴を解析して「ホットスポット」「コードの老朽化」「隠れた依存（共変化）」など、アーキテクチャ上の警告を自動生成します。CI統合やPRコメント生成に向く軽量設計が特徴です。

## この記事を読むべき理由
日本の製品チームや大規模リポジトリ運用者は、コードレビューやリファクタの優先順位付けに悩みます。本ツールは履歴から「どこを直すべきか」をデータで示し、CIに組み込んで継続的に監視できます。

## 詳細解説
- 基本機能：コミット履歴からファイルごとのリビジョン数、追加/削除（churn）、共変化（coupling）、コード年齢、所有権分散などを算出。リネーム追跡にも対応。
- 性能：設計上は高速（著者報告で約700ms／100kコミット。ただしgit-log取得は別途時間がかかる）。大規模リポジトリでは「最近6〜9ヶ月」に注目するのが推奨。
- インサイト生成：生の統計から人間向けのアラート（info/warning/critical）を作成するgenerateInsightsを提供。例えば
  - hotspots: ≥25リビジョン → 頻繁に変わるファイル
  - churn: ≥1000行 churned → 書き直しが多い箇所
  - coupledPairs: ≥70% 共変化率 → 隠れた依存
 などのしきい値で警告を出します。
- 拡張性：言語別の静的複雑度スコアを外部で算出し渡せる。computeForensicsFromDataでgitアクセスなしの環境（ミラー／データAPI）にも対応。
- CIワークフロー：全履歴を事前集計して保存 → PR時は変更ファイルだけで高速にインサイト生成、PRコメントやCI注釈を自動作成する運用が想定されています。
- 出典／思想：Adam Tornhillの「Your Code as a Crime Scene」等の考えを踏襲。

Quick Start（最小例）:
```javascript
import { simpleGit } from 'simple-git';
import { computeForensics } from 'git-forensics';

const git = simpleGit('/path/to/repo');
const forensics = await computeForensics(git);
console.log(forensics.hotspots);
```

CIでPR用インサイトを出す流れ（事前集計を利用）:
```javascript
import { simpleGit } from 'simple-git';
import { generateInsights, getChangedFiles } from 'git-forensics';

const git = simpleGit();
const forensics = await fetch('/api/forensics?repo=org/repo').then(r=>r.json());
const changed = await getChangedFiles(git, 'origin/main');
const insights = generateInsights(forensics, { files: changed, minSeverity: 'warning' });
```

## 実践ポイント
- まずは「直近6〜9ヶ月」の履歴で試す。長年履歴はノイズ化することがある。
- CIに組み込むなら「事前集計を定期実行」→ PR時は差分だけで評価するとコスト削減に有効。
- チーム独自の閾値（リビジョン数、churn等）を現場データでチューニングする。
- 言語固有の複雑度スコアを用意してcomputeForensicsに渡すと精度が上がる。
- リポジトリの所有権やナレッジ分散の検出は、オンボーディングやリファクタ優先順位付けにそのまま使える。

元リポジトリ（コード・詳細）: https://github.com/itaymendel/git-forensics
