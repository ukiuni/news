---
layout: post
title: "Boring Systems Earn Trust - 退屈なシステムが信頼を稼ぐ"
date: 2026-01-09T17:55:37.833Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://open.substack.com/pub/hashrocket/p/boring-systems-earn-trust?utm_campaign=post&amp;utm_medium=email"
source_title: "Boring Systems Earn Trust - by Jason Shultz"
source_id: 467022831
excerpt: "説明できる明示状態で不確実性を可視化し運用負荷を減らす、組織で即実践できる設計指針"
image: "https://substackcdn.com/image/fetch/$s_!KFG_!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2fa530b2-28d2-45c8-8618-e71770d92344_1536x1024.png"
---

# Boring Systems Earn Trust - 退屈なシステムが信頼を稼ぐ
見せかけの「賢さ」を捨てて信頼を積み上げる――実務で使える制約優先設計の勘どころ

## 要約
「賢い推論」で状態を決める設計は短期的にはスマートに見えるが、実運用では説明できない振る舞いを生みやすい。重要な真実（信頼を左右する領域）は、推論ではなく明示的な状態遷移と記録で扱うべき、という話。

## この記事を読むべき理由
多くの日本企業でも、ログ・締切・外部データなど“あいまい”な情報をベースにした自動推論に頼りがちです。金融・公共・B2B SaaSなど「信頼」が第一の領域では、ユーザー問い合わせや運用負荷が増え、ビジネスリスクになります。本記事は実務で即使える考え方と実装ヒントを提供します。

## 詳細解説
問題の核心
- 開発者には「スマートに見える」推論を入れたくなる誘惑がある：項目を増やさずに状態を導出し、表面積を減らす設計。  
- しかし複数ルールを組み合わせると、ある条件が変わったときに挙動があいまいになり、誰にも短時間で説明できなくなる（＝信頼が落ちる）。

典型例（助成金申請システム）
- 利用可能かどうかを、締切、直近フェッチ結果、ユーザーの操作履歴、外部ソースの報告などで推論すると、期限延長や再公開など現実の変化に対して脆弱になる。  
- 表面上は正しく動いていても「なぜこの案件に応募できないのか？」をコードを開かずに答えられない状態が発生する。

解決の方向性：推論をやめ、明示的な状態を採用する
- 推論ロジック（複雑なブール条件）を削除し、システムが「何を知っているか」を宣言する形にする。例：status = OPEN | CLOSED | EXTENDED | UNKNOWN、statusChangedAt、statusSource（INGESTION | USER | SYSTEM）など。
- こうすることで、UIやサポートが「現在の状態」と「その理由」を即座に示せるようになり、デバッグや説明が格段に楽になる。

簡単なコード比較（イメージ）
```javascript
// javascript
// 推論ベース（問題になりやすい）
const isAvailable = now < deadline && detailsFresh && !userDismissed && sourceStatus !== 'CLOSED';
```

```javascript
// javascript
// 明示的な状態（推奨）
const grant = {
  status: 'OPEN', // OPEN | CLOSED | EXTENDED | UNKNOWN
  statusChangedAt: '2026-01-08T12:34:56Z',
  statusSource: 'INGESTION' // or USER, SYSTEM
};
```

なぜこれが効くか（要点）
- 可視性：不確実性が「UNKNOWN」として見える。隠れた条件がなくなる。  
- 説明可能性：いつ・誰が・どのソースで状態を変えたかが残る。サポート回答が速くなる。  
- 耐変化性：未来のデータ分布が過去と違っても、制約は壊れにくい。新しい例外は状態遷移で扱う。

制約駆動設計のパターン
- 明示的な状態 > 派生状態  
- ガードレール（制約）を優先 > 過度な柔軟性  
- 冗長性（ソースやタイムスタンプ）を許容 > 「スマートな再利用」

コストと落としどころ
- カラム増、明示的な遷移、設計工数は増える。美しい抽象は犠牲になる。  
- だがバグの発見・修正が速くなり、新人の習得コストも下がるため長期的には回収できる。

## 実践ポイント
- まず監査：どのドメインで状態を“推論”しているか洗い出す（課金・可用性・契約など優先）。  
- 重要な真理には必ず「status」「statusSource」「statusChangedAt」を持たせる。  
- UI上で「UNKNOWN」や「最終更新日時」「変更理由」を見せる。ユーザーの不安を減らす。  
- 推論は「低リスクな補助領域」に限定する（ログ集計や推奨など）。  
- テスト：状態遷移テストと、状態説明を返すAPIのユニットテストを必ず作る。  
- 運用：状態変更はイベントとして記録しておき、監査ログ・アラートと繋ぐ。

日本の現場への一言
細かい例外や頻繁なビジネスルール変更が日常的な日本のシステムでは、説明可能性と運用コストの低さが顧客信頼に直結します。見栄えの良い「賢い」設計よりも、説明できる「退屈な」設計を選ぶことが、長期的な信頼とスピードを生みます。
