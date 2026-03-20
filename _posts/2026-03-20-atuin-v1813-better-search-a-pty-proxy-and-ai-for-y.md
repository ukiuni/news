---
layout: post
title: "Atuin v18.13 – better search, a PTY proxy, and AI for your shell - Atuin v18.13 — 高速検索・PTYプロキシ・シェル向けAIが一挙に到来"
date: 2026-03-20T15:04:22.577Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.atuin.sh/atuin-v18-13/"
source_title: "Atuin v18.13 – better search, a PTY proxy, and AI for your shell"
source_id: 1604659499
excerpt: "v18.13で検索高速化・消えないPTY・英→bashAI搭載、即効でターミナル改善"
---

# Atuin v18.13 – better search, a PTY proxy, and AI for your shell - Atuin v18.13 — 高速検索・PTYプロキシ・シェル向けAIが一挙に到来
ターミナル体験が一段と賢く・安全に・快適になる最新アップデートまとめ

## 要約
Atuin v18.13は（1）メモリ内ホットインデックスによる高速で精度の高い検索、（2）軽量PTYプロキシ「hex」による“消えない”ポップアップ描画、（3）英語→bashを支援するAtuin AIを導入します。同期・認証改善やカスタムキーも強化。

## この記事を読むべき理由
検索速度・コマンド提案・ターミナル描画の体験が同時に改善され、生産性向上と安全性（危険なコマンドの二段確認）を両立します。日本のリモートワーク／複数マシン運用環境でも即効性のある恩恵です。

## 詳細解説
- デーモンによる高速検索  
  - 新しいdaemon-fuzzyモードは、nucleoベースのインメモリ検索インデックスでfuzzy検索の精度と速度を改善。frequency・recency・frecencyの重み（倍率）を設定可能。デーモンはautostartで自動管理でき、リモート機でもログイン直後に最新データが使えます。
  - 有効化例（config）:
```toml
# toml
search_mode = "daemon-fuzzy"

[daemon]
enabled = true
autostart = true
```
  - セットアップコマンド:
```bash
# bash
atuin setup
```

- Atuin AI（英語→bash）  
  - プロンプトで ? を押し、英語で要望を入力するとコマンド候補を出す。Enterで実行、Tabで編集、fで追加入力が可能。危険性が疑われるコマンドは二重Enterが必要で、静的チェック＋LLMガードレールで安全性を高めています。デフォルトで機械固有情報は最小限のみ取得（OSとシェル）。
  - 有効化例:
```toml
# toml
[ai]
enabled = true
```

- Hex：軽量PTYプロキシで“消えない”UI  
  - 既存のフルスクリーンや出力クリアの課題を解消。popupを以前の出力の上に重ね、閉じれば元の出力を復元する。tmuxのような副作用（scrollback破壊など）は起きません。超軽量にバイトをプロキシし、影のVT100を維持します。
  - 試すコマンド:
```bash
# bash
atuin hex          # ワンオフ
eval "$(atuin hex init)"   # シェル起動時に常用
```

- 認証とHub（ホスト型同期）  
  - Atuin HubはGoogle/GitHubログインとメール復旧をサポート。既存のself-hosted atuin-serverはそのまま動作します。Hub本体は現時点でクローズドだが将来的に公開予定。

- その他ハイライト  
  - カスタムキーバインド（検索TUI）、メモリ削減、Nushell対応改善、マルチライン/シェル互換性の強化など多数のバグ修正と機能追加。

## 実践ポイント
- まずは：atuin setup を実行してdaemonやAIを導入する。  
- すぐ試す設定：
```toml
# toml
[daemon]
enabled = true
autostart = true

[ai]
enabled = true
```
- Hexを有効にしてポップアップ挙動を確認：eval "$(atuin hex init)" をシェルに追加。  
- リモート複数マシンでコマンド履歴や検索を即時共有したい場合はデーモン＋同期を活用。  
- プライバシー重視ならHubの利用許可・アクセス設定を確認、または自己ホストを継続。  
- 新しいキー割当やTUI設定はドキュメントでカスタマイズ可能なので、自分のワークフローに合わせて調整する。

以上を試せば、日常のターミナル操作が確実に快適になります。
