---
layout: post
title: "Origin of the rule that swap size should be 2x of the physical memory - スワップサイズは物理メモリの2倍にすべき、というルールの起源"
date: 2026-02-26T01:48:25.811Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://retrocomputing.stackexchange.com/questions/32492/origin-of-the-rule-that-swap-size-should-be-2x-of-the-physical-memory"
source_title: "unix - Origin of the rule that swap size should be 2x of the physical memory - Retrocomputing Stack Exchange"
source_id: 47159364
excerpt: "スワップがRAM2倍とされた歴史的理由と現代の最適運用法を具体例で示す"
image: "https://retrocomputing.stackexchange.com/Content/Sites/retrocomputing/Img/apple-touch-icon@2.png?v=6b27f39a6023"
---

# Origin of the rule that swap size should be 2x of the physical memory - スワップサイズは物理メモリの2倍にすべき、というルールの起源
「スワップはRAMの2倍」ルールの真相 — なぜ“2x”と言われたのか、今でも使えるのか

## 要約
「スワップ＝RAMの2倍」は厳密な理論で決まった数値ではなく、歴史的・実務的な経験則（rule of thumb）から生まれた指南です。初期UNIXの実装・運用慣行、フォーク/予約方式、ディスク特性、ユーザーの心理が複合して2xが広まった経緯があります。

## この記事を読むべき理由
日本の開発者／運用者は、現代の大容量RAMやSSD環境で昔の常識を鵜呑みにしがちです。由来を知れば、適切なスワップ設計（例：ハイバネーション要件、クラウドVM、監視方針）を自分の環境に合わせて判断できます。

## 詳細解説
- 歴史的な痕跡  
  - 1989年頃の SunOS 4 インストール文書や1993年の FreeBSD インストーラに2x指定の記録あり。2001年に FreeBSD の man ページで「VMアルゴリズムは2xを想定」と明記。  
  - さらに古い論文（McKusick 1986）では「アクティブな仮想メモリが物理メモリの1.5〜2倍を想定」との記述があり、実装チューニングの根拠になった可能性がある。

- 技術的理由（複合要因）  
  - 予約方式とオーバーコミットの有無：過去のUNIXは匿名領域ごとにスワップ領域を確保する方式が一般的で、forkで同じメモリ空間を複製する運用だとスワップ必要量が倍になる条件があった。  
  - ページングのチューニング：一部実装は「スワップ容量が十分ある」ことを前提にVMスキャンやスワップ策略が調整されていた。  
  - ディスク特性：HDD時代は連続した空き領域（断片化回避）が重要で、ある程度まとまったスワップ領域を確保する慣習が生まれた。  
  - 運用・心理的側面：1xや1.5xは分かりにくく、2xは説明しやすく「安全側」の数字として普及。

- 現代との乖離  
  - SSDや大容量RAM、オーバーコミット（Linuxのovercommitやzram/zswapなど）の普及で「必ず2x」という必然性は低下。  
  - Windowsではフルメモリダンプや仮想アドレス空間の取り扱いがあり、プラットフォームごとに注意点が異なる。

## 実践ポイント
- ルールは出発点に過ぎない：まずは監視（swap使用率・スワップイン/アウト頻度）を導入する。  
- ハイバネーション要件：休止（hibernate）を使うならスワップ >= 実物理RAMが必要。  
- クラウド/サーバ運用：VM用途なら workload に基づきスワップを決め、過度のスワップは「RAM増設」で解決するのが原則。  
- 軽量代替：ラップトップやコンテナ環境では zram/zswap や圧縮スワップを検討する。  
- Windows特有：フルメモリダンプを取りたい場合はページファイルを物理RAM以上に設定する。

まとめ：2xは「安全側の経験則」であり、由来は初期UNIXの実装・運用慣行とディスク特性。現代では環境に応じて柔軟に設計すべきです。
