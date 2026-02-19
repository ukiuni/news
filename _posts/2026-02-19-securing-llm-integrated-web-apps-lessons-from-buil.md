---
layout: post
title: "Securing LLM-Integrated Web Apps: Lessons from Building an AI Tool - LLM統合ウェブアプリの防御術"
date: 2026-02-19T04:51:08.754Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@jabrsalm449/securing-ai-powered-applications-a-comprehensive-guide-to-protecting-your-llm-integrated-web-app-dcf8d7963e78"
source_title: "Securing LLM-Integrated Web Apps: Lessons from Building an AI Tool"
source_id: 438075245
excerpt: "サーバ側モデル検証・レート制御・HTTP-onlyで金と機密を守る。"
---

# Securing LLM-Integrated Web Apps: Lessons from Building an AI Tool - LLM統合ウェブアプリの防御術
AI搭載アプリで“金とデータを守る”実践セキュリティガイド

## 要約
LLM（大規模言語モデル）を組み込むと従来のWebアプリにはなかった脅威（費用搾取、プロンプト注入、パラメータ改竄など）が発生する。本記事はPromptimizerの実装で学んだ多層防御の要点を解説する。

## この記事を読むべき理由
日本のスタートアップや既存サービスがAI機能を追加する際、無策だと運用コスト爆発や機密漏洩のリスクが高まる。本記事は即実装できる防御策を端的に示す。

## 詳細解説
- なぜ従来のセキュリティで足りないか  
  LLMは「APIコール＝コスト」「プロンプトが振る舞いを左右する」という性質があり、リクエスト量・入力内容・出力長で被害が直結する。

- セキュリティユーティリティの集中化  
  全てのレート制御・ブロック管理・検知ロジックを1モジュールにまとめ、監査と保守性を確保する。

- レートリミット（エンドポイント別）  
  チャット等コスト高のエンドポイントは厳しく、認証は段階的ブロッキング。実運用ではX-Forwarded-For考慮、分散環境はRedis等で状態共有を推奨。
  
  ```javascript
  // javascript
  export const RATE_LIMIT_CONFIG = {
    chat: { windowMs: 60*1000, maxRequests: 10 },
    auth: { windowMs: 15*60*1000, maxAttempts: 5, blockDurationMs: 30*60*1000 },
  };
  ```

- プロンプト注入対策（検知は第一層）  
  パターンマッチで典型的な"ignore previous instructions"や"reveal system prompt"などを検出する。高度な攻撃は回避できるとは限らないため、出力制約・ログ監査と組み合わせる。

  ```javascript
  // javascript
  const SUSPICIOUS_PATTERNS = [/ignore\s+previous/i, /reveal\s+(your|the)\s+prompt/i, /jailbreak/i];
  ```

- モデル/パラメータ検証（必須）  
  クライアントから任意のmax_tokensやモデル指定を受けない。ホワイトリスト化とサーバ側での最大トークン強制がポイント。  
  トークン上限はモデルごとに定義し、サーバでclampする。

- APIルートの流れ（原則）  
  1) クライアントIPでレートチェック → 2) カウンタ増加 → 3) ボディサイズ検査 → 4) モデル・メッセージ・オプション検証 → 5) 検証済みでAPI呼び出し → 6) 汎用エラーメッセージと内部ログ

- サーバ側認証とセッション管理  
  パスワードやトークンをクライアントに置かない。HTTP-onlyクッキー＋サーバ側セッション（本番はRedis等）でXSSや認証回避を防ぐ。失敗試行はカウントしてIPブロック。

- セキュリティヘッダとCSP  
  X-Frame-Options, X-Content-Type-Options, CSP等でXSS・クリックジャッキングなどの二次被害を抑える。

- エラーハンドリング  
  内部情報をクライアントに返さない。ログは詳細に、ユーザー向けは汎用メッセージにする。

## 実践ポイント
- サーバ側で必ずモデルとtoken上限を検証・強制する。  
- エンドポイント別にレート制限を設け、チャット系は特に厳しく。Redis等で分散同期。  
- プロンプト注入はシグネチャ＋ログ＋出力検査の多層防御で。完全防御は困難と割り切る。  
- 認証はHTTP-onlyクッキー＋サーバセッション、認証失敗は段階的にIPブロック。  
- リクエストサイズ制限、セキュリティヘッダ、汎用エラーメッセージを必ず実装する。  
- 日本市場向け：個人情報や機密データは国内法・契約要件を満たすモデルやオンプレ/専用VPC経由で扱う（データ駆動サービスは特に要注意）。

以上を踏まえ、まずは「サーバ側のモデル検証」「エンドポイントごとのレート制御」「HTTP-onlyセッション」を最初の3点として導入することを推奨する。
