---
layout: post
title: "How to Choose Colors for Your CLI Applications - CLIアプリの色をどう選ぶか"
date: 2026-01-29T15:54:29.695Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.xoria.org/terminal-colors/"
source_title: "How to Choose Colors for Your CLI Applications · Luna’s Blog"
source_id: 46810904
excerpt: "主要端末（Solarized等）で実測した、崩れない最小限のCLI配色とフォールバック法を解説。"
---

# How to Choose Colors for Your CLI Applications - CLIアプリの色をどう選ぶか
ターミナル配色で「見えない」や「読みづらい」を防ぐ実践ガイド

## 要約
CLI表示の色は端末テーマ次第で「美しい」から「読めない」まで変わる。元記事は主要テーマ（macOS Basic、Tango、Solarized 等）での可読性を調べ、実運用で安全に使える色の選び方を示す。

## この記事を読むべき理由
日本でも macOS、Ubuntu、WSL、各種カスタムテーマ（Solarized や Gruvbox 等）を使う開発者が多く、色が読めないとデバッグや日常作業に致命的なストレスが生じる。少ない手間で誰にでも読みやすいCLIが作れるため必読。

## 詳細解説
- 問題の本質：端末ごとに16色パレットや背景の明暗、"boldをbrightにする"設定が異なるため、開発者が選んだ色が別ユーザー環境で崩れる。
- 実測したテーマ例：
  - Basic（Terminal.app のデフォルト）：light/darkで色の可読性が大きく変わり、一部の色はほぼ使えない。
  - Tango（多くのLinuxディストロに近い）：Basicより改善するが、明るい黄色などはライトテーマで読めない。
  - Solarized：$L^{*}a^{*}b^{*}$ を元に設計され、ライト/ダークでアクセント色を共用できるが、16色パレットに丸めると明度対称性が壊れて「灰色化」や「見えなくなる」問題が出る。特に bright 系（br...）を使うとSolarizedユーザーで表示異常が出やすい。
- 太字（bold）問題：古い慣習で bold が bright 色として扱われる設定があり、太字によって色が予期せず明るく/薄くなる。
- 結論の要点：全32設定（通常/bright/太字など）から多くは互換性が悪く、広く安全に使えるのはごく一部。実運用向けには「多数のユーザー設定で壊れない色」に限定するべき。

## 実践ポイント
- テーマを跨いで必ずテストする：少なくとも macOS Terminal（Basic）、Ubuntu/Tango、Solarized（Light/Dark）で確認する。
- 色は限定する：端末間で安定する色（極端に明る/暗い bright 系や bold→bright に依存する表現は避ける）。
- フォールバックを用意：色が使えない場合は単純な強調（接頭句、アイコン、括弧）で代替表示する。
- Truecolor（24-bit）を使う場合でも、ユーザーがパレットを上書きしていると挙動が変わるので「ユーザーの設定を尊重」する実装にする。
- テスト自動化：CI やローカルのスクリプトで複数テーマをエミュレーションし、可読性チェックを入れる。
- ユーザー設定を許す：テーマ依存の配色を強制せず、設定で色を無効化できるようにする。

短く言うと、「美しい配色」より「多環境で読める配色」を優先し、最低限の色数でフォールバック設計を行えばユーザー体験が大幅に向上します。
