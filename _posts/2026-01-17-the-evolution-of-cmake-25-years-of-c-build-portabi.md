---
layout: post
title: "The Evolution of CMake: 25 Years of C++ Build Portability - Bill Hoffman - CppCon 2025 - CMakeの進化：C++ビルドの移植性が歩んだ25年 - Bill Hoffman（CppCon 2025）"
date: 2026-01-17T14:04:59.401Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=wPZV2hBNJmo"
source_title: "The Evolution of CMake: 25 Years of C++ Build Portability - Bill Hoffman - CppCon 2025 - YouTube"
source_id: 424612975
excerpt: "CMakeの25年に渡る進化で、ターゲット設計とクロスビルド高速化が即戦力に。"
image: "https://i.ytimg.com/vi/wPZV2hBNJmo/maxresdefault.jpg"
---

# The Evolution of CMake: 25 Years of C++ Build Portability - Bill Hoffman - CppCon 2025 - CMakeの進化：C++ビルドの移植性が歩んだ25年 - Bill Hoffman（CppCon 2025）
驚くほど変わった「CMake」の今 — 今こそ知っておきたいモダンCMake入門

## 要約
CppCon 2025でBill Hoffmanが語ったCMakeの25年の進化は、「ビルドの移植性」を軸に、レガシー慣習からターゲット中心のモダンな設計へ移行してきた流れを整理し、今後の改善点と現場で使える実践的な手法を示した。

## この記事を読むべき理由
C++開発でのビルド設定はプロジェクトの生産性と保守性を左右します。とくに日本の組み込み、ゲーム、金融といった現場ではクロスコンパイルや複数プラットフォーム対応が必須で、CMakeの最新知見を押さえておくことは即戦力になります。

## 詳細解説
- 歴史と背景  
  CMakeは元々クロスプラットフォームにMakefile（やVisual Studioプロジェクト）を生成するツールとして登場し、ここ25年で「ファイルベースの命令」→「ターゲット中心（target-based）」へパラダイムシフトしました。これにより、コンパイルオプションやリンク依存がグローバルなヘッダや変数ではなく、ターゲット単位で安全に管理できるようになりました。

- モダンCMakeの核となる考え方  
  - target_link_libraries と PUBLIC / PRIVATE / INTERFACE による依存性の可視化  
  - compile_features（C++標準や言語機能の要求）のターゲット指定  
  - インポートターゲット（外部ライブラリをターゲットとして扱う）による一貫性  
  これらは「設定を部品化して再利用・検証しやすくする」ための設計です。

- ビルド高速化と再現性  
  NinjaやCMakeのファイルAPI、Presets、キャッシュの改善、外部プロジェクト管理（FetchContent / ExternalProject）などにより、CIやローカルで高速かつ再現性のあるビルドが可能になってきました。

- エコシステムとの連携  
  vcpkgやConanといったパッケージマネージャー、IDE（VS Code/CLion）との統合、CTest/CPackによるテストと配布の自動化がCMakeを中心に回るケースが増えています。Bill Hoffmanの話は、この「CMakeがハブになる」役割を再確認するものでした。

- 今後の課題  
  大規模ビルドの並列化やキャッシュの汎用化、クロスコンパイルの簡素化（特に組み込み分野）、より良いIDE統合が引き続き重要です。

## 実践ポイント
すぐに使えるモダンCMakeの小技・移行ガイド：

- ターゲット志向に切り替える  
  ```cmake
  cmake_minimum_required(VERSION 3.15)
  project(MyApp LANGUAGES CXX)

  add_library(libfoo src/foo.cpp)
  target_include_directories(libfoo PUBLIC include)
  target_compile_features(libfoo PUBLIC cxx_std_17)

  add_executable(app src/main.cpp)
  target_link_libraries(app PRIVATE libfoo)
  ```
  - グローバルな変数や古い変数（INCLUDE_DIRECTORIESなど）を減らす。

- 依存管理はパッケージマネージャーかFetchContentで統一する  
  - vcpkgやConanをCIに組み込み、ローカルとCIで同じ依存解決を行う。
  - 小さめのライブラリならFetchContentを使ってソースレベルで取り込む（ただし大規模依存には注意）。

- Presets＆Toolchainで環境差を吸収する  
  - dev/prod/ci用のCMakePresets.jsonを用意し、クロスコンパイルや異なるビルドタイプを明確化する。
  - 組み込みやAndroidなどはtoolchainファイルで再現性を確保。

- ビルド速度を改善する  
  - Ninjaとccacheの併用、並列ビルド設定、不要な再生成を避ける工夫を行う。
  - CMakeのFile APIや他のキャッシュ戦略を活用する。

- CIへの組み込み例（概念）  
  - GitHub Actions / Azure PipelinesでPresetsを呼んでビルド→CTestでテスト→CPackでアーティファクト生成の流れを作る。

日本のプロジェクトで特に効くポイント：
- クロスコンパイル（ARM、Android、組み込み）用のtoolchainファイル整備は投資効果が高い。  
- レガシーMakefileや手作業のビルドスクリプトが残ると移植性が落ちるため、段階的にターゲット中心へ移行する。  
- 社内ライブラリはCMakeのインポートターゲット（Export/Install）を整備し、異なる部署間で共有しやすくする。

まとめ：CMakeは単なるビルドツールではなく「ビルドの設計思想」を持つプラットフォームです。25年の進化を踏まえ、今は「モダンCMake」の原則（ターゲット中心、再現性、パッケージ連携）をチームの標準にする好機です。
