---
layout: post
title: "Resurrecting Crimsonland - Crimsonlandを復活させる"
date: 2026-02-02T05:11:02.305Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://banteg.xyz/posts/crimsonland/"
source_title: "banteg - Resurrecting Crimsonland"
source_id: 1294515402
excerpt: "GHIDRA×AIで実行ファイルを仕様化し挙動とバグまで復元した手法"
image: "https://banteg.xyz/posts/crimsonland/cover.avif"
---

# Resurrecting Crimsonland - Crimsonlandを復活させる
GHIDRA × AIで“バイナリから完全再現”したレトロ名作の舞台裏

## 要約
2003年のトップダウンシューター「Crimsonland」を、実行ファイルを“仕様”として逆コンパイル→再実装し、挙動やバグまで完全に再現したプロジェクトの記録。GHIDRA・Binary Ninja・WindbgとAIエージェントを組み合わせた手法が核。

## この記事を読むべき理由
ゲーム保存とリバースエンジニアリングの現場で実際に使える手法と落とし穴が具体的に学べるため。日本のインディー開発者やレトロゲーム保存に関心ある技術者に実践的な示唆を与えます。

## 詳細解説
- 対象と目的：対象はVisual Studio 2003でビルドされたDirectX 8.1版のcrimsonland.exe（grim.dllを含む）。著者の目標は「実行ファイルの振る舞いをソースで完全に再現する」こと（バグや1ピクセルの差まで再現）。
- 3つのルール：1) フルフィデリティ（GOGクラシック v1.9.93 を基準） 2) 推測禁止（名前付けや実装はデコンパイル／実行時証拠に基づく） 3) 既存ランタイムに依存しない（資産は流用可だがコードは一から）。
- 技術スタック：静的解析にGHIDRA（ヘッドレスでのパイプライン化）、Binary Ninja（自動探索）、ランタイム解析にWindbg／cdb。VMやBootcampで実機Windowsを用意して直接デバッグ。
- 実作業の流れ：GHIDRAで大規模デコンパイル→識別した関数/型をname_map.jsonへ記録→vtable（grim.dllの84メソッドがDirect3D等をラップ）をマッピングして描画／入力処理を解読→ランタイムで呼び出しを記録して実装と照合→再実装を繰り返す。AI（Codex/GPT-5.2）をエージェント化して定型作業を自動化し、数百コミットの反復を高速化。
- キモ：vtableと文字列リテラル、呼び出しパターン、構造体サイズなどを組み合わせて名前と型を推定し、逐次的に型情報を伝播させることで可読性を上げていく。サードパーティライブラリ（libpng等）は識別して除去／置換して解析を簡潔化。

## 実践ポイント
- ツールを揃える：まずGHIDRA（ヘッドレス化可）を中心に、Binary NinjaやWindbgを補助的に用意する。Windows実機でのランタイム解析は大きく効く。  
- ドキュメントを残す：name_map.jsonのような「住所→名前→根拠」を必ず残す。後で型が伝播する。
- vtableを重視：外部エンジンは間接呼び出しが多いので、vtableマッピングで描画/入力の意味が解ける。
- 自動化は助けになるが検証必須：AI／エージェントで命名やリタイピングを自動化しても、ランタイム検証で必ず裏取りすること。
- 法的・倫理的配慮：元バイナリの扱いと配布は権利者の許可が必要。保存・研究用途でも配慮を忘れずに。

短く言えば、古いゲームを「実行ファイルを仕様にする」方法で再現するには、静的解析＋ランタイム観察＋厳密なドキュメント化が鍵です。
