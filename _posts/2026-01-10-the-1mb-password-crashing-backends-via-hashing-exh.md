---
layout: post
title: "The 1MB Password: Crashing Backends via Hashing Exhaustion - 1MBパスワード：ハッシュ処理枯渇でバックエンドを落とす"
date: 2026-01-10T06:28:09.475Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://instatunnel.my/blog/the-1mb-password-crashing-backends-via-hashing-exhaustion"
source_title: "The 1MB Password: How Hashing Exhaustion Crashes | InstaTunnel Blog"
source_id: 466521964
excerpt: "1MBパスワードでハッシュ処理を枯渇させサービスを停止させる攻撃と防御法"
image: "https://i.ibb.co/XZRhr5xZ/The-1-MB-Password-Crashing-Backends-via-Hashing-Exhaustion.png"
---

# The 1MB Password: Crashing Backends via Hashing Exhaustion - 1MBパスワード：ハッシュ処理枯渇でバックエンドを落とす
1MBの「パスワード」がバックエンドを沈める — あなたの“安全な”ハッシュ設定が招く意外なDoS

## 要約
遅くて「安全」なパスワードハッシュ（Argon2/Bcrypt/PBKDF2）は、長すぎる入力を処理するとCPUやメモリを枯渇させ、少数のリクエストでサービス停止に至る可能性がある。アプリ側で最大長やプリハッシュ、エッジでの制限を入れれば簡単に防げる。

## この記事を読むべき理由
日本のスタートアップやクラウド運用チームは、認証エンドポイントが狙われると可用性・請求額・顧客信頼に直結する。Django、Laravel、Node.jsが広く使われる日本の現場では、既定の設定だけではこの攻撃に無防備なことが多い。

## 詳細解説
- 「遅いハッシュ」の逆説  
  適応的ハッシュ（work factor を持つもの）は総当たりに強い一方、入力長 $n$ に対する処理コストも無視できない。概念的な計算量は  
  $$O(n \times \text{work\ factor})$$  
  となり、$n$ が 1,000,000（1MB）になると数秒〜数十秒のCPU時間を要し得る。

- アプリ層攻撃である点の厄介さ  
  1MBのPOSTはネットワーク的には一件の「大きめの正当なリクエスト」に見えるため、従来のWAFやネットワークレート制御をすり抜けやすい。ハッシュ処理中はワーカやメインスレッドが塞がり、他のリクエスト処理が停滞する。

- アルゴリズム別の挙動（簡潔）  
  - Bcrypt: 実装上72バイト以降を切り捨てるため、長尺攻撃には耐性がある（ただしセキュリティ上の注意点あり）。  
  - Argon2id: 任意長入力を正確に処理するため、長大入力でメモリ・CPUを大量消費する。  
  - PBKDF2: CPUバウンドで長さに比例して負荷が増える。

- フレームワークの落とし穴  
  多くのフレームワークは最低長チェックを用意するが、最大長（max length）をデフォルトで設けていない場合がある。さらに、NodeやPHPのライブラリは受け取った文字列をそのままハッシュ関数に渡すことが多く、入力検査が不十分だと攻撃が直撃する。

- 環境面の影響  
  Node.js のシングルスレッド性や、Pythonの限定的なワーカープールなどでハッシュ処理が他の処理をブロックする実運用のリスクが高い。

## 実践ポイント
- 最大長を設定する（最も重要）  
  パスワード最大長を 128〜256 字に制限する。現実的なパスフレーズはこれで十分であり、処理負荷を劇的に下げられる。

- 先にバリデーション／拒否する  
  JSON ボディサイズやフィールド長をロードバランサ／WAF（Cloudflare、AWS ALB、NGINX等）でエッジ段階で弾く。ログインフォームのPOSTなら 10KB を超えない想定にする。

- 必要ならプリハッシュを導入（注意点あり）  
  極端に長い入力をどうしても受けたい場合は、まず SHA-256 等の高速な固定長ハッシュを取り、その出力を Argon2/Bcrypt に渡す。ただし既存ユーザーとの互換性と移行計画が必要。概念コード例：

  ```javascript
  // javascript
  const crypto = require('crypto');
  const argon2 = require('argon2');

  // password は大きな文字列でも可
  const preHash = crypto.createHash('sha256').update(password).digest('hex');
  const finalHash = await argon2.hash(preHash);
  ```

- レート制限とスロットリング  
  IP／アカウント単位のレート制限を厳格に。ログイン・登録はリーキー・バケット等で短期間の同時処理数を抑える。

- 入力検証ライブラリを活用する  
  Node: Joi 等で先に max を検証する。Laravel: バリデータで max:255 等を指定。例（短縮）：

  ```javascript
  // javascript
  const schema = Joi.object({
    username: Joi.string().email().required(),
    password: Joi.string().min(12).max(128).required()
  });
  ```

- 運用監視と緊急対策  
  認証エンドポイントのCPU使用率やレスポンスタイムを監視し、異常時は一時的にパスワード認証を遅延させる、もしくはWAFでサイズ超過を即ブロックする手順を用意する。

- 日本の現場での注意点  
  クラウド課金（リクエスト処理時間）やSLA、顧客対応コストにつながるため、セキュリティと可用性のバランスを明確に。既存ユーザーへのポリシー変更はユーザー通知・段階的移行を計画する。

まとめ（ワンポイント）  
「強いハッシュ」は正義だが、入力の長さも同じくらい重要。最も手早く効果的なのはアプリレイヤーでの最大長制限とエッジでのサイズチェック。これだけで“1MBパスワード”という単純だが強力なDoSを防げる。
