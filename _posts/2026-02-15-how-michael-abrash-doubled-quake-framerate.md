---
layout: post
title: "How Michael Abrash doubled Quake framerate - Michael AbrashがQuakeのフレームレートを2倍にした方法"
date: 2026-02-15T16:06:46.671Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://fabiensanglard.net/quake_asm_optimizations/index.html"
source_title: "How Michael Abrash doubled Quake framerate"
source_id: 1554612570
excerpt: "Abrashが手書きアセンブリでQuakeの描画を最適化しフレームレートを2倍にした実践テクニック"
---

# How Michael Abrash doubled Quake framerate - Michael AbrashがQuakeのフレームレートを2倍にした方法
Quakeを“組み立て”して性能を2倍にしたAbrash流の低レイヤ最適化テクニック

## 要約
1997年のQuakeソースにはMichael Abrashによるアセンブリ最適化が含まれ、C版と比べて実行速度が約2倍になった。主要寄与は低レイヤの描画ルーチンとモデル描画周りの手作業最適化だ。

## この記事を読むべき理由
レトロゲームの最適化話として面白いだけでなく、「プロファイルしてホットスポットに集中する」「CPUパイプライン／FPUを意識した命令スケジューリング」という普遍的な高性能化の教訓が得られるため、日本のゲーム開発者・組込み系や性能改善に携わるエンジニアに役立つ。

## 詳細解説
- 事実関係：Stock WinQuake は timedemo で約42.3fps。アセンブリ最適化を外したビルドは約22.7fpsで、差は約19.5fps。Abrashのアセンブリ群がフレームレート向上に大きく寄与している。
- 対象関数群：ソース内で多くの.asm／.sが見つかるが、実際に効果が大きかったのは
  - D_DrawSpans8（壁・床のスパン描画）: +12.6fps（最大の寄与）
  - R_DrawSurfaceBlock8_mip*（テクスチャ＋ライトマップ合成）: +4.2fps
  - D_Polyset*（モデル描画）: +2.2fps
  残りは微小。
- 最適化手法（Abrashが多用）：
  - ループ展開や分岐削減で分岐予測ミスを回避。
  - 自己書き換えコードで実行時に最適化パスを選択（当時の手法）。
  - Pentium世代のFPUパイプラインを意識した命令並べ替え（ロード→乗算→加算を重ねて遅延を隠す）。
  - 整数パイプラインとFPUを“重ねる”ことで並列実行を引き出す。
- 具体例（TransformVector）：行列×ベクトルのようなホットな小関数を、FPUスタックを巧みに使ってロードと演算を重ね、VC6が吐く単純なコードより遥かにスループットを稼いでいる。

## 実践ポイント
1. まずプロファイラでボトルネックを特定する（Quakeの例もこれが出発点）。  
2. ホットループに集中する：内側ループの命令数・分岐を減らす。  
3. コンパイラの改善を確認する：現代コンパイラやSIMD（SSE/NEON）は多くを自動化するが、特殊ケースでは手書き最適化が効く。  
4. CPU特性を学ぶ：パイプライン、キャッシュ、分岐予測、FPU/SIMDの挙動を理解すると、効果的な並べ替えができる。  
5. 保守性とのバランス：自己書き換えや大量のアセンブリは保守コストが高い。まずはアルゴリズム改善→コンパイラ設定→必要なら局所的にアセンブリ、の順が現実的。  

Quakeの話は「昔のハードでどう絞り出したか」の教科書です。現代でも、プロファイル重視とホットスポットへの集中は変わらない王道です。
