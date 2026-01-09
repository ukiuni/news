---
layout: post
title: "My C++ compiler just wrote its own fan-fiction (inference at compile-time) - C++コンパイラが自作のファンフィクションを書いた（コンパイル時推論）"
date: 2026-01-09T09:13:14.247Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/erodola/bigram-metacpp"
source_title: "GitHub - erodola/bigram-metacpp: A tiny LM that does inference entirely at compile time"
source_id: 468579051
excerpt: "C++のコンパイル時に言語モデルを走らせ、ビルドごとに異なる名前をバイナリに焼き込む実験"
image: "https://opengraph.githubassets.com/f2657cabba06fe22c54ad2ea45fa98bed2850259fa4698a37aa13cf7b539c785/erodola/bigram-metacpp"
---

# My C++ compiler just wrote its own fan-fiction (inference at compile-time) - C++コンパイラが自作のファンフィクションを書いた（コンパイル時推論）
コンパイルするたびに「名前」を生み出すC++魔術──コンパイラが推論エンジンになったら何が起きるか？

## 要約
C++のconstexprとテンプレートメタプログラミングだけで、ビグラム（文字レベルのマルコフ連鎖）による言語モデルの推論をコンパイル時に実行し、生成した文字列をバイナリに焼き込む実験リポジトリです。ランダム種はビルド時のマクロ（__TIME__/__DATE__）から作られ、実行時の生成コストはゼロです。

## この記事を読むべき理由
- 「コンパイル時に計算を終わらせる」という発想は、組み込み・リソース制約環境や確定的ビルドに関心ある日本のエンジニアにとって新たな視点を与えます。  
- C++のconstexprやテンプレートの可能性を学べ、実務でのパフォーマンス最適化やデプロイ前処理のアイデア源になります。

## 詳細解説
- モデル構造：文字単位のビグラム（2-gram）マルコフモデル。遷移確率は外部で学習して静的なconstexpr行列にエンコードされています。  
- コンパイル時乱数：__TIME__ と __DATE__ をFNV-1aでハッシュしてシードを作り、constexpr実装のXorshift32で疑似乱数を生成します。コンパイラは決定論的なので、同じビルド時刻なら同じ出力、ビルドタイミングを変えれば別の出力が埋め込まれます。  
- サンプリング：逆変換法（Inverse Transform Sampling）のconstexpr実装で、現在文字の確率分布から次の文字を選びます。  
- ベーキング（焼き込み）：NameGenerator構造体がマルコフ連鎖を反復し、終端文字（'.'）か最大長に達するまで続け、生成した文字列をstatic constexprな定数としてデータセグメントに埋め込みます。結果としてランタイムの生成コストはゼロ。  
- 実行と確認：実行ファイルの文字列をstringsやImHexで調べると、コンパイル時に決まった生成文字列が入っています。  
- 互換性と制約：リポジトリはMSVC (cl.exe) での動作確認のみ。C++17のconstexprとテンプレート機能に依存するため、GCC/Clangでも理論的には動くがテンプレート深さやconstexpr評価の制限に引っかかる可能性があります。大規模モデルには向かない（コンパイル時間・コンパイルリソースが急増）。

このプロジェクトは実用性より「コンパイラ自身が計算を完了して結果を含めて配布する」という概念実証（proof-of-concept）で、C++の計算可能性とツールチェーンを再発見させるものです。

## 実践ポイント
- 試す：リポジトリをクローンしてMSVCでコンパイルするのが確実。README通り its.cpp をビルドしてみる。生成はビルドごとに変わります。  
  ```cpp
  // Inference happens here. If you wait one second and recompile,
  // the binary will contain a different name.
  static constexpr NameGenerator<15> result(seed, T);
  int main() {
      // Zero computation happens here. It just prints a constant string.
      std::cout << " Generated Name: " << result.name << std::endl;
  }
  ```
- バイナリ確認：生成文字列は実行時に計算されないため、strings ./binary や ImHex で直接確認できる。  
- 実用化のヒント：組み込み系で頻出する「ビルド時に決められる定数」をより多く焼き込む設計に応用できる。起動時の初期化コスト削減やファームウェアの定型データ埋め込みに役立つ可能性がある。  
- 拡張：遷移行列を外部で訓練して埋め込めば、出力の性質を変えられる。ただしモデル規模を増やすとコンパイル負荷が急増する点に注意。  
- 移植性対策：GCC/Clangで試す場合、テンプレート深度やconstexpr評価の制限に注意してコンパイラフラグを調整（環境依存）するか、モデルを小さくして試す。

最後に：実用性は限定的でも、工具としての「コンパイラ」を再解釈する面白いデモです。C++の深淵を覗きたい人、コンパイル時処理を業務に活かしたい人は一度コードを覗いてみてください。リポジトリ： https://github.com/erodola/bigram-metacpp
