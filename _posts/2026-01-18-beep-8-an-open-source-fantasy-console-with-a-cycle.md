---
layout: post
title: "BEEP-8: An open-source fantasy console with a cycle-accurate ARM emulator written entirely in JavaScript - BEEP-8：JavaScriptで書かれたサイクル精度ARMエミュレータを備えたオープンソースのファンタジーコンソール"
date: 2026-01-18T09:13:17.791Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/beep8/beep8-sdk"
source_title: "GitHub - beep8/beep8-sdk: SDK for developing games and tools for the BEEP-8 fantasy console."
source_id: 425113447
excerpt: "ブラウザで動くJS製サイクル精度ARMでC/C++ゲームを60fps配信"
image: "https://opengraph.githubassets.com/51323c26d244a669d57073be9fe86526ebcac859c8d754aea67d95f5b72761b7/beep8/beep8-sdk"
---

# BEEP-8: An open-source fantasy console with a cycle-accurate ARM emulator written entirely in JavaScript - BEEP-8：JavaScriptで書かれたサイクル精度ARMエミュレータを備えたオープンソースのファンタジーコンソール

ブラウザで動く“本格ARM”レトロ機 — BEEP-8で作って遊んで世界に公開する方法

## 要約
BEEP-8は、JavaScript製のサイクル精度ARMエミュレータを核にしたオープンソースのファンタジーコンソール。C/C++でネイティブに近い感覚でゲームを作り、ブラウザで60fpsで動かし、簡単に配布できるプラットフォームです。

## この記事を読むべき理由
日本のモバイル中心のゲーム文化やインディー開発コミュニティに最適──App Store審査不要でブラウザ配信でき、縦長画面最適化や低リソース制約が学習とプロトタイピングに役立ちます。レトロ表現と本格的なC/C++開発の両立は教育・ハッカソン・ポートフォリオ制作で魅力的です。

## 詳細解説
- コア設計：BEEP-8はARM v4を「固定4MHz」でサイクル精度エミュレーション。エミュレータは完全にJavaScriptで動作するため、ブラウザだけで同一挙動を得られます。
- 開発言語とツールチェーン：C/C++（C++20対応）で開発。リポジトリにプラットフォーム別の事前ビルド済みGNU ARM GCCが同梱され、特にWSL2を使えばWindows上でもUNIXライクな開発が容易です。
- ハードウェアモデル（仮想）：メインRAM 1MB、VRAM 128KB（4bpp、512×512レイアウトをBG/spriteで共有）、表示は128×240ピクセル・16色パレット。ROMサイズ上限は1,024KB。これらの制約が「制限を活かす設計」を促します。
- 画面・音声：PPU（Pixel Processing Unit）で背景・スプライト・図形を描画。APUはNamco C30風の音源を模した8ch合成でレトロな音作りが可能。
- 入出力とOS：キーボード／タッチ／マウス対応のHIF、60Hz駆動のタイマ、軽量RTOS（b8OS）を内蔵。b8OSはスレッド・セマフォ・割り込み・簡易ファイルシステムを提供しますが、多くの場合ゲームロジックに専念できます。
- 配布と実行：ゲームは単一の.b8 ROMにパッケージングされ、公式ポータル（https://beep8.org）にアップロードして世界中に共有可能。ブラウザベースなのでiPhone等でもApp Storeを介さず配信できます。
- 開発体験：サンプルプロジェクト（hello, pico8_example等）やPICO‑8互換のC/C++ライブラリが用意され、低レイヤーAPIへ直接アクセスするか、互換ライブラリで手早く作るか選べます。画像はpng2cでC配列に変換され、run.sh / run.batでビルド→ROM生成→ブラウザ起動が自動化されます。
- 実行性能：WebGLとシェーダ最適化によりPC・スマホで安定した60fpsを保証。縦長スマホ表示に最適化されている点がモバイル中心の日本市場にフィットします。

## 実践ポイント
- まず試す：ブラウザで即プレイできる公式ポータルを試す（https://beep8.org）。自分の端末で動作確認してみるのが一番早い。
- リポジトリをクローンしてサンプルを起動（macOS/Linux推奨、WindowsはWSL2推奨）：

```bash
# リポジトリ取得とサンプル起動例
git clone https://github.com/beep8/beep8-sdk.git
cd beep8-sdk/sdk/app/pico8_example
./run.sh
```

- macOSでブラウザからダウンロードしたアーカイブを使う場合はGatekeeper除去：

```bash
# macOSでのGatekeeper例
xattr -r -d com.apple.quarantine <extracted-folder>
```

- 開発フロー：画像は data/import/ に置くと自動で png2c が C++ ソースに変換される。run.sh / run.bat がビルド→ROM生成→ブラウザ起動を実行し、右ペインにデバッグ出力（printf）が表示されます。
- 学習用途に最適：ARM命令・メモリ制約・低レイヤAPIを学びつつ、PICO‑8互換APIで速くプロトタイプを作れる。大学の授業や社内ワークショップ、ハッカソンにも向きます。
- 配布戦略：ROMは1ファイルで配布可能。公式ポータルにアップするだけで世界中の端末で遊べるため、スマホ向けのプロモや簡易ベータ公開に便利です。
- 制約を逆手に取る：128×240・16色・VRAM制約はデザインの強制力になる。小さなリソースでの表現力を磨く良い訓練になります。

短時間で結果を出せる一方、ARMサイクル精度やRTOS相互作用など深掘りできる要素も豊富です。まずは公式サイトで動作を確認し、pico8_exampleをビルドして「自分のゲーム」をブラウザで公開してみてください。
