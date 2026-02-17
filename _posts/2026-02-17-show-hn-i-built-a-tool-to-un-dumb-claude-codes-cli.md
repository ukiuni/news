---
layout: post
title: "Show HN: I built a tool to un-dumb Claude Code's CLI output (Local Log Viewer) - Claude CodeのCLI出力を賢く復元するローカルログビューア"
date: 2026-02-17T09:03:01.040Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/matt1398/claude-devtools"
source_title: "GitHub - matt1398/claude-devtools"
source_id: 47004712
excerpt: "Claude CodeのCLI出力を復元し、ツール呼び出しやトークン消費を詳細可視化する無償ローカルツール"
image: "https://opengraph.githubassets.com/bcecda5d897682134c2760e36380ea7887e8102146c55db5b9842e2699c8fffe/matt1398/claude-devtools"
---

# Show HN: I built a tool to un-dumb Claude Code's CLI output (Local Log Viewer) - Claude CodeのCLI出力を賢く復元するローカルログビューア

ターミナルの“黒箱”を可視化する神器：Claude Codeが隠した詳細をそのまま再現するローカルログビューア

## 要約
claude-devtoolsはローカルに残るClaude Codeのセッションログ（~/.claude/）を読み取り、ファイルパス、ツール呼び出し、トークン消費などを再構築して可視化する無料のオープンソースデスクトップ／スタンドアロンツールです。APIキー不要・設定不要で端末実行分もIDE経由も一元的に解析できます。

## この記事を読むべき理由
- Claude Codeの最近のアップデートで詳細出力が簡素化され、デバッグや監査が難しくなった問題に直接対処するため。  
- 日本の開発現場でも、ローカルでの可視化・秘匿情報監視・チーム協調の追跡に有用で、企業ポリシーやセキュリティ要件と相性が良いから。

## 詳細解説
- ログソース：既存のセッションログディレクトリ（デフォルト ~/.claude/）をそのまま読み取り、セッションごとの実行トレースを再構築する。ツール自体はClaude Codeをラップ／改変せず「見るだけ」なので動作を変えない。  
- コンテキスト復元：各ターンごとにトークン使用を7カテゴリに内訳化（CLAUDE.md、スキル、@-参照ファイル、ツール入出力、extended thinking、チーム・オーバーヘッド、ユーザーテキスト）し、コンパクション（文脈圧縮）イベントを可視化する。  
- ツールコール表示：Read（ファイル表示）、Edit（差分表示）、Bash（コマンド出力）、Subagent（子エージェント実行ツリー）をネイティブにレンダリング。差分や行番号付きで確認可能。  
- チーム／サブエージェント追跡：Task/Team系のツール呼び出しを展開し、エージェントごとの実行ツリー・トークン・期間・コストを表示。Teammateメッセージは色分けされて見やすい。  
- 通知＆トリガー：正規表現ベースのルールで .env や課金関連ファイルアクセス、エラー、高トークン使用などを通知。フィルタや無視パターンでノイズ制御可能。  
- リモート対応：~/.ssh/config を読み取りSSH経由で遠隔ホストの ~/.claude/ をSFTPでストリーミング解析。Electron版はネイティブFSウォッチ、スタンドアロン（Docker/Node）版はSSEで更新を配信。  
- 配布形態：macOS/.dmg、Linux(.AppImage/.deb/.rpm/.pacman)、Windows.exe、Dockerイメージ、Node.jsスタンドアロン。MITライセンス。設定不要で即起動できる点が特徴。

## 実践ポイント
- まずはDockerで試す（CLAUDEディレクトリをread-onlyでマウントする例）:
```bash
bash
docker run -p 3456:3456 -v ~/.claude:/data/.claude:ro matt1398/claude-devtools
# ブラウザで http://localhost:3456 を開く
```
- ローカル.appや.exeを使えばネイティブFSウォッチで即時更新を確認可能。  
- カスタムログパスを使う場合は環境変数CLAUDE_ROOTを指定して起動。  
- まずはデフォルトの通知トリガー（.envアクセス、ツールエラー、高トークン使用）を有効にして、どこが問題を起こしているか可視化する。  
- チームで使う場合は、サブエージェント／Teamイベントの可視化で担当分担や無駄なトークン消費が分かるため、プロンプト設計やワークフロー改善に直結する。
