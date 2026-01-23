---
layout: post
title: "Claude.ai silently failing since Jan 14, no official acknowledgment - Claude.ai が1月14日以降静かに障害、公式発表なし"
date: 2026-01-23T20:26:03.449Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anthropics/claude-code/issues/18866"
source_title: "[BUG] Auto-compact not triggering on Claude.ai (web &amp; desktop) despite being marked as fixed · Issue #18866 · anthropics/claude-code · GitHub"
source_id: 46736091
excerpt: "Claude.aiが1月14日以降自動圧縮停止、公式説明なしで業務リスク増大"
image: "https://opengraph.githubassets.com/0dccb7fd289524c8b9808ef2b9d71e8e1d82cd8b04ad096cfeb85d3499a40fdd/anthropics/claude-code/issues/18866"
---

# Claude.ai silently failing since Jan 14, no official acknowledgment - Claude.ai が1月14日以降静かに障害、公式発表なし
会話が続かない！Claude.aiの“自動コンパクト”機能が効かずチャットが止まる問題の全貌

## 要約
1月14日の障害以降、Claude.ai（Web/デスクトップ）で「自動コンパクト（auto-compact）」が働かず、コンテキストが溜まるとメッセージが入力欄に戻るか「limit reached」と表示される不具合が報告されている。公式の明確な説明や修正確認はまだ得られていない。

## この記事を読むべき理由
Claudeを業務や文書検索・長文コンテキストで使う日本の開発者やビジネスユーザーにとって、会話が途中で止まる問題は生産性やワークフローに直結するため、原因と対策を把握しておく必要がある。

## 詳細解説
- 自動コンパクトとは：会話の履歴（コンテキスト）がモデルのトークン上限に近づいた際、古い発言を要約・圧縮してトークン数を減らし会話を継続させる仕組み。大規模コンテキスト対応モデルで重要な機能。  
- 起きている現象：コンテキストが増えると送信したメッセージが何のエラーも出さずに入力欄へ戻る、または「limit reached」エラーが出る。報告者は200kトークン上限に到達していないケースでも発生すると指摘している。  
- 経緯：1月14日の大規模障害の後、1月15日に「修正済み」とフラグされたが、1月17日時点でも同問題が継続しているとのユーザ報告（GitHub Issue #18866）。Webとデスクトップ両方で発生、Projects機能内で特に報告が多い。  
- インパクト：長文ドキュメントや複数資料を投げるワークフロー（リサーチ、法務、顧客対応、社内ナレッジ）で会話が断絶しやすく、業務での信頼性に影響。公式アナウンスがない点も運用リスクを高める。

## 実践ポイント
- 一時的回避策：
  - 新しいチャットを作成して作業を再開する。  
  - 定期的に「要約」プロンプトを入れて自分でコンテキストを圧縮する。  
  - 大きな文書は事前に分割・要約してから投入する。  
- 監視と保全：
  - 重要な会話は適宜エクスポート・保存しておく。  
  - 問題発生時は再現手順（操作環境、モデル、スクショ）を添えて報告する。  
- 運用方針：
  - クリティカルな業務では代替のモデル/サービスを用意する。  
  - Anthropicのステータスやアップデートを定期チェックし、社内利用ポリシーを見直す。

問題はユーザー報告が増えているものの公式対応が不透明な点が最も懸念されます。業務で依存している場合は上記の対策を早めに取り入れてください。
