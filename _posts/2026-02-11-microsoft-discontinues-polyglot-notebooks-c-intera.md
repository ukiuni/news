---
layout: post
title: "Microsoft Discontinues Polyglot Notebooks (C# Interactive) - Polyglot Notebooks 廃止のお知らせ"
date: 2026-02-11T20:59:02.248Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/dotnet/interactive/issues/4163"
source_title: "📢 DEPRECATION ANNOUNCEMENT: Polyglot Notebooks · Issue #4163 · dotnet/interactive · GitHub"
source_id: 445294946
excerpt: "MicrosoftがC#版Polyglotを廃止、移行手順と運用対策を今すぐ確認すべき理由とは"
image: "https://opengraph.githubassets.com/f04573731bc326bf6b7b1c552facd979f7336758fc3ecbe9c5a345484faf0629/dotnet/interactive/issues/4163"
---

# Microsoft Discontinues Polyglot Notebooks (C# Interactive) - Polyglot Notebooks 廃止のお知らせ
C#ノートブック終了の衝撃 — 今すぐ移行を始めるべき理由と実務対応ガイド

## 要約
Microsoft（dotnet/interactive）がPolyglot Notebooks拡張を2026年3月27日付で廃止すると発表。拡張自体はVS Codeに残るが、新機能は追加されず、バグ対応・サポートは即時終了。C#ユーザーは「file-based apps」へ、他言語ユーザーはVS CodeのJupyter拡張への移行が推奨されている。

## この記事を読むべき理由
Polyglot NotebooksはC#や複数言語での対話的なプロトタイピングや学習に使われてきたため、社内ツールや教育コンテンツに影響が出る可能性が高い。早めに代替手段を決めて移行計画を立てる必要があります。

## 詳細解説
- 廃止の内容：拡張はアンインストールされないが「deprecated」扱い。新機能追加なし、バグ修正／サポートは即時終了。関連Issueは「not planned」でクローズされる。
- 推奨アクション：
  - C#中心のユーザー：Microsoftが推奨する「file-based apps」を利用。単一の .cs ファイルからビルド／実行／公開でき、ノートブックと同様に短いサイクルで試行錯誤できる点が狙い。C# Dev Kitや今後のAI機能と連携して開発体験を継続する方針。
  - 他言語ユーザー：VS CodeのJupyter拡張へ移行。広い言語サポートとノートブック機能を備えるため、既存ワークフローの大部分を置き換えられる。
- 運用上の懸念：拡張に依存した自動化・拡張ポイント（CI、教材、社内テンプレート）がそのままでは動作しなくなる可能性。早期の検証と移行テストが必要。

## 実践ポイント
- 所有ノートブックを棚卸し：用途（学習／実験／プロダクション）で優先順位付け。
- C#ノートはまず「file-based apps」で試す：短いサンプルを一つ移行して動作確認。
- 他言語ノートはVS Code Jupyterへ移行テスト：依存ライブラリや拡張機能の互換性を確認。
- 重要データはバックアップ（nbformatやソースとして保存）。
- 期限を設定：2026-03-27前に主要リポジトリの移行完了を目標に。不要なら拡張をアンインストール。

早めに手を動かせば影響は最小化できます。
