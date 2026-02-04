---
layout: post
title: "China-made Loongson 12-core chip is approximately three times slower than six-core Ryzen 5 9600X — 3B6000 hampered by low clock speeds in Linux benchmarks - 中国製Loongson 12コアは6コアRyzenに約3倍遅い：3B6000は低クロックでLinuxベンチを圧迫"
date: 2026-02-04T02:59:54.115Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/pc-components/cpus/china-made-loongson-12-core-chip-is-approximately-three-times-slower-than-six-core-ryzen-5-9600x-3b6000-hampered-by-low-clock-speeds-in-linux-benchmarks"
source_title: "China-made Loongson 12-core chip is approximately three times slower than six-core Ryzen 5 9600X &mdash; 3B6000 hampered by low clock speeds in Linux benchmarks | Tom's Hardware"
source_id: 411171841
excerpt: "中国製12コアLoongson 3B6000、実測でRyzen 5 9600Xの約3分の1性能だが用途次第で健闘"
image: "https://cdn.mos.cms.futurecdn.net/BXqUTJ2D3iyJMb3oQAS83k-1920-80.jpg"
---

# China-made Loongson 12-core chip is approximately three times slower than six-core Ryzen 5 9600X — 3B6000 hampered by low clock speeds in Linux benchmarks - 中国製Loongson 12コアは6コアRyzenに約3倍遅い：3B6000は低クロックでLinuxベンチを圧迫

魅力的な日本語タイトル：国内路線の“国産CPU”はどこまで来た？Loongson 3B6000の実力と日本での意味

## 要約
中国Loongsonの12コア「3B6000」をPhoronixがLinuxで検証したところ、一般的なベンチでは現行の6コアAMD Ryzen 5 9600Xより約3倍遅い結果に。ただし特定ワークロードでは健闘する場面もあった。

## この記事を読むべき理由
国産・代替CPUへの関心が高まる中、日本でも「互換性・性能・用途」を判断する材料になる実測データだから。組込みやサーバ、ソフトウェア移植の観点で今後の動きを追う価値があります。

## 詳細解説
- 試料：Loongson 3B6000（12コア）をPhoronixが受け取り、micro-ATX評価ボード（3B6000x1-7A2000x1-EVB：DIMM×2、M.2、PCIe×2等）で多数のLinuxベンチを実行。  
- 主因：3B6000の動作クロックは約2.5GHzと低め。最新のIntel/AMDが出す3–5+GHzレンジと比べると周波数差が大きく、IPCがそこそこ高くても総合性能で不利になる。  
- アーキテクチャ：記事ではLA664世代のコアを採用し、IPCはZen 3相当という報告もあるが、低クロックが効率をそぎ落としている点が指摘される。  
- ベンチ結果の傾向：多くの汎用ベンチでRyzen 5 9600Xに大きく劣る（概ね3倍遅い）一方、C-Ray 2.0やOpenSSL 3.6、QuickSilverの一部ではRyzenやCore系に匹敵または接近するケースもあった。ワークロード依存性が強い。  
- 今後：Loongsonは次世代LA864などでクロック3.0–3.5GHzを目標に開発中とされ、従来比で大幅改善を狙うが、Intel/AMDの高クロック帯とはまだ差がある模様。  
- 互換性留意点：LoongsonはLoongArch（MIPS系に近い独自命令派生）で、x86互換ではないためソフトの対応（コンパイル／バイナリ対応）が必要。Linuxでのサポートは進んでいるが限定的な点に注意。

## 実践ポイント
- ベンチは「クロック×IPC×ワークロード依存」で評価する：コア数だけで判断しない。  
- 開発者は対象プラットフォーム向けにビルド・最適化を検討する（LoongArch対応のコンパイラやライブラリ確認）。  
- 日本市場では組込み・産業用途や国内代替の観点で注目。導入検討は「目的（計算／暗号／IO等）」に応じて実機ベンチを取るのが早道。  
- 動向ウォッチ：LA864世代やクロック改善の情報、Linux上の実測ベンチを継続チェックするとよい。

（出典元記事の検証結果を要約・翻訳して再構成）
