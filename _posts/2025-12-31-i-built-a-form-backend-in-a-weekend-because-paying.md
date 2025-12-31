---
layout: post
title: "I Built a Form Backend in a Weekend Because Paying $20/Month for Contact Forms is Stupid - 連絡フォームに月20ドル払うのは馬鹿らしいから、週末でフォーム用バックエンドを作った話"
date: 2025-12-31T15:36:48.388Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/varshithvhegde/i-built-a-form-backend-in-a-weekend-because-paying-20month-for-contact-forms-is-stupid-1o34"
source_title: "I Built a Form Backend in a Weekend Because Paying $20/Month for Contact Forms is Stupid"
source_id: 3136225
excerpt: "週末で自前のフォームバックエンドを作り、月額数千円を節約してデータを自社管理する方法を解説"
---

# I Built a Form Backend in a Weekend Because Paying $20/Month for Contact Forms is Stupid - 連絡フォームに月20ドル払うのは馬鹿らしいから、週末でフォーム用バックエンドを作った話
魅力タイトル: 「フォームだけで月3,000円払うの、もうやめませんか？――週末で作れる自前のフォームバックエンド」

## 要約
外部SaaSに月額で払うより、自分でホストするフォームバックエンド（保存・メール・ダッシュボード）を週末で立ち上げた話。Next.js + Supabase + Resend（またはSMTP）で低コストかつ制御可能に。

## この記事を読むべき理由
フォームは機能的には単純でも、SaaSだと数千円/月かかることが多い。特に個人開発者や小規模制作物では、コストとデータコントロールを両立できる実装が有用。日本の個人サイト・ポートフォリオ運営者やスタートアップ初期のコスト最適化に直結する話題です。

## 詳細解説
- 発端：著者は友人のポートフォリオに連絡フォームを入れる際、既存のフォームSaaSの月額料金に疑問を感じ、自作することを決めた。
- 構成：
  - フロント：通常のHTMLフォームを向けるだけ。
  - バックエンド：フォームデータを受け取り、Supabase（Postgres）に保存、通知メールを送信、エントリを閲覧する簡易ダッシュボードを提供。
  - デプロイ：Vercelなどのホスティングに配置。
  - メール：Resend（無料枠3,000通/月）を利用、既存のSMTPがあればそれでも代替可能。
- 技術スタック（元記事が採用）：
  - Next.js 15（App Router + Server Actions を活用）
  - Supabase（Postgres、リアルタイム、認証）
  - Tailwind CSS / Radix UI / Lucide icons
  - ResendまたはSMTP
- ポイント：
  - 「保存＋通知」が主目的なので、実装自体はシンプル。
  - VercelとSupabaseの無料枠を組み合わせれば月額0円運用も現実的。
  - 自分でホストすることでデータの所有権とプライバシー管理がしやすい（重要：日本では個人情報保護法＝APPIへ配慮を）。
- 注意点：
  - 「セルフホスティング」と言っても Vercel/Supabase に載せる＝完全オンプレではない。運用責任やセキュリティ設定は必要。
  - データ保持・削除方針、暗号化、バックアップ、スパム対策（CAPTCHA等）は別途実装すべき。
  - 法規制（GDPR 相当や日本の個人情報保護）に沿った利用規約・プライバシーポリシーが必要。

## 日本市場との関連
- コスト感：海外で「$20/月」と言われるサービスは、日本円で数千円/月。個人や学生、フリーランスのランニングコストとして無視できない金額です。
- 法規制：日本のAPPI準拠や企業案件での個人情報取り扱いルールを満たすため、自前でログ管理や削除ポリシーを整えるメリットがある。
- インフラ事情：国内でVercel/Supabaseを使っても遅延は小さいため、国内ユーザー向け静的サイト＋外部フォームバックエンドの組合せは現実的。
- エンタープライズではなく「個人〜SMB」向けに最も刺さる実装。

## 実践ポイント
- まずはデモを触る：元プロジェクトのデモやリポジトリを確認して、動作を体験する（疑似フォームで送ってみる）。
- デプロイ手順（概略）：
  1. GitHubでリポジトリをFork。
  2. Vercelで「Deploy」ボタンを押す（環境変数を設定）。
  3. SupabaseでDBテーブルを作成し、接続文字列を環境変数に入れる。
  4. メール送信はResendのキー、もしくは自ドメインのSMTPを設定。
- セキュリティと運用：
  - DBには不要な個人情報を保存しない。必要なら暗号化と削除機能を追加。
  - スパム対策としてhoneypotやreCAPTCHAを導入。
  - 定期的に依存ライブラリを更新し、公開鍵/シークレットはVault等で管理。
- コスト判断：トラブルシューティングにかかる時間とSaaSの年間コストを比較して、自力運用が割に合うか判断する。
- カスタマイズ性：必要ならWebhookやZapier連携を追加して既存ワークフローに接続可能。

## 引用元
- タイトル: I Built a Form Backend in a Weekend Because Paying $20/Month for Contact Forms is Stupid
- URL: https://dev.to/varshithvhegde/i-built-a-form-backend-in-a-weekend-because-paying-20month-for-contact-forms-is-stupid-1o34

（参考：元プロジェクトはMITライセンスで公開。Supabase／Vercel／Resend の無料枠をうまく使うことで、週末プロジェクトとして低コストに導入可能です。）
