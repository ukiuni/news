---
layout: post
title: "Show HN: Iron-Wolf – Wolfenstein 3D source port in Rust - Rustで甦るWolfenstein 3Dのソースポート"
date: 2026-02-21T17:35:28.459Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/Ragnaroek/iron-wolf"
source_title: "GitHub - Ragnaroek/iron-wolf: wolf3D in Rust"
source_id: 47101890
excerpt: "Rust製のほぼ完全再現Wolfenstein3Dをブラウザで遊べ、モッド可能なオープンソース"
image: "https://opengraph.githubassets.com/cb59d1ed4d9a53490b0e778afe46a72921e165e5ab0e731bf1fa74acb38a3c08/Ragnaroek/iron-wolf"
---

# Show HN: Iron-Wolf – Wolfenstein 3D source port in Rust - Rustで甦るWolfenstein 3Dのソースポート
Rustで作られた名作FPSの“ほぼ完全再現”――ブラウザでも動くIron-Wolfを触ってみたくなる理由

## 要約
Iron-WolfはWolfenstein 3DをRustで再実装したオープンソースプロジェクトで、ピクセル再現とモッディング親和性を目標にしています。リポジトリにはシェアウェアのデータが同梱され、ブラウザ版（WASM）で遊べます。

## この記事を読むべき理由
レトロゲームのエンジン再実装は、ゲームレンダリング、入力処理、パフォーマンス最適化、そしてRustによる低レイヤ実装の学びどころ。日本のレトロゲーム・インディー開発者やRust学習者にとって実践的な教材になります。

## 詳細解説
- 実装言語はほぼ全てRust（リポジトリ表示で約99.5%）。レンダリングや入出力周りを安全性と性能の両立で書き直している点が特徴です。  
- 目標は「ピクセル忠実＋モッドしやすさ」。アセットやパッチ用フォルダ（assets / patch/w3d）を含み、改造や差し替えが想定されています。  
- 動作形態：ローカル実行用に run-sdl-shareware 等の実行ターゲットが用意されており、SDL系のバックエンドで動く想定です。さらに web フォルダ経由でWASMビルドをホストしており、ブラウザでプレイ可能（https://wolf.ironmule.dev/）。  
- データ：シェアウェア版のデータが testdata に同梱。フル版のゲームファイルを持っていればブラウザ版にアップロードして完全版を遊べます。  
- 設定：default_iw_config.toml をコピーして iw_config.toml として実行ファイル横に置くことで挙動を調整できます。  
- ライセンスはGPL-3.0。派生や配布の際はライセンス条件に注意が必要です。  
- リポジトリ構成（抜粋）: src / assets / web / benches / patch/w3d / testdata 等。多くのコミット履歴があり、学習・ベンチマーク対象としても価値があります。

## 実践ポイント
- まずはブラウザ版を試す：https://wolf.ironmule.dev/（フル版を遊ぶには自身のゲームファイルをアップロード）  
- ローカルで試す：リポジトリをクローンして README の run-sdl-shareware を実行（SDL環境が必要な場合あり）。  
- カスタム設定：default_iw_config.toml を iw_config.toml にコピーして調整。  
- 学習用途：レンダラー、入力処理、WASMビルド周りの実装を読むとRustでのゲームエンジン設計が学べる。  
- 配布・改変時はGPL-3.0の制約を確認すること。
