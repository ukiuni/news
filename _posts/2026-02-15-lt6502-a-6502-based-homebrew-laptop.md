---
layout: post
title: "LT6502: A 6502-based homebrew laptop - LT6502: 6502ベースの自作ラップトップ"
date: 2026-02-15T18:05:44.197Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/TechPaula/LT6502"
source_title: "GitHub - TechPaula/LT6502: A 6502 based laptop design"
source_id: 47025399
excerpt: "65C02・EhBASIC搭載の手のひらサイズ自作ラップトップ、CFや大容量バッテリで実機学習できる"
image: "https://opengraph.githubassets.com/fb612c0e2adb1a4ea2e7b3412ff10ca3ccbbb5a4c19c3f941db2cfd1df40a335/TechPaula/LT6502"
---

# LT6502: A 6502-based homebrew laptop - LT6502: 6502ベースの自作ラップトップ
8MHzで動く“レトロ×自作”ラップトップ――手のひらで楽しむ6502ベースのミニPCプロジェクト

## 要約
65C02を心臓に据えた自作ラップトップ設計で、EhBASICをROMに搭載、9インチ表示、CFストレージ、10000mAhバッテリ、USB‑C給電を備えた携帯型レトロPCプロジェクトです。

## この記事を読むべき理由
レトロCPUの学習用プラットフォームとして回路・ファーム・ケース設計まで一貫して公開されており、ハードウェア入門者や組込み／レトロ愛好家が実機で学べる実践的なリソースです。日本のメイカーズや教育現場でも応用しやすい構成です。

## 詳細解説
- ハード仕様（主要スペック）
  - CPU: 65C02 @ 8MHz
  - RAM: 約46KB（ゼロページ等含む）
  - ROM: EhBASIC（EhBASIC 2.22p5等）、eWozMon、ブート用ルーチン
  - 周辺: 65C22 VIA（タイマ/IO）、65C21（内蔵キーボード用）、FTDIシリアルコンソール
  - ディスプレイ: 標準9"（内蔵フォント＋簡易グラフィック）、RA8875/RA8889系のドライバ実験あり
  - ストレージ: Compact Flash
  - 電源: 10000mAhバッテリ、USB‑C給電/充電
  - その他: 内蔵キーボード、ビーパー、1スロットの内部拡張、CPLDでFTDI調整

- メモリマップ（要点）
  - RAM: 0x0000–0xBEAF（約48,816バイト）
  - ペリフェラル領域: 0xBE00–0xBFFF（周辺機器マッピング）
  - ROM: 0xC000–0xFFFF（約12KB、EhBASIC＋モニタ＋ブート）
  - ROM内訳: EhBASIC本体、拡張Wozモニタ、ブート/入出力/保存機能など

- ソフトウェア/機能
  - EhBASIC拡張コマンド（実用例）
    - BEEP, CIRCLE, LINE, PLOT, SQUARE, ELIPSE, CLS, COLOUR, MODE, DIR, LOAD, SAVE, OUTK, WOZMON など
  - Compact Flashに対するDIR/LOAD/SAVEサポート
  - キーボードはファーム統合済みで直接入力可能
  - 開発履歴（抜粋）: PCB到着→電源確認→ROM/RAM/コンソール動作→VIA/ACIA/キーボード統合→CF動作→ディスプレイ実験→ケース組立

- 現状と課題
  - 一部ディスプレイドライバ（LT7683）は失敗、RA8875は成功。将来的に10.1" RA8889 1024×600対応を試行予定。
  - キースキャンのバグ修正、拡張ボード作成が主なTODO。

- 参照: GitHubリポジトリには回路図（Schematics）、PCBデータ、ソースコードが公開（MITライセンス）。

## 実践ポイント
- まずはリポジトリをクローンしてREADME／schematicsを確認。PCB/ガーバー、パーツリストがあるので個人制作の足がかりになる。
- ソフトはEhBASICで手軽に遊べる。まずはCLS, PLOT, LINEなどで画面描画を試すと学習が早い。
- 日本での部品調達は秋月電子やスイッチサイエンス、海外はMouser/Aliexpressを併用。RA8875系の小型TFTは流通が安定している。
- バッテリ＋USB‑C設計はモバイル用途にも実用的。安全対策（保護回路）を忘れずに。
- 貢献方法: ドキュメントの日本語化、キースキャン修正、10.1"表示対応やケース改良などが参加しやすい領域。

リポジトリ（詳細設計・回路図・ソース）を見て、自作ラップトップを「学びながら作る」プロジェクトに挑戦してみてください。
