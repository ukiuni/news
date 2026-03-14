---
layout: post
title: "Baochip-1x: What It Is, Why I'm Doing It Now and How It Came About - Baochip-1xとは何か、なぜ今それを行うのか、そしてその経緯"
date: 2026-03-14T12:09:41.241Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.crowdsupply.com/baochip/dabao/updates/what-it-is-why-im-doing-it-now-and-how-it-came-about"
source_title: "Dabao Evaluation Board for Baochip-1x - What It Is, Why I&#39;m Doing It Now, and How It Came About | Crowd Supply"
source_id: 47339219
excerpt: "22nmでMMU搭載のRISC‑V『Baochip‑1x』がARM依存を打破し安全な組込み基盤を提示"
image: "https://www.crowdsupply.com:80/img/6888/64958d03-a0dd-47ec-9d0e-8ef6dc126888/baochip1-silicon-area_png_open-graph.jpg"
---

# Baochip-1x: What It Is, Why I'm Doing It Now and How It Came About - Baochip-1xとは何か、なぜ今それを行うのか、そしてその経緯
22nmプロセスで“MMU搭載マイコン”がやってきた — 開かれたSoCで組み込みの未来を再設計するBaochip-1x

## 要約
Baochip-1xは、従来の小型マイコンにはほとんど搭載されなかったMMU（メモリ管理ユニット）を備えたRISC‑VベースのほぼオープンRTL SoCで、より安全で移植性の高い組み込みソフトウェア環境を目指している。

## この記事を読むべき理由
日本の組み込み／IoTエンジニアやスタートアップにとって、既存のARM依存を減らしつつ実用的なオープンハードウェア基盤で安全なソフトウェアを動かせる可能性があるため。製造は先進22nmプロセスで行われ、実機入手のチャンスも始まっている。

## 詳細解説
- MMUの意義：MMUは各アプリを独立した仮想メモリ空間で走らせられるため、プロセス分離・スワップなど高度なOS機能（Linuxなど）やロード可能なセキュアなアプリ運用が可能になる。従来の小型MCUはコストとリソース制約でMMUを持たず、代わりにMPU（メモリ保護ユニット）が使われてきたが、MPUは仮想化やスワップが苦手。
- 歴史的背景：ARM7世代の成功により「小型＝MMUなし」の慣習が定着。だが半導体の能力が飛躍的に向上した今、設計上の制約は薄れており、RISC‑VやオープンRTLのおかげで自由に機能選択が可能になった。
- オープン度と現実的選択：Baochip-1xは「ほぼオープンRTL」。演算ロジックなどデータ処理に関わる部分は公開される一方、USB PHYやアナログ回路、AXIバスフレームワークなど一部は閉じたコンポーネントとして残る。完全オープンを待つより、部分的にでも公開してエコシステムを育てる実利を重視している。
- 技術面のトリック（“ヒッチハイク”）：フル新規テープアウトのコストを抑えるため、Crossbar社の22nmチップ設計の余白にVexRiscvコアなどを組み込む形で実現。これにより低コストで先進プロセスの恩恵（22nm＋RRAM）を受けられる。
- ソフトウェア側：純Rustで書かれたXousなどMMU対応の軽量OSを想定しており、Linuxを含め複数のOSやランタイムが検討可能。コミュニティでドライバやドキュメントを育てるフェーズにある。
- 製品化状況：試作ウェハは既に回り、初回数千個規模の量産分を評価ボード（Dabao）経由で先行配布・販売するクラウドファンディングが進行中。追加生産は資金や工程の都合で後倒しになる見込み。

## 実践ポイント
- 興味がある開発者はDabao評価ボードのプロジェクトページ（Crowd Supply）を確認して先行入手を検討する。  
- MMUや仮想メモリを理解する（入門書／オンライン講座）とBaochipでの応用がスムーズ。  
- RustやRISC‑Vツールチェーンに慣れておくと、Xousやドライバ開発に貢献しやすい。  
- 日本の組み込みプロジェクトでARMロックインを避けたい場合の代替選択肢として注視する価値あり。
