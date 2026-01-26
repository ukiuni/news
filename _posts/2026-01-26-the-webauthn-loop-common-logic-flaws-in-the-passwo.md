---
layout: post
title: "The WebAuthn Loop: Common Logic Flaws in the \"Passwordless\" Handshake - 「WebAuthnループ：『パスワードレス』ハンドシェイクの論理的欠陥」"
date: 2026-01-26T14:19:45.644Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/the-webauthn-loop-common-logic-flaws-in-the-passwordless-handshake"
source_title: "WebAuthn Logic Flaws: Breaking the Passwordless Handshake | InstaTunnel Blog"
source_id: 417099748
excerpt: "パスキー実装のハンドシェイクと復旧欠陥により、フェイクドメインやリプレイで乗っ取り可能に"
image: "https://i.ibb.co/3yktxnpk/The-Web-Authn-Loop-Common-Logic-Flaws-in-the-Passwordless-Handshake.png"
---

# The WebAuthn Loop: Common Logic Flaws in the "Passwordless" Handshake - 「WebAuthnループ：『パスワードレス』ハンドシェイクの論理的欠陥」
パスキーは安全神話ではない—実装の“手順ミス”が攻撃経路を生む理由

## 要約
WebAuthn（FIDO2）ベースのパスキーは理論上フィッシング耐性を持つが、フロントエンドとバックエンドの握手（handshake）や回復フローの論理的ミスマッチが「WebAuthnループ」と呼ばれる脆弱性を生む。実装で注意すべきポイントは主に5つ。

## この記事を読むべき理由
日本でも大手サービスや IDaaS がパスキー対応を急速に進めており、実装ミスは国内ユーザーのアカウント乗っ取りや企業の信頼失墜につながる。初心者でも分かる形で、現場で即使えるチェックリストを示す。

## 詳細解説
1. WebAuthnハンドシェイクの要点（超簡潔）
   - 登録（Registration）：サーバがチャレンジを出し、端末が公開鍵・credentialId・attestationを返す。サーバは署名と証明を検証して公開鍵を保存。
   - 認証（Authentication）：サーバが新しいチャレンジを送り、端末が署名して返し、サーバが保存済み公開鍵で検証。
   - 重要：ブラウザはOrigin（発行元）バインディングを行うが、サーバ側の検証も必須。

2. 欠陥1 — Origin & RP ID 検証ギャップ
   - 問題点：authenticatorのclientDataJSON内のoriginをサーバで検証しない実装がある。
   - 危険：正当な署名でも「別の悪意あるドメイン」を経由してリレーフィッシングが可能になる。
   - 対策：サーバ側でclientDataJSONのoriginを厳密照合。関連ドメインはRelated Origin Requests（ROR）等で安全に扱う。

3. 欠陥2 — 静的チャレンジとリプレイ
   - 問題点：チャレンジを予測可能・再利用可能にすると、署名済みレスポンスを再送して認証を突破される。
   - 要件：サーバ生成の高エントロピーチャレンジ（推奨16バイト以上）、使い捨て、TTL短め。
   - 対策：「Challenge-Store-Verify」パターン（Redis等でチャレンジを保存し、検証後すぐ削除）。

4. 欠陥3 — 回復（Recovery）パラドックス（弱い縁が全体を壊す）
   - 問題点：パスキー紛失時の復旧でSMS OTPやメールリンクを使うと、攻撃者はそこを突く。
   - 危険：SIMスワップやソーシャルエンジニアリングでパスキーの利点が帳消しに。
   - 対策：複数端末の登録を促す、ワンタイム回復コード（オフライン保管）、高リスクアカウントは待機や手動確認を導入。

5. 欠陥4 — 証明（Attestation）軽視と仮想認証器
   - 問題点：attestationを"none"にしてしまうと、ソフトウェア製の仮想認証器で生成された鍵も受け入れてしまう。
   - 危険：ハードウェア保護がないキーを正規と扱うと、本来の安全性が失われる。
   - 対策：FIDO Metadata（MDS3）で認証器特性を確認し、ポリシーに応じてattestationを検証する。

6. 欠陥5 — フロントエンド／バックエンドの非同期（Successful Failure）
   - 問題点：フロントが「成功」と返しただけでバックが署名検証を省くケースがある。
   - 危険：中間者がフロントのAPI呼び出しを改竄して「成功」を送れば認証をバイパスできる。
   - 対策：サーバ側が生データ（authData, clientDataJSON, signature）を必ず検証する。フロントは運搬に徹する。

## 実践ポイント
- 起点：まずは既存のWebAuthnライブラリ（SimpleWebAuthn / FIDO2-lib / IDaaS）を利用する。自前実装は避ける。
- サーバチェックリスト（必須）
  - clientDataJSON.origin を厳密比較する。
  - チャレンジはサーバ生成・高エントロピー・一度きり・短TTLで管理する（Challenge-Store-Verify）。
  - 署名検証はバックエンドのみで行う。
  - Attestationポリシーを定め、必要ならMDS3で確認。
  - 回復フローを最小化し、SMSは「劣化モード」として権限制限・通知を行う。
- UX提案：パスキー優先の画面表示、バックアップデバイスの登録を初回で促す。
- 日本向け注意点：国内キャリアのSIMスワップ被害やSMS二段階の運用実態を踏まえ、SMS復旧は最小化すること。

パスキーは強力だが「論理」が甘ければ意味がない。実装と運用の両側をチェックして、WebAuthnの利点を現実の安全に変えよう。
