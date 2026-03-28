---
layout: post
title: "OpenTTD for Windows NT RISC - OpenTTD の Windows NT RISC 移植"
date: 2026-03-28T14:06:33.088Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://virtuallyfun.com/2026/03/28/openttd-windows-nt-risc/"
source_title: "OpenTTD Windows NT RISC | Virtually Fun"
source_id: 1321352057
excerpt: "QEMUで実行可、LLM補助でVC互換化したOpenTTDをNT RISCで動かす方法"
---

# OpenTTD for Windows NT RISC - OpenTTD の Windows NT RISC 移植
レトロNTで遊ぶ新たな楽しみ — OpenTTDがMIPS/PowerPC/Alpha上で動作する理由と遊び方

## 要約
古典的なオープンソースの交通シミュレータOpenTTDが、Windows NTのRISC系（Alpha AXPに加えMIPS・PowerPC）で動作するビルドが公開された。Visual Cの古い互換性問題をLLMで補い、QEMU上で動かせる形になっている。

## この記事を読むべき理由
レトロPC・組込み系・仮想化に興味がある日本の技術者や趣味者にとって、実機がなくてもNT RISC環境で古いソフトを動かして解析・保存・遊べる好機だから。

## 詳細解説
- 背景: 以前、開発者 Nitton Åttiofyra が Alpha AXP 向けに OpenTTD を Windows NT 上で動くように移植していたが、そのビルドはVisual Studio 6.0依存で、MIPSやPowerPC向けのコンパイラ環境が揃わなかった。
- 技術的ポイント: 最新の寄稿では、古いVisual C（VC6相当）でしか通らないコードをさらに古いVisual C 4.0向けに互換対応させる作業が行われた。元作者が「LLM（大規模言語モデル）」をコード書き換え支援に使い、手作業で大幅改変することなくダウングレード対応を実現している。
- 実行環境: 実機不要で、QEMUなどのエミュレータを使えばWindows NT（RISC版）イメージ上でOpenTTDを起動できる。記事ではWindows NT MIPS上で動くスクリーンショット／実行例が示されている。

## 実践ポイント
- 試す手順（概要）: QEMUで該当RISCアーキテクチャの仮想マシンを作成 → Windows NT RISCのディスクイメージを用意 → 記事中のビルド（またはバイナリ）をダウンロードして実行。
- 注意点: Windows NTの商用バイナリやOSイメージの配布にはライセンス制約があるので、入手は自己責任で。QEMUの各アーキテクチャ用オプション（mips/ppc/alpha）に慣れておくとスムーズ。
- 応用: 同様の「古い開発環境向けコードのダウングレード」はLLMを補助に効率化できるため、レガシーソフトの保存・移植プロジェクトでの活用を検討すると良い。
