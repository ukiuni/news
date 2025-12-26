---
layout: post
title: "Ruby 4.0.0 Released | Ruby"
date: 2025-12-26T03:56:05.123Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.ruby-lang.org/en/news/2025/12/25/ruby-4-0-0-released/"
source_title: "Ruby 4.0.0 Released | Ruby"
source_id: 438519320
---

# Ruby 4.0到来 — 「Ruby Box」と「ZJIT」で何が変わるのか？今すぐ試したい実践ポイント付き解説

## 要約
Ruby 4.0は「Ruby Box」（定義の分離）と「ZJIT」（新世代JIT）を柱に、Ractorの改善や言語・コアクラスの細かな変更を導入。パフォーマンスと安全性の両面で次の世代に踏み出します。

## この記事を読むべき理由
多くの日本企業・スタートアップが依存するRubyエコシステムにとって、テストの分離、並列実行の効率化、将来のJIT性能向上は重要課題です。CIやデプロイ、gem互換性の観点から早めに挙動を把握しておく価値があります。

## 詳細解説
- Ruby Box（実験機能）
  - 環境変数 RUBY_BOX=1 で有効化される実験的機能。Ruby::Box クラスにより、ロードされたクラス/モジュール、モンキーパッチ、グローバル／クラス変数、ネイティブ拡張などを「箱（box）」ごとに隔離できます。
  - 期待されるユースケース：モンキーパッチによるテスト汚染の防止、単一プロセス内でのブルーグリーン的な並列アプリ実行、依存関係の更新を局所的に評価するスモーク環境、将来的なパッケージAPI実装の下地。
  - 注意点：現状は実験機能で、APIや動作の安定性は今後変わる可能性があります。

- ZJIT（新しいJITコンパイラ）
  - YJITの次世代として開発されたJIT。内部でSSA中間表現を持ち、より大きなコンパイル単位を扱える設計でパフォーマンスの天井を上げることが狙いです。
  - ビルド時に Rust 1.85.0 以上が必要で、ビルドオプション --zjit を指定して有効化します。
  - 現状はインタプリタより高速だが、YJITほど成熟しておらず本番導入は慎重に。4.1で更なる改善が予定されています。

- Ractor（並行実行）の改善
  - 新しいクラス Ractor::Port によりメッセージ送受信周りの課題を解消。Ractor.shareable_proc で Proc の共有がしやすくなりました。
  - 内部データ構造の改善でグローバルロックの競合が減り、CPUキャッシュ競合も低減。3.0で実験導入されたRactorは近いうちに「実験」扱いを外す予定です。

- 言語・コアクラスの変更（抜粋）
  - nil.to_a の暗黙呼び出しが廃止される（**nil と同様の扱いに近づく）。
  - 行頭に来る論理二項演算子（||, &&, and, or）は行継続として前行とつながる扱いに。
  - Array#rfind / Array#find の追加で走査処理が効率化。
  - Binding の番号付きパラメータ周りの仕様変更と、numbered parameters（it 等）にアクセスするAPI追加。
  - Enumerator.produce に size オプションが追加（無限／有限のサイズ指定が可能）。
  - ArgumentError の表示改善など、デバッグ体験の向上も含まれます。

## 実践ポイント
- 環境構築
  - ZJITを試すなら Rust 1.85+ をインストールし、ソースから --zjit でビルドして試す。
    ```bash
    # bash
    rustup install 1.85.0
    ./configure --zjit
    make -j$(nproc)
    sudo make install
    ```
- Ruby Box を使ってみる
  - 簡単な確認：
    ```bash
    # bash
    RUBY_BOX=1 ruby -e "p defined?(Ruby::Box)"
    ```
  - テストスイートで一部ケースだけ Box 内で実行して、グローバル副作用が潰れるかを検証する運用を検討する（モンキーパッチ多用のライブラリがある場合に有効）。

- ZJITの評価方法
  - 標準的なベンチマーク（benchmark-ips、Railsベンチなど）でYJIT／ZJIT／インタプリタを比較。特にスループットとメモリ挙動を注視する。
  - 本番導入は控え、まずステージングで一定期間運用して挙動確認を。

- CI/ビルドの更新
  - ソースビルドを取り入れている場合、Rustの導入やビルドオプションの追加をCIに反映。gem/native拡張の互換性テストを自動化しておく。

- 互換性チェック
  - Array/Binding/Enumerator周りの変更は既存コードの微妙な挙動差を生む可能性があるため、主要なgemとアプリのテストを通して問題がないか確認する。

## 引用元
- タイトル: Ruby 4.0.0 Released | Ruby
- URL: https://www.ruby-lang.org/en/news/2025/12/25/ruby-4-0-0-released/
