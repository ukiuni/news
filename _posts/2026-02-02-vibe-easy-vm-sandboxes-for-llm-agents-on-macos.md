---
layout: post
title: "Vibe: Easy VM sandboxes for LLM agents on MacOS - MacでLLMエージェントを隔離する簡単VM「Vibe」"
date: 2026-02-02T06:12:32.317Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/lynaghk/vibe/"
source_title: "GitHub - lynaghk/vibe: Easy Linux virtual machine on MacOS to sandbox LLM agents."
source_id: 1646103295
excerpt: "10秒で起動する軽量VMでMac上のLLMを安全に隔離して試せる新ツール"
image: "https://opengraph.githubassets.com/84775005381c5ff061de1138b6188232d65dda829510d3d26a6f391cf304b631/lynaghk/vibe"
---

# Vibe: Easy VM sandboxes for LLM agents on MacOS - MacでLLMエージェントを隔離する簡単VM「Vibe」
MacでLLMを“安全に・素早く”試せる。10秒で立ち上がる軽量VMでエージェントをホストから分離する新しい選択肢。

## 要約
VibeはARM Mac（macOS 13以降）向けにゼロコンフィグでLinux仮想マシンを立ち上げ、LLMエージェントの実行をホストから安全に分離する小さなツールです。デフォルトでプロジェクトやパッケージキャッシュを共有し、短時間で起動します。

## この記事を読むべき理由
日本でもローカル開発中にLLMが意図せずホストファイルへアクセスしたり、外部ツールを勝手にインストールするリスクが増えています。Vibeは「手軽さ」と「仮想化による強い隔離」を両立し、実務での安全に直結する実用的な選択肢です。

## 詳細解説
- 対応環境：ARMベースのMac（macOS Ventura 13+）。初回起動時にDebianベースのディスクイメージをダウンロードして ~/.cache/vibe/ に格納。以降はプロジェクトごとに .vibe/instance.raw をコピーして起動。
- セキュリティ方針：コンテナより仮想化（VM）を採用。Mac上のコンテナは実質VMを使うことが多く、仮想化のほうが脱出リスクが低いという判断。
- パフォーマンスと設計：M1で約10秒のブートが報告されており、Appleのファイルシステムのコピーオンライトを利用してディスク消費を抑える設計。
- 共有とデフォルト動作：起動時にカレントディレクトリやパッケージキャッシュ、OpenAI/Anthropic用のユーザディレクトリ（~/.codex, ~/.claude など）をゲストにマウントするのがデフォルト。必要に応じて --no-default-mounts や --mount で制御可能。
- 主なCLI機能：CPUコア数／RAM指定、スクリプト実行、コンソール出力を待ってから次アクションを実行する --expect／--send、既存ディスクイメージを指定して起動など。
- 実装と配布：Rustで単一バイナリ（小容量）として配布。事前ビルドバイナリを配置するか、cargo経由でインストール可能。macOSの仮想化エンタイトルメントに合わせて自己署名チェックを行う仕組みあり。
- なぜ既存ツールでなくVibeか：LimaやVagrant等は設定の複雑さや起動遅延、マウント制約など実用上の不満があり、Vibeは「速く・明示的に・必要最小限で動く」ことを優先している。

## 実践ポイント
- まず試す：プロジェクトディレクトリで単に vibe を実行して、VM内でLLMエージェントを動かしてみる（初回はイメージDLが必要）。
- 自動化：起動時に --script と --expect／--send を組み合わせてテストやセットアップを非対話で実行できる。
- マウント管理：機密ファイル（APIキー等）を渡したくない場合は --no-default-mounts を使い、必要なディレクトリだけ明示的に --mount する。
- バージョン管理：公式リリースを追わずコミットで運用されているため、安定運用ならコミットSHAで固定するかローカルでバイナリを管理する。
- トラブル対処：ディスク使用量はコピーオンライトのため実ファイルサイズと du の値を確認。既に起動中のVMへ接続しようとするケースは注意（今後の改善項目）。

参考の簡単な実行例：
```bash
# プロジェクトで起動（初回はイメージをDL）
vibe
# カスタムマウント＋2CPU/4GBメモリで起動
vibe --cpus 2 --ram 4096 --mount /path/on/host:/mnt/guest:read-write
```

短く言えば、ローカルでLLMを「手軽に安全に」試したい日本の開発者にとって、Vibeは実用的で導入コストが低い選択肢です。興味があるならリポジトリをチェックして、まずローカルで一回立ち上げてみることを勧めます。
