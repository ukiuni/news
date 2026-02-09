---
layout: post
title: "UEFI Bindings for JavaScript - JavaScript向けUEFIバインディング"
date: 2026-02-09T14:25:44.619Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://codeberg.org/smnx/promethee"
source_title: "UEFI Bindings for JavaScript"
source_id: 46945348
excerpt: "DuktapeでUEFI上にJavaScriptを載せ、ブート時スクリプトをQEMUで即試作できるプロジェクト"
---

# UEFI Bindings for JavaScript - JavaScript向けUEFIバインディング
UEFIをJavaScriptで操る：ブート時に動くスクリプトでOS起動処理を試作する

## 要約
prometheeはUEFI環境でJavaScript（Duktapeランタイム）を動かし、script.jsをそのままブートローダ／ブート時スクリプトとして実行できるプロジェクト。QEMUで動作確認でき、UEFIサービスにJSから直接アクセスできる。

## この記事を読むべき理由
UEFIレイヤで「いつもの言語（JS）」が使えることで、ファームウェア周辺やブート処理の試作が格段に楽になる。日本の組込み／OS開発者やハードウェアプロトタイプを行う開発者にとって、低レイヤー実装の学習や高速プロトタイピングの新しい選択肢を提供する。

## 詳細解説
- 仕組み：prometheeはブートボリューム上のscript.jsを読み込み、UEFIサービス（SystemTable や BootServices）をJSから呼び出せるようにバインディングした実装。内部はCでランタイムや最小限のlibcスタブを用意し、Duktapeを埋め込む構成。
- 実行例：Graphics Output Protocolを探して矩形を塗りつぶすなど、UEFIのプロトコルをそのまま呼べる。READMEのサンプル：
```javascript
var gop = efi.SystemTable.BootServices.LocateProtocol(efi.guid.GraphicsOutput);
if (gop) {
  var red = { r: 255, g: 0, b: 0 };
  gop.Blt(red, 'EfiBltVideoFill', 0, 0, 50, 50, 200, 120, 0);
}
```
- ビルドと実行：依存取得スクリプト（./get-deps）→ make run でQEMU上のUEFI FATに \script.js を配置して実行可能。開発にはNode.jsがDuktape生成ツールで必要。
- 制約と注意点：実運用のファームウェアとしてはセキュリティ・信頼性の検討が必須（サンドボックスや署名など）。現状はプロトタイプ／学習用途が主。

## 実践ポイント
- 試す手順：リポジトリをクローン→ ./get-deps → make run（QEMU推奨、実機は注意）。
- まずは script.js を編集して画面描画や簡単なUEFIサービス呼び出しを試す（例：コンソール出力、タイマー、ファイル読み書き）。
- 学ぶべき基礎：UEFI仕様の基礎、Duktape の埋め込み方法、QEMUによる仮想環境でのファームウェアデバッグ方法。
- 日本市場での応用例：組込み機器のブート検証、カスタムリカバリツールのプロトタイプ、教育目的での低レイヤー学習教材作成。

興味があるならまずQEMU上で安全に動かし、UEFIサービスをJavaScriptから呼ぶ感触を掴むことを推奨する。
