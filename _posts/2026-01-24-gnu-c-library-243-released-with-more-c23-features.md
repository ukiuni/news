---
layout: post
title: "GNU C Library 2.43 released with more C23 features, mseal & openat2 functions - GNU Cライブラリ 2.43：C23機能強化、mseal と openat2 をサポート"
date: 2026-01-24T01:58:02.023Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.phoronix.com/news/GNU-C-Library-Glibc-2.43"
source_title: "GNU C Library 2.43 Released With More C23 Features, mseal &amp; openat2 Functions - Phoronix"
source_id: 420330725
excerpt: "glibc 2.43がC23機能とmseal・openat2を追加、性能とセキュリティを強化"
image: "https://www.phoronix.net/image.php?id=2023&image=gnu"
---

# GNU C Library 2.43 released with more C23 features, mseal & openat2 functions - GNU Cライブラリ 2.43：C23機能強化、mseal と openat2 をサポート
次世代C標準とセキュリティ機能で高速化＆堅牢化──今すぐ注目したいglibcアップデート

## 要約
glibc 2.43（2026年1月リリース）はC23の新機能追加、Linux向けのmseal／openat2サポート、数学ライブラリ最適化、Clangでの実験的ビルド対応などを含む大規模アップデートです。性能改善とセキュリティ強化が同時に進められています。

## この記事を読むべき理由
glibcはほぼ全てのC/C++アプリや多くの言語ランタイムが依存する基盤ライブラリで、日本のサーバ／組込み／デスクトップ環境にも直接影響します。今回の変更は性能向上やセキュリティ・互換性に直結するため、開発者・運用者は把握しておくべきです。

## 詳細解説
- C23機能強化：free_sized, free_aligned_sized, memset_explicit, memalignment などの新APIを追加し、一部既存関数も変更。時間基準のオプション（TIME_MONOTONIC / TIME_ACTIVE / TIME_THREAD_ACTIVE）をサポートし、時間計測やスレッド動作の精密制御が容易になります。
- セキュリティ系API：mseal（メモリマッピングを実行時に封印し権限変更や解除・リサイズを防ぐ）と openat2（openatの拡張、より細かいファイルオープン制御）をLinuxでサポート。コンテナやサンドボックスでの堅牢化に有用です。
- コンパイラ／プラットフォーム：Clang 18以上での実験的ビルド対応（AArch64/x86_64）。将来的にLLVMツールチェーンでの正式サポートが期待できます。
- 数学関数とFMA最適化：CORE-MATH由来のacosh/asinh/atanh/erf/erfc/lgamma/tgamma等の最適化に加え、fma系やfrexp系の高速化。特にFMA実装は大幅に高速化され、AMD Zen向けの改善も含むため科学計算や機械学習で恩恵が出ます。
- メモリ割当の挙動：AArch64でmallocがデフォルトで2MBの透明HugeTLBを有効化。大きなヒープ割当でTLB圧縮により性能向上が期待されますが、ページサイズ依存の挙動変化に注意が必要です。
- 互換性・その他：Intel Nova/Wildcat LakeのCPU検出追加、Unicode 17.0対応（日本語文字や絵文字処理の最新化）。リリースは当初予定を前倒しして提供されました。

## 実践ポイント
- 自分のディストリでglibc 2.43が提供されたら、テスト環境でアプリケーションを回して互換性と性能差を確認する。
- コンテナやサンドボックスではmsealやopenat2を活用して攻撃面を減らす（カーネルサポート状況も確認）。
- 科学計算・数値処理を行うサービスはFMA最適化の恩恵を受ける可能性があるためベンチを実施する。
- AArch64環境ではmallocのHugeTLB挙動を検証し、メモリ割当チューニングを見直す。
- 開発者はC23の新APIを学び、必要ならコードの移行を検討する。Unicode 17対応は日本語表示や正規化で有利。

---  
原文情報：Phoronix「GNU C Library 2.43 Released With More C23 Features, mseal & openat2 Functions」（2026年1月）。詳細やソースはinfo-gnuメーリングリスト／公式配布を参照。
