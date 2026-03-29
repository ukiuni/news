---
layout: post
title: "A Verilog to Factorio Compiler and Simulator (Working RISC-V CPU) - VerilogをFactorioに変換するコンパイラ＆シミュレータ（動作するRISC‑V CPU）"
date: 2026-03-29T03:35:55.188Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ben-j-c/verilog2factorio"
source_title: "GitHub - ben-j-c/verilog2factorio · GitHub"
source_id: 47528853
excerpt: "VerilogをFactorioブループリントに変換しRISC‑Vを実機で可視化"
image: "https://opengraph.githubassets.com/c198e031c9de5f3f63eed10fc6a746b4ea2f477ba4b6ed27e84807c7c386f563/ben-j-c/verilog2factorio"
---

# A Verilog to Factorio Compiler and Simulator (Working RISC-V CPU) - VerilogをFactorioに変換するコンパイラ＆シミュレータ（動作するRISC‑V CPU）
究極の「回路をゲーム内で動かす」体験：VerilogからFactorioのブループリントを自動生成し、シミュレーションまでできるツール

## 要約
Verilogで書いた回路をFactorioのコンビネータ配置（ブループリント）へ変換し、ブラウザ/ローカルでシミュレーション・可視化できるオープンソースツール。RISC‑V（RV32IM）コアの実例も含まれ、設計→合成→配置→動作確認の流れを一気通貫で試せます。

## この記事を読むべき理由
ゲーム好きのハードウェア入門者や教育者、趣味で論理回路を試したいエンジニアにとって、視覚的かつインタラクティブにHDL設計を学べる新しいアプローチだからです。日本のコミュニティでもFactorioやRISC‑Vの興味は高く、教材やプロトタイピングの可能性が広がります。

## 詳細解説
- 何をするツールか：Verilogソースを受け取り、YosysでRTL解析・マップ→独自のマッピングでFactorioのコンビネータ表現（JSONブループリント）を生成。さらに内部シミュレータで波形や状態を追える。
- 実装とインターフェース：メインはRustで実装され、LuaとCLIのAPIを提供。Luaはオブジェクト指向風で手軽にデザイン生成・シミュレーションが可能。v2fというCLIでLuaスクリプトや中間のRTLマップを入力して出力（blueprint.json）を得られます。
- 合成フロー：YosysがRTL/ワードレベルの解析を担当。必要に応じてYosysスクリプト（rtl.ys／mapping.ys）を挟んで細かく制御可能。ただしブラウザへの完全搭載は大変なので、現状はバックエンド＋GUIの組合せやローカル／コンテナ実行が中心。
- 主要機能：Factorioへのブループリント生成、シミュレーション（DFFなどのトレース）、SVGによる物理配置レンダリング（コンビネータにホバーで信号確認可）、アニメーション配置、複雑設計のパーティショニング。
- 実例：RV32IMのRISC‑VコアをコンパイルしてFactorio上で動作させる例あり（hello_worldの出力など）。64x32 ROMや32bit ALUなどのサンプル配置も含まれ、教育・検証に使える。
- 開発環境：VSCode＋Dev Containers（推奨）、Docker、またはローカルでYosys等をビルド。READMEにビルド手順やenv設定、CLIオプションの説明あり。

## 実践ポイント
- まず試す：リポジトリをクローン→VSCodeでDev Containerを開くかDockerで環境構築→READMEのLuaフローの例を動かしてみる。
- 既存例を読み解く：examples/riscv_v2f_optimized や test_designs フォルダのVerilog＋Yosysスクリプトを参照して、どのように合成→マッピングされるかを学ぶ。
- ブループリント出力：v2f -i example.lua -o blueprint.json で生成したJSONをFactorio 2.0にインポートして実機で動作を確認。
- シミュレーションと可視化：SVG出力やシミュレータで波形・状態を確認し、設計のデバッグを迅速化する。
- 教材・ワークショップ利用：RISC‑VやHDL入門ワークショップで、実機感覚を持たせた教材として活用可能。ゲームとの親和性を生かして学習の敷居を下げられます。

リポジトリ：https://github.com/ben-j-c/verilog2factorio でソース・サンプルや詳しい手順を確認してみてください。
