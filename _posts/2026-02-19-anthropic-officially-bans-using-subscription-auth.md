---
layout: post
title: "Anthropic officially bans using subscription auth for third party use - Anthropicがサブスクリプション認証の第三者利用を正式に禁止"
date: 2026-02-19T03:49:33.751Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://code.claude.com/docs/en/legal-and-compliance"
source_title: "Legal and compliance - Claude Code Docs"
source_id: 47069299
excerpt: "Claudeの個人サブスク認証を外部で使うと契約違反に—APIキーへ即移行を"
image: "https://claude-code.mintlify.app/_next/image?url=%2F_mintlify%2Fapi%2Fog%3Fdivision%3DResources%26appearance%3Dsystem%26title%3DLegal%2Band%2Bcompliance%26description%3DLegal%2Bagreements%252C%2Bcompliance%2Bcertifications%252C%2Band%2Bsecurity%2Binformation%2Bfor%2BClaude%2BCode.%26logoLight%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fo69F7a6qoW9vboof%252Flogo%252Flight.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Do69F7a6qoW9vboof%2526q%253D85%2526s%253D536eade682636e84231afce2577f9509%26logoDark%3Dhttps%253A%252F%252Fmintcdn.com%252Fclaude-code%252Fo69F7a6qoW9vboof%252Flogo%252Fdark.svg%253Ffit%253Dmax%2526auto%253Dformat%2526n%253Do69F7a6qoW9vboof%2526q%253D85%2526s%253D0766b3221061e80143e9f300733e640b%26primaryColor%3D%25230E0E0E%26lightColor%3D%2523D4A27F%26darkColor%3D%25230E0E0E%26backgroundLight%3D%2523FDFDF7%26backgroundDark%3D%252309090B&amp;w=1200&amp;q=100"
---

# Anthropic officially bans using subscription auth for third party use - Anthropicがサブスクリプション認証の第三者利用を正式に禁止
魅力的タイトル: 「Claudeの“個人アカウント”を使ってサードパーティ連携してはいけない—開発者が今すぐ確認すべき理由」

## 要約
AnthropicはClaude Codeで、Free/Pro/Max（OAuthベース）のサブスク認証トークンを第三者サービスやAgent SDKで使うことを禁止し、開発者向けにはAPIキー認証（Claude Consoleや対応クラウド経由）を必須化しました。

## この記事を読むべき理由
日本のスタートアップやSaaS事業者がClaudeを組み込む際、誤った認証運用は契約違反やサービス停止リスクにつながります。今すぐ認証設計を見直すべき重要情報です。

## 詳細解説
- 認証の区別：AnthropicはOAuthトークン（Free/Pro/Max）をClaude Code/Claude.ai専用と定義。これらを他サービスやAgent SDKで流用する行為は消費者利用規約違反になる。  
- 開発者向け推奨：プロダクトや統合を作る場合は、Claude Consoleやサポートされるクラウドプロバイダ（例：AWS Bedrock、Google Vertex）で発行するAPIキーを使うこと。  
- 第三者提供の制限：サードパーティがユーザー向けにClaude.aiログインを提供したり、ユーザーのFree/Pro/Max資格情報経由でリクエストを中継することは許可されない。Anthropicは違反に対して無予告で措置を取る権利を保有。  
- コンプライアンス面：医療用途では、既存のBAA契約とZero Data Retention（ZDR）を適用すればClaude CodeにもBAAが拡張される旨が明記されている。  
- 利用制限と信頼性：Pro/Maxの広告上の利用上限は個人利用を前提としているため、サーバー側で大規模に共有する運用は想定外。

## 実践ポイント
- 即対応：自社プロダクトでClaudeを使う場合、OAuthトークンの流用をやめ、APIキー認証へ移行する。  
- 契約確認：商用利用はCommercial Termsが適用。クラウド経由（Bedrock/Vertex）での利用条件も確認。  
- 医療対応：医療データを扱うならBAAとZDRの有無を確認・契約。  
- 実装チェック：ログ・コードレビューでOAuthトークンが外部サービスの認証に使われていないか検出する（自動化ルール推奨）。  
- サポート連絡：認証の特殊ケースや疑問はAnthropicの営業窓口に相談する。

短く言えば：Claude組み込み時は「個人サブスクのOAuthは使わない」「公式APIキー／クラウド経由で正しく認証する」を徹底してください。
