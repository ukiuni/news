---
layout: post
title: "Show HN: Minimal NIST/OWASP-compliant auth implementation for Cloudflare Workers - Cloudflare Workers向けのNIST/OWASP準拠ミニマル認証実装"
date: 2026-02-09T13:11:55.266Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vhscom/private-landing"
source_title: "GitHub - vhscom/private-landing: 🔐 Learn authentication by building it right. A standards-compliant reference implementation for Cloudflare Workers with Hono, Turso, PBKDF2, and JWT dual-token sessions."
source_id: 46944084
excerpt: "Cloudflare Workers向けNIST/OWASP準拠認証—PBKDF2とデュアルJWTで学べるリファレンス"
image: "https://opengraph.githubassets.com/b1759a5261515f2743deacd802aa41777bdf10ccf4ec9b69ffdc225134884ee7/vhscom/private-landing"
---

# Show HN: Minimal NIST/OWASP-compliant auth implementation for Cloudflare Workers - Cloudflare Workers向けのNIST/OWASP準拠ミニマル認証実装
エッジで学ぶ安全な認証：Cloudflare Workersで作るNIST/OWASP準拠リファレンス

## 要約
Cloudflare Workers上で動く、教育目的の認証リファレンス実装。PBKDF2によるパスワード保存、JWTのデュアルトークン（短期アクセストークン＋長期リフレッシュ）、セッション管理や多数の攻撃ベクトルを検証するテスト群を備えます。

## この記事を読むべき理由
国内でもサーバーレス／エッジで認証を扱う機会が増えています。安全な設計原則（NIST、OWASP、RFC）に基づいた実装を“学びながら”確認できるため、設計の理解やレビュー力向上に直結します。

## 詳細解説
- プラットフォーム：Cloudflare Workers（Web Crypto API利用、Node依存なし）＋Honoルーティング、エッジDBとしてTursoを使用する構成。  
- パスワード保存：PBKDF2-SHA384、128ビットソルト、整合性ダイジェスト、バージョン管理を実装。NIST SP 800-132に準拠する設計思想。  
- セッション管理：サーバーサイドでのセッション保存、デバイス追跡、スライディング有効期限、ユーザー毎最大同時セッション数制限（例：最大3）。  
- JWTデュアルトークン：15分のアクセストークン＋7日のリフレッシュトークン。セッションに紐づけてリボーク（取り消し）可能にする設計。HS256のアルゴリズム固定（ピン留め）やtypクレーム検証もあり。  
- セキュリティ周辺：HttpOnly/Secure/SameSite=Strictのクッキー、HSTSやCSPなどのヘッダー、指紋除去処理。入力検証はZodで、パスワードポリシーはNIST推奨の長さベース。  
- テスト：250以上のテストに攻撃ベクトル（JWT改ざん、アルゴリズム混同、Unicode境界など）を含むスイートがあるため学習に最適。  
- ライセンスと目的：Apache-2.0で教育用。実運用向けではなく、より多機能な「Better Auth」など既製品の利用を推奨する旨が明記。

## 実践ポイント
- ローカルで触ってみる（開発サーバ起動）：
```bash
git clone https://github.com/vhscom/private-landing.git
cd private-landing
bun install
bun run build
bun run dev
```
- 学ぶべき箇所：PBKDF2の取り扱い、トークンとセッションの紐付け、タイミング攻撃対策、テスト設計。  
- 本番に移す際に優先的に追加すべき機能：レート制限／アカウントロック、漏洩済みパスワードチェック、リフレッシュトークン回転、audクレーム、監査ログ、MFA／パスキー。  
- 日本市場での意義：個人情報保護やコンプライアンス対応が求められる中、小規模サービスやスタートアップが「安全な認証設計」を理解して実装判断できることは大きな強み。

元リポジトリは学習用リファレンスとして優れているので、実装の読み解き → テストを動かす → 自分のサービス要件に合わせた拡張、という流れで学ぶのが効果的。
