---
layout: post
title: "TruffleRuby 34: full Ruby 3.4 compatibility, up to 23% faster parsing, and a new Prism-based Ripper with 20x speedups - TruffleRuby 34：Ruby 3.4 完全互換、解析が最大23%高速化、PrismベースのRipperで20倍高速化"
date: 2026-04-15T02:27:39.547Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://truffleruby.dev/blog/truffleruby-34-is-released"
source_title: "TruffleRuby 34 is Released | TruffleRuby"
source_id: 1123282267
excerpt: "TruffleRuby 34：Ruby3.4互換、解析最大23%短縮、Ripperが20倍速"
---

# TruffleRuby 34: full Ruby 3.4 compatibility, up to 23% faster parsing, and a new Prism-based Ripper with 20x speedups - TruffleRuby 34：Ruby 3.4 完全互換、解析が最大23%高速化、PrismベースのRipperで20倍高速化

TruffleRuby 34で「互換性」と「起動／解析速度」が一気に強化された、実運用で試したくなるリリースです。

## 要約
TruffleRuby 34が公開され、Ruby 3.4の変更点をすべて実装。解析処理の最適化で最大23%高速化、RipperをPrismに置き換えて20〜40倍の高速化を実現しました。

## この記事を読むべき理由
RailsやRuby製ツールを多数運用する日本の開発現場では、テストや起動時間の短縮＝生産性向上に直結します。互換性が担保された上で高速化が進んだこのリリースは、実運用での移行検討価値が高いです。

## 詳細解説
- Ruby 3.4互換：Ruby本家の3.4チェンジログにある機能をすべて実装。例として改善されたスタックトレース、String#append_as_bytes、Array#fetch_values、Happy Eyeballs v2対応などが含まれます。
- Lazy method deserialization：TruffleRubyの解析フローは大きく3段階（ソース→Prismシリアライズ、Prismシリアライズ→Prism AST、Prism AST→TruffleRuby AST）ですが、従来は3番目のみ遅延していました。34では2番目（デシリアライズ）も遅延化し、結果としてパース時間が最大23%短縮されています。将来的には1番目もキャッシュして完全な遅延パースを目指します。
- Ripper → Prism：従来のriprper.cベース実装をやめ、Prism::Translation::Ripperへ移行。CRuby内部に強く依存する実装から脱却し、約77,000行の旧コード削減と、Ripper処理の20〜40倍高速化を達成。PrismはCRuby上でもRipperより約2.75倍高速で、ツール側でも採用が進んでいます（IRB, RDoc等）。将来的にRipperの廃止を検討する段階に来ています。
- ライブラリの配布変更：TruffleRuby上の純Ruby実装だった StringScanner が strscan gem に移行。gemを更新することで新機能をすぐ利用できます。
- エコシステム連携：RubyKaigiでの最適化発表など、並列ハッシュやスレッド周りの改善も継続的に行われています。

## 実践ポイント
- まずは既存アプリやテストスイートをTruffleRuby上で動かしてみる（互換性とパフォーマンスをチェック）。
- インストール例：
```bash
# rbenv / ruby-build / asdf の例
rbenv install truffleruby-34.0.0
# または
asdf install ruby truffleruby-34.0.0
```
- strscanを使っているならgemを更新してTruffleRuby上の改善を取り込む。
- 問題や互換性の違いはGitHubに報告、コミュニティ（Slack / Bluesky）で共有すると改善に貢献できます。

以上を踏まえ、まずは開発環境やCIでTruffleRuby 34を試し、起動・パース周りの体感改善を確かめてください。
