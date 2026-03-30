---
layout: post
title: "Claude Code runs Git reset –hard origin/main against project repo every 10 mins - Claude Codeが10分ごとにプロジェクトをgit reset --hard origin/mainで上書きする"
date: 2026-03-30T00:31:35.906Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/claude-code/issues/40710"
source_title: "Claude Code runs git reset --hard origin/main against project repo every 10 minutes · Issue #40710 · anthropics/claude-code · GitHub"
source_id: 47567969
excerpt: "Claudeが10分ごとにgit reset --hardで未コミットを消す深刻バグと対処法"
image: "https://opengraph.githubassets.com/bdc44c0ea39f0bdf4bf7f3e1651bac704d6362dd9ebfcde8ec3a34bee24a0266/anthropics/claude-code/issues/40710"
---

# Claude Code runs Git reset –hard origin/main against project repo every 10 mins - Claude Codeが10分ごとにプロジェクトをgit reset --hard origin/mainで上書きする
あなたの未コミットコードが10分ごとに消える？Claude Codeの致命的リセットバグ

## 要約
Claude Code（v2.1.87）がプロセスの作業ディレクトリに対して、プログラム内部で10分ごとにgit fetch + git reset --hard origin/mainを実行し、追跡された未コミット変更を上書きしていると報告されています。作業ツリー（worktree）は無事、未追跡ファイルも残りますが、被害は深刻です。

## この記事を読むべき理由
日本でもmacOS＋ローカルリポジトリで開発するエンジニアが多く、AI支援ツールを導入している現場では未コミットの変更が意図せず失われるリスクがあります。原因の特定と即効性のある回避策を知っておくべきです。

## 詳細解説
- 挙動の要点：プロセス内で外部gitコマンドを呼ばず（libgit2などのプログラム的操作の可能性）、600秒間隔でoriginからフェッチしてmainに強制リセットしている。  
- 証拠：git reflogに10分間隔で同一コミットへ「reset: moving to origin/main」が連続記録。fswatchで.git内のロックファイル生成が確認され、リセット時に外部gitプロセスは観測されず、影響がある作業ディレクトリのCWDがClaude Codeプロセスのみ。  
- 影響範囲：追跡ファイルの未コミット変更が消失（上書き）。コミット済み変更は影響なし。ワークツリーは免疫。問題はセッション開始オフセットが変わるため「間欠的」に見える。  
- 探索で除外された要因：エディタ／フック／クラウド同期／Cron類／プラグイン等ほぼ全て排除済み。バイナリ解析でfetch処理を指す関数が確認されているが、正確なタイマー箇所は難読化で不明。

## 実践ポイント
すぐできる対策と確認コマンド（macOS/Linux想定）：

- reflogでリセット履歴を確認
```bash
git reflog --date=iso | grep 'reset: moving to origin/main' -n
```

- 直近のリセットタイミングを確認（時刻差で10分間隔が出るか）
```bash
git reflog --date=iso | head -n 50
```

- 実行プロセス確認（Claude系プロセスを探す）
```bash
ps aux | grep -i claude
# 見つかったPIDで開いているディレクトリを確認
lsof -p <PID> | grep cwd
```

- 即効の回避策
  - git worktreeを使って別ワークツリーで作業する（報告ではworktreeは免疫）
```bash
git worktree add ../my-worktree main
cd ../my-worktree
```
  - こまめにコミット・ローカルブランチにpush/バックアップを取る
  - Claude Codeのプロセスを停止するか、アップデート・公式の修正が出るまで使用を控える

- 運用上の注意
  - CIやチーム開発のローカル作業ポリシーに「未コミットの保護」を明文化する（作業前のコミット/一時ブランチ作成等）。  
  - 特に企業やスタートアップではローカルの自動操作を許可するツール導入時に事前リスク評価を行う。

元のGitHub Issueは調査済みの再現手順と詳細ログを含んでおり、同様の被害を受けた場合はIssueを追跡してアップデートとパッチを待つことを強く推奨します。
