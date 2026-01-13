---
layout: post
title: "Your CLI's completion should know what options you've already typed - CLIの補完は既に入力したオプションを“知る”べきだ"
date: 2026-01-13T05:59:23.321Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hackers.pub/@hongminhee/2026/optique-context-aware-cli-completion"
source_title: "Your CLI's completion should know what options you've already typed"
source_id: 1626609607
excerpt: "Optique 0.10で、入力済みオプションを参照する動的CLI補完が可能に"
image: "https://hackers.pub/@hongminhee/2026/optique-context-aware-cli-completion/ogimage?l=en"
---

# Your CLI's completion should know what options you've already typed - CLIの補完は既に入力したオプションを“知る”べきだ
今すぐ試したくなる！オプション同士で参照し合う「コンテキスト対応補完」がOptique 0.10でやってきた

## 要約
Optique 0.10.0は、あるオプションの値に応じて別のオプションの補完・検証ルールを動的に作れる「dependency／derive」システムを導入しました。これにより、たとえば --repo に応じて --branch の候補をリポジトリごとに出し分けられます。

## この記事を読むべき理由
CLIツールは日本でも社内ユーティリティ、デプロイツール、CI連携、クラウド操作などで頻繁に使われます。オプション間の依存関係を正しく扱えるとユーザー体験（補完・型安全・エラー検出）が格段に良くなり、生産性と信頼性が上がります。

## 詳細解説
従来の多くのCLIパーサはオプションを独立に扱うため、--branch の補完は --repo の値を知らず、全リポジトリのブランチ一覧を出すか補完を諦めるしかありません。Optiqueはこれを3フェーズ解析で解決します：

1. まず依存元のオプション値を解析して収集する  
2. 収集した値を factory に渡し、具体的なパーサ（候補リストなど）を動的生成する  
3. 生成したパーサで派生オプションを再解析・補完する

静的な組み合わせは既存の or() でも表現できますが、リポジトリやクラウドプロジェクト名のように「実行時にしか分からない値」は dependency と derive(Async)／deriveFrom(Async) が有効です。TypeScriptの型情報を維持したまま、動的候補・補完・検証が可能になります。

@example: 単一依存（リポジトリ→ブランチ）
```ts
import { dependency, option, object, string } from "@optique/core";
import { gitBranch } from "@optique/git";

const repoParser = dependency(string());
const branchParser = repoParser.deriveAsync({
  metavar: "BRANCH",
  factory: (repoPath) => gitBranch({ dir: repoPath }), // isomorphic-git を利用
  defaultValue: () => ".",
});

const parser = object({
  repo: option("--repo", repoParser),
  branch: option("--branch", branchParser),
});
```

複数依存（環境＋リージョン→サービス候補）は deriveFrom を使い、factory に依存値の順で渡されます。I/Oが必要な処理は非同期版を使いましょう。

## 実践ポイント
- まずはプレリリースを試す：deno add jsr:@optique/core@0.10.0-dev.311 または npm install @optique/core@0.10.0-dev.311
- Git連携は @optique/git を利用（isomorphic-gitベースでNode/Deno両対応）
- 補完テストは実際のシェル（bash/zsh/fish）やVS Codeの統合ターミナルでチェックする
- defaultValue を活用すれば --repo 未指定時にカレントディレクトリを想定できる（"." 等）
- 同期処理しかない場面は deriveSync、複数非同期依存は deriveFromAsync を選ぶと良い
- 社内ツール（社内リポジトリ、クラウドプロジェクト、データベース接続など）に導入するとユーザーの誤操作が減り、UXが向上します

Optiqueの依存システムは「補完まで含めたユーザー視点のCLI設計」を楽にし、型安全も保つ強力な道具です。まずは小さなコマンドで動的補完を試してみてください。
