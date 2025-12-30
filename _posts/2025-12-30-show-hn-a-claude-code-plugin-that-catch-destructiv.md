---
layout: post
title: "Show HN: A Claude Code plugin that catch destructive Git and filesystem commands - Claude Code プラグイン：破壊的な Git／ファイル操作を捕捉する安全ネット"
date: 2025-12-30T04:13:22.549Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/kenryu42/claude-code-safety-net"
source_title: "Show HN: A Claude Code plugin that catch destructive Git and filesystem commands"
source_id: 46388882
excerpt: "AIの提案するrm -rfやforce-pushを構文解析で未然に防ぐプラグイン"
---

# Show HN: A Claude Code plugin that catch destructive Git and filesystem commands - Claude Code プラグイン：破壊的な Git／ファイル操作を捕捉する安全ネット

AIが"go ahead"と言ったとたんプロジェクトが吹き飛ぶ前に — Claude Code Safety Netで“rm -rf”や強制プッシュを自動で止める

## 要約
AIエージェント（Claude Code）から発行される破壊的なGit／ファイル操作をフックで解析し、危険なコマンドを実行前にブロックするプラグイン。単なる文字列マッチでは防げないケースをセマンティックに解析して止めるのが特徴。

## この記事を読むべき理由
- AI補助開発が日本でも普及する中、意図せぬデータ消失や force-push などの事故は被害が大きい。  
- 単純なdenyリストでは見逃すケース（シェルラッパー、インタプリタ一行、フラグ順序）に対応できる実装が参考になる。

## 詳細解説
- 背景：.cluade/settings.json のような prefix マッチ型の拒否ルールは、フラグの順序やラッパーで簡単に回避され得る。実際に rm -rf ~/ や git checkout -- で作業が失われた経験から「ルールのハード化」が必要になったのが発端。
- 方針：専用のフック（hook）でコマンドを受け取り、構文解析とセマンティックチェックを行う。シェルラッパーを再帰的に解析し、インタプリタ一行（python -c など）内の破壊的呼び出しも検出する。
- 代表的にブロックするコマンド（抜粋）
  - git checkout -- <files>（未コミット変更を破棄）
  - git reset --hard / --merge（未コミット変更を消失）
  - git push --force（リモート履歴の破壊）
  - rm -rf（カレント外や /, ~ 等危険パスを含む場合）
  - find … -delete, xargs rm -rf, parallel <shell> -c（動的入力で予測不能）
- 許容される例（抜粋）
  - git checkout -b new-branch（安全にブランチ作成）
  - rm -rf ./...（cwd内に限定された削除）
  - /tmp 等の一時ディレクトリへの削除
- モード
  - デフォルト：解析不能なコマンドは通す（fail-open）  
  - Strict Mode（SAFETY_NET_STRICT=1）：解析不能はブロック（fail-closed）  
  - Paranoid Mode（SAFETY_NET_PARANOID=1 等）：さらに厳しい検査（例：cwd内でも rm -rf をブロック）
- 追加機能：シェルラッパー／インタプリタ解析、秘密情報の自動赤字化（ログ等での漏洩防止）、監査ログを ~/.cc-safety-net/logs/<session_id>.jsonl に記録（タイムスタンプ、コマンド、cwd、理由）。
- 導入・検証（例）
```bash
# 例：プラグイン導入（Claude Code のマーケットプレイスから）
/plugin marketplace add kenryu42/cc-marketplace
/plugin install safety-net@cc-marketplace

# Strict モードを有効にする
export SAFETY_NET_STRICT=1
```
- テスト：同梱の pytest テスト群で各種エッジケースを検証できる。Blocked時はツール実行を止め、理由と代替案（例：git stash）を返す。

## 実践ポイント
- まずはテスト環境で導入して既存ワークフローとの誤検知を洗い出す。  
- 重要リポジトリでは Strict/Paranoid モードを有効化して fail-closed にする。  
- CI／Pre-commit フックや社内AI利用ポリシーと組み合わせ、"AIが提案した破壊的操作は手動確認必須" の運用ルールを作る。  
- 監査ログは定期的にレビューして誤検知や試行を把握、必要ならルール調整を行う。  
- 新人や非専門者がAIを使うチームでは導入効果が大きい（被害の回避、教育効果）。

## 引用元
- タイトル: Show HN: A Claude Code plugin that catch destructive Git and filesystem commands  
- URL: https://github.com/kenryu42/claude-code-safety-net
