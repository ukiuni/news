---
layout: post
title: "Cryptographic Issues in Matrix’s Rust Library Vodozemac - MatrixのRustライブラリVodozemacにおける暗号問題"
date: 2026-02-18T01:35:46.817Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://soatok.blog/2026/02/17/cryptographic-issues-in-matrixs-rust-library-vodozemac/"
source_title: "Cryptographic Issues in Matrix&#8217;s Rust Library Vodozemac - Dhole Moments"
source_id: 1005788324
excerpt: "VodozemacのX25519欠陥で共有鍵が全ゼロ化、通信乗っ取りの危険―即刻依存確認を"
image: "https://i0.wp.com/soatok.blog/wp-content/uploads/2026/02/BlogHeader-2026-Matrix-Vodozemac.png?fit=1200%2C675&#038;ssl=1"
---

# Cryptographic Issues in Matrix’s Rust Library Vodozemac - MatrixのRustライブラリVodozemacにおける暗号問題
暗号鍵が「ゼロ」にされる？Vodozemacで見つかった致命的ミスと今すぐ取るべき対策

## 要約
Vodozemac（MatrixのRust実装）に、X25519の出力が全ゼロになるケースを検出せず共有鍵が完全に予測可能になる重大脆弱性など複数の暗号上の問題が報告されました。公開と修正提案は研究者が短期間で行っています。

## この記事を読むべき理由
Matrix／Elementを利用する個人・組織、あるいはVodozemacを含むクライアントやサーバー実装に依存している日本の開発者は、自分たちの通信が脆弱になっている可能性を把握し、対策を急ぐ必要があります。

## 詳細解説
- 主要な脆弱性（重大）
  - X25519ベースのDiffie–Hellmanで「アイデンティティ要素（all-zero公開鍵）」を受け入れてしまう経路があり、スカラー乗算の結果が全ゼロ（shared secret = 0）となってしまう。結果として暗号鍵が攻撃者により容易に判明し得る。
  - 原因はライブラリが x25519_dalek の SharedSecret.was_contributory() を呼ばず、非寄与（non-contributory）出力を検出しない点にある。RFC 7748 / RFC 9180 の指針では、X25519の出力が全ゼロであれば中止すべきと明示されている。
- 攻撃のイメージ
  - Diffie–Hellman を単純化すると送受信は $g^a, g^b$ をやり取りして最終的に $g^{ab}$ を共有する仕組み。相手の公開鍵が「ゼロ」に該当すると共有値は常にゼロになり安全性は消失する。
- その他報告された問題（簡潔）
  - V2→V1へのダウングレード攻撃（低〜中程度）
  - ECIESのチェックコードが100通りしかなく衝突しやすい
  - メッセージ鍵が MAX_MESSAGE_BYTES 超で silently dropped される
  - Pickle（シリアライズ）で決定的IVを使っている部分がある
  - #[cfg(fuzzing)] でMACや署名検証をバイパスするビルドフラグが混在
  - Ed25519の厳格検証がデフォルトで無効になっている点
- 開示の経緯
  - 研究者は2026-02-11に報告、短期間（約1週間）で公開。過去のやり取りから90日ルールを適用しない判断をした旨。

参考となる修正（概念）：
```rust
rust
let first = one_time_key.diffie_hellman(remote_identity_key);
if !first.was_contributory() { return Err(KeyError::NonContributory); }
```

## 実践ポイント
- 影響範囲確認：自分のプロジェクトで Vodozemac を使っているか依存ツリーを即確認する。
- まずはアップデート：公式パッチが出るまで、可能なら vodozemac を最新の修正版に更新するか、当面の間該当機能を無効化する。
- バリデーションを入れる：公開鍵入力や共有鍵出力に対して was_contributory()/all-zero チェックを入れることを推奨。
- 設定とビルドフラグ確認：fuzz用のビルドフラグや「緩い」署名検証が本番に入っていないか確認する。
- 通知と監査：エンドユーザーや他のクライアント実装への周知、サードパーティ依存ライブラリの監査を行う。
- 今後の教訓：暗号プリミティブは「正しく使う」ことが必須。ライブラリの安全契約（RFC等）を実装レイヤで満たしているか定期的にチェックする。

（参考元: Soatok, "Cryptographic Issues in Matrix’s Rust Library Vodozemac", 2026）
