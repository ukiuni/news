---
layout: post
title: "agent-shell 0.47 updates - agent-shell 0.47 アップデート"
date: 2026-03-13T01:04:20.447Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xenodium.com/agent-shell-0-47-1-updates"
source_title: "agent-shell 0.47 updates"
source_id: 1100213425
excerpt: "セッション管理強化・画像送信・使用量可視化・ワークツリー対応でEmacsのLLM業務が劇的に便利に。"
image: "https://xenodium.com/share.png"
---

# agent-shell 0.47 updates - agent-shell 0.47 アップデート
EmacsでLLMエージェントをもっと実用的にする大型アップデート — 仕事で試したくなる新機能まとめ

## 要約
agent-shell v0.47はセッション管理の改良、クリップボード画像の直接送信、インライン画像表示、使用量トラッキング、ワークツリー対応など、実務で便利な機能を多数追加しました。いくつかの設定変更は手動対応が必要です。

## この記事を読むべき理由
Emacsから複数のLLMエージェントを使う開発者・リードは、使い勝手とワークフロー改善で即効性のある恩恵を受けます。日本でもIDEサブスクリプションやトークンを企業が負担するケースが増えており、業務で使うなら導入・設定のポイントを押さえておく価値があります。

## 詳細解説
- 必要なアクション（重要）
  - Anthropicパッケージ名が変更。claude-code-acp → claude-agent-acp に更新してください：
```bash
npm remove -g @zed-industries/claude-code-acp
npm install -g @zed-industries/claude-agent-acp
```
  - カスタムコマンドを使っている場合は設定変数を更新。

- セッション周り（大きな改善）
  - agent-shell-session-strategyでセッション読み込み動作を制御可能。
    - 'new: 起動時にACPハンドシェイク・認証・セッション作成を先に行う（ブートストラップ）。
    - 'new-deferred: 従来の遅延ロード。
    - 'prompt / 'latest: セッション再開のプロンプトや自動再開。
```emacs-lisp
(setq agent-shell-session-strategy 'new)
(setq agent-shell-session-strategy 'prompt)
```
  - session/resume（軽量）と session/load（履歴再生）を使い分け。現状は resume を推奨。

- 画像・クリップボード
  - クリップボードの画像をそのまま送信可能：agent-shell-send-clipboard-image。pngpaste または xclip が必要。
  - 画像は .agent-shell/screenshots に保存され、シェル内にインライン表示。
  - サポートされる画像パス例：`![alt](/path/to.png)`、`./output/chart.png`、`~/screenshots/demo.png`

- 表・画像レンダリング、チャート連携
  - テーブルはオーバーレイで見やすく表示。チャート生成エージェントと組み合わせると視覚化が強力。

- 使用量トラッキング
  - コンテキスト使用率インジケータ（緑→黄→赤）、M-x agent-shell-show-usageでトークン／コスト確認。turn終了時にサマリ表示も可能。

- マルチエージェント・ワークフロー
  - Git worktreeごとに独立したシェルを作る agent-shell-new-worktree-shell。
  - ファイル／リージョン／画像を特定のシェルに送れる send-to 系コマンド（選択ターゲット）。

- ビューポート（viewport）中心の操作
  - 片手で高速応答できるキー割当（y=yes、1-9で選択、m=more、a=again）。推奨設定：
```emacs-lisp
(setq agent-shell-prefer-viewport-interaction t)
```

- パーミッションと自動応答
  - 権限ダイアログ改善と自動応答関数を設定可能（※常時許可は注意して使う）：
```emacs-lisp
(setq agent-shell-permission-responder-function #'agent-shell-permission-allow-always)
```

- イベント購読と拡張性
  - 初期化やファイル書き出し、ツールコール等のイベントを購読でき、他ツールとの統合が作りやすくなった：
```emacs-lisp
(agent-shell-subscribe-to :shell-buffer (current-buffer)
                          :event 'file-write
                          :on-event (lambda (event) (message "File written: %s"
                                         (alist-get :path (alist-get :data event)))))
```

- 追加エージェントと関連パッケージ
  - 追加サポート例：Auggie、GitHub Copilot、Mistral Vibe、Pi 等。モバイル連携（agent-shell-to-go）、マルチエージェント管理（meta-agent-shell）などエコシステムも拡充。

- その他
  - Composeバッファの補完強化、diffのシンタックスハイライト、Flycheck対応、モデルラインのコンテナ表示、バッファ名カスタム等、多数の品質改善。

## 実践ポイント
- まずやること
  1. claude の名前変更を適用（上の npm コマンド）。
  2. 即効で試すならブートストラップ or プロンプト再開を有効に：
```emacs-lisp
(setq agent-shell-session-strategy 'prompt)
```
  3. 画像を送りたいなら pngpaste/xclip を入れて、agent-shell-send-clipboard-image を試す。

- 日常運用での設定
  - ビューポート操作を有効にして即答ショートカットを活用。
  - トークン／コンテキストの使用状況を常に確認してコスト管理。

- 組織的な取り組み
  - 仕事で使うなら、会社に寄付やスポンサーの検討を促す（プロジェクトの持続性／機能改善に直結します）。

興味があれば、具体的な設定ファイルや導入手順（Emacs init.el の抜粋）を提供します。どこから試したいですか？
