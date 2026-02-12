---
layout: post
title: "Email is tough: Major European Payment Processor's Emails aren't RFC-Compliant - メールは難しい：大手欧州決済プロバイダのメールがRFC準拠していない"
date: 2026-02-12T15:17:32.142Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://atha.io/blog/2026-02-12-viva"
source_title: "Major European Payment Processor Can&#x27;t Send RFC-Compliant Email | The Ian Atha Museum of Internet Curiosities"
source_id: 46989217
excerpt: "大手欧州決済vivaがMessage-ID欠落でGoogle受信拒否、貴社の決済も危機に。"
image: "https://atha.io/static/images/twitter-card.png"
---

# Email is tough: Major European Payment Processor's Emails aren't RFC-Compliant - メールは難しい：大手欧州決済プロバイダのメールがRFC準拠していない

ビジネス用メールが届かない原因は「ヘッダーの基本」が抜けていた — あなたの決済基盤も他人事ではない。

## 要約
欧州の大手決済プロバイダ viva.com が送る確認メールに必須の Message-ID ヘッダが欠落し、Google Workspace が受信を拒否（550 5.7.1）。サポートは技術問題を認めず、ユーザーは個人の Gmail で回避する羽目に。

## この記事を読むべき理由
決済プラットフォームは事業運営の根幹。簡単な RFC 準拠すら守れないサービスを使うリスクを理解し、国内外の決済選定やトラブル対応で実務的に役立つ視点が得られます。

## 詳細解説
- 問題点：RFC 5322（メールの基本仕様）で要求される Message-ID ヘッダが送信メールに含まれていない。2001年の RFC 2822、2008年の RFC 5322 で必須。  
- 影響：Google Workspace 等は「Messages missing a valid Message-ID header」として即時拒否（バウンス）。メーラーのスパム判定以前に届かない。  
- サポート対応：技術的な報告を行っても「あなたのアカウントは確認済みだから問題ない」とのみ返答。根本原因の修正やエンジニアへのエスカレーションがない。  
- 背景的意味合い：ドキュメント不足・サポートの技術力不足・市場の競争圧の低さが原因で、開発者体験や信頼性が低くなるケースがある。Stripe のような高品質な代替が特定ローカルレールをサポートしていない市場では、この種の問題に依存せざるを得ない。

## 実践ポイント
- まず試す：Google Workspace の Email Log Search でバウンス理由を確認する。  
- 一時回避：個人の @gmail.com で受け取れるか試す（ただし恒久対策ではない）。  
- ベンダーに要請する内容（コピペ可）：
  - 「RFC 5322 に従い、送信トランザクションメールに Message-ID ヘッダを追加してください。例：」
  
```text
Message-ID: <unique-id@viva.com>
```

- 技術チェック：自社で決済連携する際は送信メールのヘッダを SMTP ログか受信側のログで確認する習慣をつける。  
- 選定基準：決済事業者を選ぶ際は「開発者ドキュメントの充実度」「サポートの技術回答例」「ローカル決済対応状況」を評価項目に加える。
