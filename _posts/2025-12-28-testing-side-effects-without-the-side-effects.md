---
layout: post
title: "Testing Side Effects Without the Side Effects"
date: 2025-12-28T11:16:28.763Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lackofimagination.org/2025/12/testing-side-effects-without-the-side-effects/"
source_title: "Testing Side Effects Without the Side Effects"
source_id: 436269131
excerpt: "モック不要で本番外のDBや決済に触れず構文木で注文処理を高速安全に検証する方法"
---

# 副作用を「呼ばない」テスト──モック不要で注文処理を確実に検証する方法

## 要約
副作用（データベースや決済呼び出し）を「実行するのではなく記述する」ことで、ネットワークや外部サービスに触れずに業務ロジックを完全にユニットテストできる手法を紹介します。

## この記事を読むべき理由
日本のEC／FinTech系サービスでは、決済誤請求やテスト環境の整備コストが課題です。本手法は本番外部操作を一切行わずにビジネスフローを検証でき、CIで高速かつ安全に回せるため即効性のある改善になります。

## 詳細解説
この記事の核心は「Effect System」――副作用を即時実行する命令（Promise や await）ではなく、実行予定の操作を表すプレーンなデータ（Command / Success / Failure オブジェクト）として返す設計です。関数は副作用をその場で起こさず、次の処理を記述する `next` を含んだコマンドを返します。複数の純関数を合成すると、処理の手順を表す構文木（syntax tree）が得られます。

例（簡略化）:
```js
function checkInventory(order) {
  const cmdCheckInventory = () => db.checkInventory(order);
  const next = (exists) => exists ? Success() : Failure('Out of stock');
  return Command(cmdCheckInventory, next);
}

const processOrderFlow = (order) =>
  effectPipe(
    validateOrder,
    checkInventory,
    () => chargeCreditCard(order),
    (paymentId) => completeOrder(order, paymentId)
  )(order);
```

重要な立ち位置は「processOrderFlow は純関数であり、返り値は実行命令の木である」点です。テストではその木を逐次たどって期待する命令が出ていることを検証し、擬似的に `next` を呼ぶことで成功／失敗の分岐をシミュレートします。つまりモックで外部を差し替えたり、決済をサンドボックス化したりする必要がほぼ消えます。

利点は主に3つ：
- 速度：ネットワーク/DBアクセスがないためテストが瞬時に終わる。
- 決定性：業務ロジックを純粋に検証でき、外部依存は別途統合テストで確認すればよい。
- 安全性：誤って実際のカードに課金するといったリスクがゼロ。

さらにデータとして表現されたビジネスロジックは、LLM やコード生成ツールが扱いやすく、AI支援による生成・リファクタリング・テスト補助との相性が良い、という指摘もあります。

## 実践ポイント
- 小さく始める：まずは1つのユースケース（例：注文処理）で「副作用を記述に置き換える」実験を行う。
- コマンドとインタープリタを分離する：Command オブジェクトは純粋に表現だけ持ち、実行は runEffect などのインタープリタで一元実行する。
- テスト戦略を二層化する：ユニットは構文木を検証、統合はインタープリタ経由でテストDBや決済テスト環境を使う。
- CI 時はユニットを多用して早く回す：外部サービスに依存しないためフィードバックループが短くなる。
- セキュリティ考慮：決済や個人情報の操作を記述として扱う際も、実行権限やロギングは別層で厳格に管理する。
- 既存コードの移行：一気に置き換えず、サイドエフェクトが多いモジュールから段階的に適用する。

## 引用元
- タイトル: Testing Side Effects Without the Side Effects  
- URL: https://lackofimagination.org/2025/12/testing-side-effects-without-the-side-effects/
