---
layout: post
title: "The State of OpenSSL for pyca/cryptography - pyca/cryptography における OpenSSL の現状"
date: 2026-01-14T23:30:22.306Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cryptography.io/en/latest/statements/state-of-openssl/"
source_title: "The State of OpenSSL for pyca/cryptography &mdash; Cryptography 47.0.0.dev1 documentation"
source_id: 46624352
excerpt: "OpenSSL3の性能・安全問題でcryptographyがRust等へ移行検討、配布者は即対応を"
---

# The State of OpenSSL for pyca/cryptography - pyca/cryptography における OpenSSL の現状
OpenSSL 3 の「重さ」が示すもの — pyca/cryptography が示す代替と日本の開発者が今すべき対策

## 要約
pyca/cryptography チームは OpenSSL 3 の設計・性能面の後退を理由に、OpenSSL への依存を段階的に減らす方針を明示した。具体的には性能低下、APIの複雑化、テスト不足、メモリ安全性の問題が主因で、LibreSSL/BoringSSL/AWS‑LC や独自実装（Rust 等）への移行を検討している。

## この記事を読むべき理由
日本のライブラリ作者やソフトウェア配布者は、pyca/cryptography の方針変更がバイナリ配布（wheel）やランタイム性能、セキュリティ保証に直結するため、今のうちに影響と対応策を把握しておく必要がある。

## 詳細解説
- 性能面  
  OpenSSL 1.1.1 から 3.0.x で鍵読み込みや DER/X.509 解析に大幅な遅延が発生。pyca/cryptography 側で Rust による独自実装に切り替えたところ、鍵読み込みで数倍の改善、X.509 全体検証で最大 60% の高速化を観測した。多くはコピーや不要なロック、ハッシュテーブルなど基本的なオーバーヘッドの除去によるもの。

- API と複雑性  
  OpenSSL 3 は OSSL_PARAM（キー・バリュー配列）や「provider」機構を導入し、汎用性は上がったが呼び出しの冗長化、コンパイル時検査の低下、実行時の割込み可能性（任意タイミングでアルゴリズム差替え）が増え、内部で多数のキャッシュやロック、RCU といった複雑な対処を強いている。結果としてコードの可読性・追跡性が落ち、バグ調査が難しくなった。

- テストと検証の不足  
  CI のフラッキーさ、回帰テスト不足、特定ハードウェア（例：AVX‑512）でのみ発現するバグの見逃しなどが報告されている。フォーマル検証や自動化検査を積極的に取り入れる他プロジェクト（BoringSSL, AWS‑LC）と比較すると差がある。

- メモリ安全性と 言語戦略  
  Rust 等を使ったメモリ安全な実装への移行は現実的で効果がある。pyca/cryptography は既に多くのパーシングやX.509関連を Rust に移し、いくつかの CVE を回避している。OpenSSL 自体は同様の大幅な言語移行に取り組んでいない。

- 将来の方針  
  pyca/cryptography は今後、新機能で OpenSSL を必須にせず、LibreSSL/BoringSSL/AWS‑LC を優先する可能性を明示。バイナリ配布で内蔵する OpenSSL をフォークに差し替える検討も行っており、最終的には OpenSSL サポートを打ち切る場合もあり得る。

## 実践ポイント
- まずは影響範囲の把握  
  使用している pyca/cryptography のバージョンと、それがどの OpenSSL 実装に依存しているかを確認する。自社や配布先の環境（ディストリやクラウド）で互換性問題がないか検証する。

- ベンチとテストを自前で回す  
  鍵読み込みや証明書検証など、実アプリで重要な処理をベンチマークし、OpenSSL 1.1.1 / 3.x / 他フォークでの差を確認する。CI に AVX‑512 を含む異なる CPU 構成でのテスト（Intel SDE 等を活用）を組み込む。

- バイナリ配布者はリンク方針を検討する  
  wheel 等で OpenSSL を静的に同梱している場合、LibreSSL/BoringSSL/AWS‑LC への切替検討や、依存を緩めるためのパッケージング戦略を早めに策定する。

- テストと回帰カバレッジの強化  
  pyca/cryptography の指摘にある通り、暗号周りはテストが命。新しい OpenSSL バージョンを採用する際は回帰テスト、フォールトインジェクション、fuzzing を回しておく。

- 長期的にはメモリ安全な実装を検討する  
  可能ならパースやプロトコル処理をメモリ安全言語（Rust 等）で再実装する方針を検討する。既存ライブラリの置き換えや、内部モジュールの段階的移行が現実的な選択肢。

- コミュニティへの関与  
  OpenSSL 側に改善を望むなら issue 提出やパッチ、資金支援、CI 事例の提供などで積極的に関与することが最も影響力がある。

日本の現場では、配布先の多様性（オンプレ、クラウド、IoT）を考えると「今すぐ何が壊れるか」を把握して段階的に対応することが実務上の最優先。 pyca/cryptography の方針変更は警鐘であり、賢く準備すれば機会にもなる。
