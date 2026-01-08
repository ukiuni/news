---
layout: post
title: "Clang Hardening Cheat Sheet - Ten Years Later - Clang ハードニング チートシート — 10年後"
date: 2026-01-08T20:49:30.406Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.quarkslab.com/clang-hardening-cheat-sheet-ten-years-later.html"
source_title: "Clang Hardening Cheat Sheet - Ten Years Later - Quarkslab's blog"
source_id: 782934586
excerpt: "Clangの最新ハードニング旗で実運用バイナリの攻撃面を劇的に減らす方法を解説"
---

# Clang Hardening Cheat Sheet - Ten Years Later - Clang ハードニング チートシート — 10年後
思わずビルド設定を見直したくなる！Clang の最新ハードニング旗（フラグ）まとめ

## 要約
Clang/LLVM と攻撃手法はこの10年で進化した。OpenSSF の推奨を含め、コンパイラ／リンカの新しいハードニングオプション（スタック・クラッシュ防止、CET、nodlopen、FORTIFY_SOURCE=3、など）を組み合わせて使うことで、実運用バイナリの攻撃面を大きく減らせる。

## この記事を読むべき理由
日本のサーバー、組み込み、デスクトップ向けソフトウェアは依然として C/C++ 製が多く、供給連鎖やプラグイン・ロードを狙った攻撃が増えている。コンパイル時に設定するだけで効果の大きい防御手段があるため、ビルドパイプラインを管理するエンジニアは必読。

## 詳細解説
- OpenSSF の推奨オプション（要点）
  - 基本の最適化と警告: -O2 -Wall -Wformat -Wformat=2 -Wconversion -Wimplicit-fallthrough
  - セキュリティ強制: -Werror=format-security -D_FORTIFY_SOURCE=3 -U_FORTIFY_SOURCE
  - libstdc++ の追加チェック: -D_GLIBCXX_ASSERTIONS
  - メモリ関連: -fstrict-flex-arrays=3
  - スタック防御: -fstack-clash-protection -fstack-protector-strong
  - リンカで攻撃面を減らす: -Wl,-z,nodlopen -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,--as-needed -Wl,--no-copy-dt-needed-entries

  コード例（推奨フラグの一例）:
  ```bash
  clang -O2 -Wall -Wformat=2 -Wconversion -D_FORTIFY_SOURCE=3 \
        -D_GLIBCXX_ASSERTIONS -fstack-protector-strong \
        -fstack-clash-protection -fstrict-flex-arrays=3 \
        -Wl,-z,nodlopen,-z,relro,-z,now,--as-needed ...
  ```

- Fortify（-D_FORTIFY_SOURCE=3）
  - memcpy / memmove、snprintf 系、strtok/strncat などの危険なパターンを追加検査。ビルド時にサイズ情報があれば実行時チェックを挿入。

- C++ 標準ライブラリの強化（-D_GLIBCXX_ASSERTIONS）
  - NULLチェックや境界チェックなど、libstdc++ の追加アサーションを有効化。デバッグでは特に有効だが、本番でも検討可能。

- nodlopen（-Wl,-z,nodlopen）
  - dlopen による実行時ロードを禁止。プラグイン/拡張を許すアプリでは互換性検証が必要。ライブラリが書き換え可能なら回避され得る点に注意。

- Non-Executable Stack（noexecstack）
  - スタック実行不可は現在ほとんどの環境でデフォルトだが、明示的にリンカフラグで保証できる。

- Stack Clash / -fstack-clash-protection
  - ガードページを回避する「スタッククラッシュ」を防ぐため、大きなスタック確保をページ単位で触るコードに変換し、ガードページを確実に踏ませる。攻撃の成功確率を下げる強力な対策。

- コード再利用攻撃対策（ROP/JOP）
  - ハードウェア支援の CET（Control-flow Enforcement Technology）を使って、IBT（Indirect Branch Tracking） と Shadow Stack を有効化可能。Clang では -fcf-protection=return|branch|full|none を指定。
    - return: Shadow Stack（RET 攻撃対策）
    - branch: Endbr（IBT、間接ジャンプ攻撃対策）
    - full: 両方有効

- 投機的実行（Speculative）攻撃向け対策
  - Speculative Load Hardening（SLH）などのコンパイラ変換で投機的実行による情報漏洩を緩和。近年の脆弱性群に対する必須級のオプション。

- 制限と注意点
  - これらは単独で万能ではない。リンカ/環境/ファイル権限や実行環境（カーネルやCPUサポート）による制約があるため、複数対策を組み合わせること、性能影響を評価することが重要。

## 実践ポイント
- まずは CI に OpenSSF 推奨セットを追加して警告・ビルドテストを回す（性能測定は必須）。
- プラグインや dlopen を使うアプリは nodlopen の影響範囲を洗い出す。必要なら設計見直し（明示的なプラグイン API など）を検討。
- -D_FORTIFY_SOURCE=3 と -D_GLIBCXX_ASSERTIONS を有効化し、テストで動作とエラーを確認する（テストカバレッジは重要）。
- -fstack-clash-protection を導入して大きなスタック割当をする箇所（deep recursion、大きな自動変数）を見直す。
- CET（-fcf-protection=full）はハードウェア依存。対象プラットフォームでサポートされているか確認して段階的に有効化する。
- 日本のパッケージング（ディストリビューションパッケージ、コンテナ、組み込みイメージ）でもこれらのフラグを標準化すると、供給連鎖リスクを下げられる。

短時間で防御効果が得られるビルド時の「フラグ整備」は、小さな労力で現実的な安全性向上をもたらす。まずは CI に最低限のセットを入れて、影響範囲を測ることから始めよう。
