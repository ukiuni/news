---
layout: post
title: "river-classic: river 0.3.x forever - river-classic：river 0.3.x を守り続けるフォーク"
date: 2026-01-19T00:40:37.394Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/river/river-classic"
source_title: "river-classic: river 0.3.x forever"
source_id: 1040756228
excerpt: "慣れた操作感を守るリバー0.3系フォーク—外部レイアウトとランタイム設定で柔軟運用"
---

# river-classic: river 0.3.x forever - river-classic：river 0.3.x を守り続けるフォーク
魅力的な古典派タiling Wayland：使いやすさと保守性を重視した「river 0.3系」を使い続けたい人へ

## 要約
river-classic は Wayland 用の動的タイル型コンポジタ river 0.3 系を維持するフォークで、ランタイム設定・外部レイアウトジェネレータによる柔軟なウィンドウ配置が特徴。安定性を重視するユーザーやカスタム性を求める人に適している。

## この記事を読むべき理由
- 日本でもタイル型ウィンドウマネージャ（dwm/xmonad 系）が根強い人気を持つ中、Wayland 環境で「慣れた操作感」を維持したいなら注目すべきプロジェクトだから。
- 大きな API 変更（river 0.4系）を避け安定した環境を長く使いたい開発者・愛好家にとって、実運用での価値が高い。

## 詳細解説
- 何が特徴か：river-classic は画面上のウィンドウを自動的にタイル配置する「動的タイル型」コンポジタ。レイアウトのロジックをコンポジタ本体に埋め込まず、独自の Wayland プロトコルと外部プロセス（レイアウトジェネレータ）に委ねる設計になっている。これにより、自分でレイアウトを差し替えたりコミュニティ製のレイアウトを導入しやすい。
- レイアウトジェネレータ：公式の rivertile が基本例。C/Python のサンプルもあり、自作レイアウトの作成が容易。タグ（複数タグ割当可）でウィンドウ管理する点は X のタイル WM に近い発想。
- 設定方法：ランタイムで riverctl ツールを使ってキーバインド、レイアウト設定、入力デバイス設定などを変更可能。起動時は $XDG_CONFIG_HOME/river/init（未設定なら ~/.config/river/init）を読み、通常はこのスクリプトで riverctl を呼ぶ運用になる。
- 技術スタック：プロジェクトは主に Zig（ビルド設定等）で書かれており、wlroots ベースの Wayland コンポジタ。依存には zig、wlroots、wayland-protocols、xkbcommon、libevdev、pixman などがある。ライセンスは GPLv3（プロジェクト本体）。
- なぜフォークしたか：river 本体で大幅な破壊的変更（0.4 系）が予定されていたため、0.3 系の使い勝手をそのまま維持したいユーザー向けに fork が維持されている。

## 日本市場との関連性
- 日本の Linux ユーザーは軽量でキーボード中心の操作を好む傾向があり、タイル型 WM 需要は高い。Wayland 移行が進む中で、river-classic は「既存の操作感を残したまま Wayland を使いたい」層に刺さる選択肢。
- 日本語入力（IME）やロケール周りは Wayland 環境での設定が必要（fcitx5/ibus の Wayland 対応を確認）。さらに、Electron 系アプリや一部アプリが Wayland 未対応なら Xwayland オプションを有効にして運用することが現実的。
- ディストリビューション別のパッケージング（Arch/Ubuntu 等）を行う場合、依存バージョン（wlroots など）や Zig バージョンの指定に注意が必要。

## 実践ポイント
- 依存を揃えてビルドする（例）：

```bash
zig build -Doptimize=ReleaseSafe --prefix ~/.local install
```

- Xwayland が必要な場合はビルド時に -Dxwayland を追加する。
- 初めて試すときは既存のデスクトップ環境上にネストして起動（Wayland/X11 セッション内）して安全に挙動を確認する。
- カスタムレイアウトを試すには rivertile を使い、慣れたら独自のレイアウトジェネレータを書いてみる（リポジトリに C/Python の例あり）。
- 日本語入力は fcitx5/ibus の Wayland サポートを確認して設定。GUI アプリの互換性で困ったら Xwayland を有効化して対処。
- 長期運用向けに：river-classic は安定性重視のため、システムに組み込んで現場で使う場合はパッケージ化（配布方針に合わせたパッケージングガイド参照）を検討する。

短くまとめると、river-classic は「river 0.3 系の使い勝手を失わず Wayland を使いたい」日本のエンジニアやパワーユーザーにとって実用的で拡張性の高い選択肢。まずはネスト起動で試し、init スクリプトと rivertile を触って操作感を確かめると良い。
