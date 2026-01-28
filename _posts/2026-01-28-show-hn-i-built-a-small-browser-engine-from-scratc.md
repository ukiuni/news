---
layout: post
title: "Show HN: I built a small browser engine from scratch in C++ - C++で一から作った小さなブラウザエンジンを公開しました"
date: 2026-01-28T18:07:58.239Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/beginner-jhj/mini_browser"
source_title: "GitHub - beginner-jhj/mini_browser"
source_id: 46795540
excerpt: "C++/Qtで8週間で作られた学習用ブラウザエンジン、レンダリングの全工程をコードで追える"
image: "https://opengraph.githubassets.com/0908da08a00de5428c773c62b4d686ae5beb9c01f2504e46fc04e73cd24c0135/beginner-jhj/mini_browser"
---

# Show HN: I built a small browser engine from scratch in C++ - C++で一から作った小さなブラウザエンジンを公開しました
魅せるだけじゃない、仕組みが分かる。高校生が8週間で作った「ブラウザの中身」ハンズオン

## 要約
韓国の高校生がC++/Qtで8週間かけて作った学習用ブラウザエンジン。HTMLトークン化→DOM構築→CSS適用→レイアウト→描画の基本パイプラインを一通り実装しています。

## この記事を読むべき理由
ブラウザの内部動作（レンダリングパイプライン）を実際のコード構造で学べる稀有な教材。日本の学生や若手エンジニアが「仕組みを理解して手を動かす」入門プロジェクトとして最適です。

## 詳細解説
- 目的と性質：学習目的の小規模エンジンで、実運用は想定していませんが概念は本物のブラウザと同一です。  
- 技術スタック：C++17、Qt6（GUI/描画/ネットワーク）、CMakeでビルド。クロスプラットフォーム（macOS/Linux/Windows）対応を想定。  
- 実装した主要機能：  
  - HTMLパーサ（トークナイザ→TOKEN構造体）でタグ・テキストを分解  
  - DOMツリー（NODE）構築と属性管理  
  - CSSパーサ、CSSOM、スタイル計算（特異性・継承の簡易実装）  
  - レイアウトエンジン（ブロック/インライン、マージン・パディング計算、position対応）  
  - 描画（QtのQPainterで背景・ボーダー・テキスト・画像を順に描画）  
  - 画像キャッシュ、ナビゲーション（リンク・ヒストリ）、非同期画像読み込み  
- パイプライン（実装順）：
  1. HTML文字列 → HTML_TOKENIZER（トークナイズ）  
  2. TOKEN → HTML_PARSER（DOMツリー）  
  3. CSS_PARSER + CSSOM → apply_style()（計算済みスタイル）  
  4. layout_* 関数群で LAYOUT_BOX ツリー生成（座標・幅高さ算出）  
  5. Renderer が LAYOUT_BOX を描画して画面出力  
- サポートCSS例：color, font-size, display, position, margin/padding, border, background-color, text-align など主要プロパティをパース可能。  
- ソース構成：include/（html/, css/, gui/）と src/ に実装。READMEにビルド手順（CMake → make → ./browser）とテスト(cd test; ctest)が記載。

## 実践ポイント
- まず試す：リポジトリをクローンして README の手順でビルド → test_html_files を開いて動作確認。  
- 学び方：tokenizer → parser → style → layout → renderer の順にコードを追うと概念が掴みやすい。各モジュールは比較的分離されているので改造が容易。  
- 小さな拡張案：CSSプロパティ追加、簡易JavaScript呼び出しのダミー実装、フォント処理改善、レイアウトのフォールバック処理追加。  
- 教育利用：大学や社内勉強会で「ブラウザの内部入門」としてそのまま教材にできる。Qtを使うのでクロス環境での実演も簡単。  
- 日本市場との関連性：Webレンダリング理解はフロントエンド最適化、組み込み機器のUI、高速なネイティブWebビュー実装などに直結。若手エンジニアの学習投資として有用です。

元記事／ソース：GitHub - beginner-jhj/mini_browser（学習目的の小規模ブラウザエンジン、実運用向けではありません）
