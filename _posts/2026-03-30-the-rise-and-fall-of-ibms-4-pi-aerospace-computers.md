---
layout: post
title: "The rise and fall of IBM's 4 Pi aerospace computers: an illustrated history - IBMの4 Pi航空宇宙コンピュータの栄枯史（写真で見る歴史）"
date: 2026-03-30T00:33:00.374Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://www.righto.com/2026/03/ibm-4-pi-computer-history.html"
source_title: "The rise and fall of IBM's 4 Pi aerospace computers: an illustrated history"
source_id: 748862006
excerpt: "スペースシャトルや戦闘機を支えたIBM 4π系コンピュータの栄枯と設計教訓を写真で辿る"
---

# The rise and fall of IBM's 4 Pi aerospace computers: an illustrated history - IBMの4 Pi航空宇宙コンピュータの栄枯史（写真で見る歴史）
スペースシャトルや戦闘機を支えた「ブリーフケース級」コンピュータの知られざる物語

## 要約
IBMのSystem/4 Piは1960〜80年代に軍用・宇宙用で広く使われた小型高信頼コンピュータ群で、冗長化や放射線耐性を重視した設計で一時代を築いたが、技術進化や運用問題で姿を消した。

## この記事を読むべき理由
Space ShuttleやSkylab、F-4など日本にもゆかりのある機材で使われた実例から、組込み・航空宇宙向け設計（冗長化、コアメモリ、I/O構成、マイクロコード）の基本と教訓を学べるため。レトロPC好きや組込み初学者にも入門になる話題です。

## 詳細解説
- 背景：IBM System/360の発想を空間（球）に拡張したのがSystem/$4\pi$（$4\pi$は球全体の立体角を示す）で、1967年ごろに登場。狭い筐体で高信頼を求められる航空宇宙用途に最適化された家族（TC/CP/EP → 後のAdvanced AP/SP/CC/ML）を形成。
- 初代（TC/CP/EP）：
  - TC（Tactical）：8–64KBの磁気コアメモリ、8ビットバスだが16/32ビット語長の設計。例：Skylabの姿勢制御で使用。コアは電源断でも保持され放射線耐性あり。
  - CP（Customized Processor）：36ビット幅メモリバス、オプションでマイクロコード化、豊富なI/Oライン。F-111やEA-6Bなど兵器で採用。
  - EP（Extended Performance）：System/360互換の32ビット、複雑命令をマイクロコードで実装。マルチプロセッサ版も存在。
- Advanced System/4 Pi（AP系が中心）：
  - MSIや高速コア採用で小型高速化。AP-101系はSpace Shuttle（AP-101B）で4台冗長＋1台ホットスタンバイの構成で飛行制御を担当。
  - 一部は軍の標準命令セット（MIL-STD-1750A）やJOVIALでの開発をサポート。日本でもF-4などに搭載例あり。
- 実装技術：TTLフラットパックICを“ページ”と呼ぶ多層基板に密に配置。コアメモリスタックや専用I/Oプロセッサ（IOP）で入出力を分離しリアルタイム性を確保。
- 成功と限界：高信頼・リアルタイム機能で多数採用された一方、コアメモリやSSI時代の制約、運用上の信頼性問題（例：一部機種の故障多発）や新技術への置換で徐々に衰退。

## 実践ポイント
- 冗長化設計：4-of-5のような多重化（Votingやホットスタンバイ）は現代の組込み冗長設計にも直結する。
- ハードウェア／ソフトの分離：IOPや専用I/Oチャネルは負荷分離の有効なパターン。
- レトロハード観察：コアメモリやフラットパック基板から学べる物理実装の工夫（冷却・振動対策など）は組込み設計の教科書的資料。
- 参考行動：Ken Shirriffらの写真・分解記事やオークション出品写真を探して実機観察、MIL-STD-1750AやJOVIALの資料を読んで当時のソフト実装を追うと学びが深まる。
