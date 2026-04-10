---
layout: post
title: "I Still Prefer MCP over Skills - 私は今もSkillsよりMCPを選ぶ"
date: 2026-04-10T02:41:58.808Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://david.coffee/i-still-prefer-mcp-over-skills/"
source_title: "I Still Prefer MCP Over Skills | David Mohl"
source_id: 47712718
excerpt: "CLI依存を脱却し認証・更新を一元化するMCP優先の実運用設計"
image: "https://david.coffee/i-still-prefer-mcp-over-skills/banner.png"
---

# I Still Prefer MCP over Skills - 私は今もSkillsよりMCPを選ぶ
CLI地獄からの脱出：MCPが示す「LLMとサービス統合」の正解

## 要約
著者は「Skills」は知識伝達には有効でも、サービスへの実際のアクセスにはModel Context Protocol（MCP）が圧倒的に実用的だと主張する。接続は“コネクタ（MCP）”、説明は“マニュアル（Skill）”で分けるべき、という結論。

## この記事を読むべき理由
日本のプロダクトや企業もAI統合を進めており、認証や運用、セキュリティが強く問われる環境では「CLIを前提にしたSkillsだけ」のアプローチは限界がある。実運用で役立つ設計指針が学べます。

## 詳細解説
- MCPとは何か  
  MCPは「LLMが呼び出すためのAPI抽象層」。LLMは内部実装を気にせず、定義されたメソッド（例：devonthink.do_x()）を叩くだけでサービス操作できる。実行ロジックや認証はMCPサーバ側で完結する。

- MCPの利点（要点）  
  - ゼロインストール：リモートMCPならクライアント側のセットアップ不要。  
  - 自動更新：サーバ側更新で全クライアントが最新を利用可能。  
  - 安全な認証：OAuth等でシークレット管理がサーバ側に集約される。  
  - ポータビリティ＆サンドボックス：スマホやウェブから同じ挙動、実行権限は制限される。  
  - 必要時のみロードするツール探索とコンテキスト節約。

- Skillsの役割と問題点  
  - 向いている場面：内部用語や書式、ワークフローの「知識を教える」目的。README的なマニュアルとして有用。  
  - 問題点：多くのSkillsはCLI依存を前提とし、ChatGPTや標準ウェブ版ClaudeなどCLI実行ができないクライアントでは機能しない。配布・更新・シークレット管理・フォーマット互換性などの運用コストが高い。さらにSKILL.md全体をコンテキストに読み込ませることでトークンが無駄になる（コンテキスト肥大化）。

- いつMCPを使うべきか、いつSkillか  
  - MCPを推奨：サービスやアプリをLLMから直接制御したいとき（カレンダー操作、ブラウザの状態制御、プロジェクト操作など）。  
  - Skillを推奨：ツールの使い方・社内ルール・テキスト表現など「知識」や「慣習」をLLMに教えるとき。  
  - 最適解：MCP（実行コネクタ）＋Skill（利用マニュアル）の併用。SkillはMCPの「チートシート」として振る舞う。

- 実例と運用パターン  
  NotionやGoogle CalendarはリモートMCPを持つべきで、ユーザーはOAuthで権限付与するだけでどのLLMクライアントからも操作可能になる。ローカル限定のツールはMCPをクラウド越しにトンネルする（著者のMCP Nestのような仕組み）ことで運用性が向上する。

## 実践ポイント
- 新サービス設計時は「まずMCPでの公開」を検討する（API＋認証をMCP仕様にする）。  
- Skillsはドキュメント／運用ノウハウをLLMに伝える目的で作る（CLIsを前提にしない）。  
- CLI依存のSkillは可能ならMCPに置き換えるか、MCP呼び出し用の軽いラッパーを用意する。  
- 認証はOAuth等の標準方式で集中管理し、クライアントに生トークンを渡さない。  
- 日本の現場では、LINEや国内SaaS、社内業務系ツールにMCP的設計を採り入れると現場運用とセキュリティが楽になる。

（要点）接続は「コネクタ（MCP）」で、説明は「マニュアル（Skill）」で。両者を分けて組み合わせるのが現実的かつ拡張性のあるアプローチです。
