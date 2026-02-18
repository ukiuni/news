---
layout: post
title: "Ladybird: Closing this as we are no longer pursuing Swift adoption - Ladybird: Swift採用を断念してこのIssueを閉じます"
date: 2026-02-18T23:35:20.936Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/LadybirdBrowser/ladybird/issues/933"
source_title: "Swift 6.0 Blockers · Issue #933 · LadybirdBrowser/ladybird · GitHub"
source_id: 47067678
excerpt: "LadybirdがSwift導入断念、C++相互運用の致命的課題と実践対策を解説"
image: "https://opengraph.githubassets.com/fbdd74fc323879362e6ed426856dcd8f810f76831a92854e9434150159641937/LadybirdBrowser/ladybird/issues/933"
---

# Ladybird: Closing this as we are no longer pursuing Swift adoption - Ladybird: Swift採用を断念してこのIssueを閉じます
LadybirdがSwift採用から撤退——技術的障壁の全貌と日本の現場で気をつけること

## 要約
オープンソースブラウザ「Ladybird」はSwift 6.0への本格移行を断念しました。原因はSwift/LLVMやC++相互運用（cxx-interop）、libstdc++、CMake周りなど多岐にわたる未解決の技術的ブロッカーです。

## この記事を読むべき理由
ブラウザやネイティブアプリの言語選定・FFI設計に関わる開発者なら、SwiftとC++を組み合わせる際の現実的な落とし穴と回避策を知っておくべきです。特に日本の開発環境（Ubuntu 24.04やmacOS、CMake利用）にも直接影響します。

## 詳細解説
- 根本問題群：Swift本体（Swift/LLVM）とClang、libstdc++、CMake、SwiftのC++相互運用レイヤーで複数の未解決バグや互換性問題が連鎖。結果としてLadybirdは「実運用レベルでの採用」が困難と判断しました。
- 代表的な障害：
  - LLVMのアサーション付きビルドが特定のClang ICEを含むため、Swiftのスナップショット（アサート有効）ではビルドできない。
  - Swiftのcxx-interopでOptional<CxxType>やswift::String等の受け渡しが正しく扱えない（ABI不一致、クラッシュ）。
  - libstdc++-13以降の<header>（特に <chrono> や <execution>）でモジュールマップや循環依存が発生し、Ubuntu 24.04環境で問題。
  - SWIFT_UNSAFE_REFERENCEやビットフィールド周りでコンパイラ/検証器がクラッシュするケース。
  - CMake + Swift環境でのデプロイターゲットやinstall_name_dirの設定差異がビルド/実行時に悪影響。
- Ladybird特有の問題：AKライブラリ（独自のC++型群）をSwift側で期待通りに扱えず、デバッグビルドでfrontendが落ちる、名前空間解決でクラッシュする等の実装上の相互運用課題。
- 一時的回避策（抜粋）：Swiftをアサート無しでビルド、macOSでビルド・実行、Optionalを使わない（配列やheap化で代替）、libstdcxx.hから<execution>をコメントアウト、テストはReleaseで動かす、String参照は明示的に名前空間を付ける等。

## 実践ポイント
- 当面の方針：プロジェクトでSwift↔C++の深い相互運用を前提にするなら、現状では「待ち」か「限定的採用」を推奨。重大なアップストリーム修正が来るまでは本番移行はリスクが高い。
- すぐできる対策：
  - Ubuntu 24.04環境ではlibc++を使う、またはlibstdc++のバージョンを下げる検討をする（Dockerで環境固定が現実的）。
  - Swiftのビルド/ツールチェーンを自前でビルドする場合、アサーション設定やCMakeのワークアラウンドを準備する。
  - FFI境界ではOptionalやスモールオブジェクトの直接返却を避け、明示的にheap化した型やstd::型で受け渡す。
  - ビルドシステム（CMake）で発生するフラグ問題はインポート直後にフラグを書き換えるなどの短期対応を用意する。
  - SourceKit-LSP/vscode-swift利用時はルートのcompile_commands.jsonを用意する（シンボリックリンクなど）。
- 情報収集：Swiftの該当issue群とLadybirdのレポートをウォッチして、主要なfix/バックポートが出たら再検討する。

短期的には「魅力的だが実運用にはまだ未熟」という結論です。Swiftを採用検討中のチームは、FFI設計とビルド環境の固定（DockerやmacOS CIの併用）を最優先で検討してください。
