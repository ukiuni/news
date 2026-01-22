---
layout: post
title: "It looks like the status/need-triage label was removed - status/need-triage ラベルが削除されたようです"
date: 2026-01-22T17:18:23.826Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/google-gemini/gemini-cli/issues/16728"
source_title: "jetbrains ide detection · Issue #16728 · google-gemini/gemini-cli · GitHub"
source_id: 46721179
excerpt: "Gemini CLIがJetBrainsを検出できず偽装が必要、検出優先改善を提案"
image: "https://opengraph.githubassets.com/2e6c8e14883fed002549e41fd312e9a300ef55d1d6c559d87d5988d5a406624e/google-gemini/gemini-cli/issues/16728"
---

# It looks like the status/need-triage label was removed - status/need-triage ラベルが削除されたようです
JetBrains系IDEを「正しく」検出してほしい——Gemini CLIのIDE検出に関する地味に重要な提案

## 要約
Gemini CLIが現在TERM_PROGRAMなどのハードコードされた環境変数でVS Codeのみを「公式対応」と見なしており、JetBrains系IDE（IntelliJ/PyCharmなど）をネイティブに検出できないため、環境変数の偽装を強いる問題が報告されています。提案はIDE定義にJetBrainsシリーズを追加し、`TERMINAL_EMULATOR=JetBrains-JediTerm` を優先検出する変更です。

## この記事を読むべき理由
日本でもJetBrains製IDEは広く使われており、IDE連携がスムーズでないと開発フローや拡張ツール（プラグイン／CLI連携）に支障が出ます。GeminiのようなCLIツールが正しくIDEを判別できることは、開発者体験（DX）向上に直結します。

## 詳細解説
- 現状の問題点  
  - Gemini CLIはIDE連携の有無を環境変数（例：`TERM_PROGRAM=vscode`）で判定しており、JetBrains系は検出対象に入っていない。  
  - 結果、JetBrains向けのサードパーティ統合（jetbrains-ide-companion等）はVS Codeの環境変数を偽装して機能させる必要がある。  
  - さらにWindows/Linux環境でのプロセス検出が不安定で、ポート情報ファイルではなく環境変数ベースの検出が重要になっている、というユーザー報告がある。  
- 提案内容（技術的ポイント）  
  - IDE_DEFINITIONSにJetBrainsシリーズを追加。  
  - 検出優先度に`TERMINAL_EMULATOR=JetBrains-JediTerm`を加え、JetBrainsの端末を第一級でサポート。  
  - これにより「環境変数を正しく読む」→「偽装不要」→「プラグインの互換性向上」が期待される。  
- 関連課題・経緯  
  - 既往のIssue（例: #16083 やプラグインレビューレポート）に触発された改善提案で、triageラベル付けの変遷があった模様。

コード例（検出ロジックのイメージ）:
```bash
# bash
if [ "$TERMINAL_EMULATOR" = "JetBrains-JediTerm" ]; then
  IDE="jetbrains"
elif [ "$TERM_PROGRAM" = "vscode" ]; then
  IDE="vscode"
fi
```

## 実践ポイント
- JetBrainsユーザー：当面の回避策は、プラグイン側で環境変数を設定するか、Gemini CLIの更新を待つこと。偽装は一時対処であり根本解決ではない。  
- 開発者／メンテナー：IDE_DEFINITIONSにJetBrains系を追加し、`TERMINAL_EMULATOR`を含めた検出ロジックの順序を見直すパッチを提案・テストすると良い。Windows/Linuxでの動作確認を忘れずに。  
- テスター：自分の環境で`echo $TERMINAL_EMULATOR`や`echo $TERM_PROGRAM`を確認し、変更後のGemini CLIが期待通りにIDEを識別するか検証する。

この記事のポイントは「偽装ではなく正しい検出を実装して、JetBrainsユーザーの開発体験を改善する」ことです。
