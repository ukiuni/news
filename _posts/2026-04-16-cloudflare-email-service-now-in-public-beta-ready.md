---
layout: post
title: "Cloudflare Email Service: now in public beta. Ready for your agents - Cloudflare Email Service：パブリックベータ公開。エージェント対応準備完了"
date: 2026-04-16T14:15:06.399Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/email-for-agents/"
source_title: "Cloudflare Email Service: now in public beta. Ready for your agents"
source_id: 47792593
excerpt: "Cloudflareのメール公開ベータで、Workers連携のエージェントが受信→処理→返信を自動化"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/3RDH6grpXMz6DWEQmZgXj9/0dcfca0bf86c72e933d4fcb8b585b45c/OG_Share_2024-2025-2026__2_.png"
---

# Cloudflare Email Service: now in public beta. Ready for your agents - Cloudflare Email Service：パブリックベータ公開。エージェント対応準備完了
InboxがあなたのAIを“仕事させる”日：CloudflareのEmail Serviceでメールをエージェントの第一級インターフェースに

## 要約
CloudflareがEmail Sendingをパブリックベータに移行し、Email RoutingとAgents SDK、Workers連携で「受信→処理→送信」をクラウド上で完結できるメールネイティブなエージェント基盤を提供します。

## この記事を読むべき理由
メールは誰でも持っている普遍的なインターフェースで、日本のサポートや業務自動化でも主要チャネルです。送受信の認証や配信改善を自動化しつつ、Cloudflareのネットワーク上で低遅延にエージェントを動かせる点は、日本のプロダクト／SRE／カスタマーサポートに直結する価値があります。

## 詳細解説
- 主要コンポーネント
  - Email Sending：Workersバインディングで直接送信（APIキー不要）。REST/API/TypeScript/Python/Go SDKも利用可。
  - Email Routing：受信をWorkersにルーティングし、オンチェーン処理が可能。
  - Agents SDK：onEmailフックで受信メールをDurable Objectsに紐づけて状態を保持。返信は非同期で行え、長時間の処理やエスカレーションが可能。
  - 配信と認証：ドメイン追加時にSPF/DKIM/DMARCを自動設定して配信性を高める。
  - 補助ツール：MCPサーバ、Wrangler CLI、Email Service Skill、オープンソースのAgentic Inbox（参照実装）。
- セキュリティ／運用
  - 返信ルーティングにHMAC-SHA256署名を使い、なりすましで別エージェントに返信が流れるリスクを低減。
  - GlobalなCDNネットワーク上で配信するため低遅延・高可用。
- 開発フロー（簡易コード例）
  - Workersから送信する例（概念的）：

```javascript
export default {
  async fetch(request, env) {
    await env.EMAIL.send({
      to: "user@example.com",
      from: "no-reply@yourdomain.com",
      subject: "注文が発送されました",
      text: "ご注文 #1234 を発送しました。"
    });
    return new Response("Email sent");
  },
};
```

- エージェント設計ポイント
  - アドレスベースのルーティング（support@ → SupportAgent）やサブアドレス（support+billing@）でインスタンス振り分け。
  - setStateで会話履歴をDurable Objectsに保持し、外部DB不要で「受信箱＝エージェントの記憶」にできる。

## 実践ポイント
- まずはCloudflareダッシュボードでEmail Sendingを有効化し、ドメインを追加してSPF/DKIM/DMARCを自動設定する。
- Workersバインディングで送信を試し、Email Routingで受信→onEmailフックの流れを確認する。
- Agents SDKのonEmailでstate保存→非同期処理→sendEmailのパターンを実装してサポート自動化を試す。
- Wrangler CLIやMCPを使えばローカルや外部エージェントからもメール送信が可能。CI/CDやビルド通知に組み込むと即効性あり。
- Agentic Inboxをデプロイして参照実装をフォークし、自社ワークフローに合わせて拡張する。

短く試すなら「ダッシュボードでドメイン追加 → Workersで env.EMAIL.send を呼ぶ」だけで配信・認証・低遅延の恩恵を体感できます。
