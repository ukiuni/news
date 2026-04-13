---
layout: post
title: "Tracking down a 25% Regression on LLVM RISC-V - LLVM RISC‑Vで発生した25%の性能低下を追う"
date: 2026-04-13T17:44:57.750Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.kaving.me/blog/tracking-down-a-25-regression-on-llvm-risc-v/"
source_title: "Tracking down a 25% Regression on LLVM RISC-V – KG&#39;s Blog"
source_id: 47743728
excerpt: "InstCombineの変更でfdiv.d化しP550で約25%性能低下、範囲解析で回復"
---

# Tracking down a 25% Regression on LLVM RISC-V - LLVM RISC‑Vで発生した25%の性能低下を追う
LLVMの最適化が意図せず崩れて、SiFive P550上でループが約25%遅くなった原因と修正までの流れ

## 要約
LLVMの中間最適化（InstCombine）の変更で整数→浮動小数点変換の扱いが変わり、結果としてdouble版の除算命令（fdiv.d）が使われてしまい、RISC‑V上で約24–25%の性能後退が発生した。著者はllvm-mcaやIR比較で原因を突き止め、range分析を追加するパッチで狭め化（narrowing）を復活させて改善した。

## この記事を読むべき理由
コンパイラの小さな内部改善が実機性能に重大な影響を与える実例で、RISC‑Vや組み込み向け最適化、コンパイラデバッグの実践テクニック（IRの比較、llvm-mca、コミット差分探索など）を学べます。日本の組込み／OS開発者やコンパイラに興味があるエンジニアに直結する話題です。

## 詳細解説
- 問題の観察  
  SiFive P550（アウトオブオーダ実行）上であるベンチマークを比較すると、GCCよりLLVMのビルドが約8%多くサイクルを消費。詳細を見ると主要ループでLLVMがfdiv.d（double除算、遅延33サイクル）を吐いており、GCCはfdiv.s（float除算、遅延19サイクル）だった。これがスループット/RThroughputを悪化させ、実測で約24%の回帰を生んだ。

- なぜ起きたか（IRレベル）  
  元ソースにある定数リテラルがdouble（74383.0）であるため、コンパイラは一時的にfloat→double（fpext）→doubleの除算→double→float（fptrunc）というIRを生成していた。従来の中間最適化はこの流れを「早期に」floatに狭めて fdiv.s にできていたが、最近のInstCombineの変更（isKnownExactCastIntToFPにComputeNumSignBitsを導入）でint→FPキャストの扱いが変わり、狭め化に必要だった情報が消えてしまった。結果、最終的にdouble除算（fdiv.d）が生成された。

- 解析手法  
  llvm-mcaで命令遅延とスループットを確認、古いビルドと新しいビルドで生成アセンブリを比較、clangで最適化前後のLLVM IRを出力して中間で何が起きているかを追跡。さらにコミットログを漁り、該当するInstCombineのコミットを特定して再現確認。

- 解決策  
  著者はgetMinimumFPTypeに範囲解析（range analysis）を追加することで、fptrunc(uitofp x double) → float を直接 uitofp x to float に簡約できることを認識させ、狭め化を復活させるパッチを当てて回帰を解消した。

## 実践ポイント
- ソースレベルでの簡単対策：浮動小数点リテラルは必要なら明示的にfloatに（例: 74383.0f）しておくと、コンパイラに余計なcastを生ませず安全。  
- デバッグツール：llvm-mcaで命令遅延/スループットを確認、clangで -S -emit-llvm を使って最適化前後のIRを比較。  
- 回帰対応の流れ：まず実機で差分を確認 → IR比較 → llvm-mcaで命令レベル診断 → git log/コミット差分で怪しい変更を絞る → ビルド前後で再現 → 最小再現ケースを作ってパッチ/報告。  
- コミュニティ貢献：コンパイラ改善は新たな回帰を生むことがあるので、最小再現ケースとベンチ結果を添えてIssue/PRを出すと効果的。  
- 日本の製品開発へ：RISC‑V搭載機の最適化は命令幅やレイテンシ差が効きやすく、組み込み・リアルタイム用途ではリテラル表記やコンパイラバージョン管理を厳密に行うことが重要。

上記は実際のトリアージと修正例の要約です。興味があれば原著のコミットやパッチ（isKnownExactCastIntToFPの差分、getMinimumFPTypeへのrange分析追加）を直接確認すると勉強になります。
