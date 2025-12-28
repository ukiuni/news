---
layout: post
title: "Python 3.15’s interpreter for Windows x86-64 should hopefully be 15% faster"
date: 2025-12-26T03:54:10.518Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fidget-spinner.github.io/posts/no-longer-sorry.html"
source_title: "Python 3.15’s interpreter for Windows x86-64 should hopefully be 15% faster"
source_id: 46384167
---

# Windows版CPythonが約15%速くなるかもしれない話 — 3.15で変わる“インタプリタの中身”

## 要約
Windows x86-64向けMSVCビルドで、インタプリタ実装を「tail-call（末尾呼び出し）方式」にすると pyperformance 上で約15% のジオメトリック平均向上が観測されたという報告。macOS AArch64 でも5%程度の改善が確認されている。

## この記事を読むべき理由
多くの日本の開発者はWindowsで開発・デプロイしており、CPythonの単体性能改善は日常的なレスポンス改善やCIコストの低減につながる。インタプリタの低レイヤ改善が、手元のアプリやライブラリにどう影響するかを理解しておくべきだからだ。

## 詳細解説
- 背景：Cで書かれたインタプリタには代表的に「switch-case」方式と、GCC/Clangが提供する「computed goto（labels-as-values）」方式がある。computed goto は理論上次命令ジャンプが1回で済み有利だが、現代のコンパイラ/CPUではその利点が縮小している。
- もう一つの手法が「call/tail-call threaded interpreter」。各バイトコードハンドラを関数にして、次ハンドラへ末尾呼び出しで遷移する方式。Cでは末尾呼び出し最適化が保証されなかったため現実的ではなかったが、Clang の `__attribute__((musttail))` のように「必ず末尾呼び出しにする」手段が登場して再注目されている。
- 元記事の報告：開発者は macOS AArch64（Xcode Clang）で約5% の改善、そして Windows x86-64（MSVC の実験的な内部ビルド）で約15% のジオ平均改善を観測した。計測は pyperformance ベンチで、ほとんどのベンチマークで改善が見られる一方、極端な落ち込みを示すベンチ（約60% 減）や大幅改善（約78% 増）といったアウトライアもある。
- 注意点：MSVC側の機能は実験的で、将来的に保持される保証はない。さらに、ローカルでのVisual Studio（記事は VS 2026 での確認）依存の結果であるため、公式リリース時に同等の効果が出るかは開発サイクル次第。

## 実践ポイント
- すぐ試したい場合：公式の Python 3.15 の Windows バイナリが出たら、まず既存の重要ワークロード（テストスイート、CI、ベンチ）で比較測定する。pyperformance や自前のプロファイルを回すこと。
- 自前ビルドを試す：興味があるならソースをチェックアウトして、該当のビルドフラグ／パッチを当てた MSVC 環境でビルドして試す（ただし実験的機能なので本番導入は注意）。
- リスク管理：ベンチの大部分で改善が見られても、特定のコードパスで逆効果になるケースがある。主要なサービスやライブラリで回帰テストを必ず行う。
- 継続的に情報収集：この変更は開発途中のため、Python の issue トラッカーや MSVC のドキュメント、関連するベンチ結果をフォローして、最終的な公式方針を確認する。
- 日本の現場への示唆：Windows サーバや開発環境が多い組織では、公式バイナリの更新で簡単に恩恵が得られる可能性が高い。CI時間短縮やレスポンス改善を数%単位で積み上げたいチームは注視すべき。

