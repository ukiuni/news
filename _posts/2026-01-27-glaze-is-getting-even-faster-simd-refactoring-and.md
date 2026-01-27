---
layout: post
title: "Glaze is getting even faster – SIMD refactoring and crazy whitespace skipping in the works - Glazeがさらに高速化へ：SIMDリファクタリングと高速な空白スキップの取り組み"
date: 2026-01-27T21:43:35.061Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/stephenberry/glaze/pull/2270"
source_title: "SIMD Optimizations and can_error checks by stephenberry · Pull Request #2270 · stephenberry/glaze · GitHub"
source_id: 415938716
excerpt: "GlazeがSIMD刷新とskip_ws最適化、can_errorでJSON処理を高速化"
image: "https://opengraph.githubassets.com/eb9a7a68fdf2e5be8d68fa83c50b413fdd9bafcafbef99727037081dc84f7be9/stephenberry/glaze/pull/2270"
---

# Glaze is getting even faster – SIMD refactoring and crazy whitespace skipping in the works - Glazeがさらに高速化へ：SIMDリファクタリングと高速な空白スキップの取り組み
驚くほど速くなるJSON処理──SIMDを整理してNEON/SSE2にも対応、さらにコンパイル時の失敗判定で不要なチェックを省略

## 要約
SIMD処理のリファクタリングでAVX2/SSE2/NEONごとの最適化パスを整理・追加し、さらに書き出し処理で「失敗し得ない型」をコンパイル時に判別してランタイムチェックを省く最適化（can_error）を導入。空白スキップ（skip_ws）周りもSWAR実装でベンチを詰めています。

## この記事を読むべき理由
JSONシリアライザ／パーサは多くのサービスでホットパスになりがちで、わずかな高速化がコスト削減やレスポンス向上に直結します。特に日本ではARM（NEON）ベースのサーバ／モバイル端末が多く、今回のNEON対応とコンパイル時最適化は即効性のある改善です。

## 詳細解説
- SIMDの整理
  - 共通インターフェースを simd/simd.hpp に抽出し、ISAごとに avx.hpp / sse.hpp / neon.hpp を用意。設計が分かれメンテしやすくなりました。
  - AVX2（既存、32バイト）、SSE2（16バイト）、NEON（16バイト＋64バイトの幅を想定）の各パスを追加／改良。
  - AVX2の文字列エスケープ検出を、従来の「SWARをYMMに埋める」方式から direct cmpeq / movemask を使う方式に書き換え→マスク取得が単純で高速化。
  - エスケープ処理の書き込みロジックを write_escape ラムダに統一し重複削除。

- 空白スキップ（skip_ws）／SWAR
  - SWAR（同時に複数バイトをスカラーで扱うテクニック）によるportable実装とベンチ強化。特定サイズ（たとえば8バイト付近）の性能バグ修正が入っています。

- 書き出し最適化（can_error）
  - to<JSON, T> 特殊化に static constexpr bool can_error を追加し、「書き込みで失敗し得ない型」（bool、数値、文字列、enum、bitset、flags、null、nullable 等）を型レベルでマーク。
  - オブジェクトの直列化で全フィールドが can_error==false なら ctx.error チェックや ensure_space 呼び出しをスキップ。これで分岐・関数コールを減らせます。
  - 配列パディング情報（array_padding_known）を拡張して、固定パディングが計算可能ならさらに最適化。

- 共通ユーティリティとビルド調整
  - util/bit.hpp を作成し、countr_zero / countl_zero / int_log2 を集約。SIMDヘッダはこれを直接使うように。
  - __has_builtin のチェック修正、ドキュメント（README・optimizing-performance.md）更新、GLZ_DISABLE_SIMD オプションの記載あり。

- 開発／コラボの状況
  - ベンチ・テストが継続中で一部コミットでCIが失敗することもあるが、コントリビュータ間でベンチ比較やリベース調整が進んでいます。AVX-512は議論中（スループット／サーマル等のトレードオフで慎重な姿勢）。

## 実践ポイント
- まず自分のワークロードでプロファイル：SIMD有無で実測を取る（GLZ_DISABLE_SIMDで切替可能）。
- ARM環境（モバイル／組込み）ではNEONビルドを試すと効果が出やすい。
- カスタムシリアライザを書く場合、can_error相当の型レベル情報を使えばランタイムチェック削減が可能。
- util/bit.hpp 相当のビットユーティリティ（countr_zero 等）は自前で持つより統一したものを使うと保守が楽。
- リポジトリの skip_ws ベンチマークを動かして、自分の入力分布での影響を確認する（特に短い入力や境界サイズで挙動が変わることあり）。
- AVX-512は恩恵大だがハードウェア依存／トレードオフあり。広い互換性を優先するならAVX2/SSE2/NEONの強化を歓迎。

短く言えば、Glazeは「SIMDの土台を整理して多様なCPUで効率的に動くようにした」＋「コンパイル時情報で無駄なチェックを落とす」ことで、実運用での高速化を狙っているアップデートです。興味があればリポジトリでベンチを回して自分の環境向け効果を確かめてください。
