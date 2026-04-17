---
layout: post
title: "30 Years of HPC: many hardware advances, little adoption of new languages - HPCの30年：ハードは進化したが新言語は普及せず"
date: 2026-04-17T07:45:37.420Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://chapel-lang.org/blog/posts/30years/"
source_title: "Reflections on 30 Years of HPC Programming: So many hardware advances, so little adoption of new languages"
source_id: 47759436
excerpt: "HPCはハードが劇的進化した一方でFortran/Cが根強く残る理由と今取るべき対策を解説"
---

# 30 Years of HPC: many hardware advances, little adoption of new languages - HPCの30年：ハードは進化したが新言語は普及せず
ハード激変でも言語は不変？――「使える」HPCコードが生まれる理由と今すべきこと

## 要約
TOP500で見ると過去30年でコア数や性能は桁違いに拡大したが、現場で広く使われるコンパイル言語は依然としてFortran/C/C++が中心のまま、GPU時代の言語多様化も限定的、という現状を議論する回顧録。

## この記事を読むべき理由
日本の研究機関・企業（富士通、理研、スーパーコンピュータ利用者など）にとって、なぜ既存言語に固執するのか、今後の人材育成や投資判断に直結する洞察が得られます。

## 詳細解説
- ハードの変化：1995→2025でコア数は $~563$～$141{,}750\times$、性能（Rmax）は $~3.3\times10^{6}$～$1.83\times10^{7}\times$ の向上。要因はベクトル命令の普及、マルチ/メニーコア化、チップレット、マルチソケット、ハイラディックスイッチ、GPUの商用化など。
- 現場の言語・モデル：1995年はFortran/C/C++、MPI/PVM/SHMEM、スレッドやベンダー拡張。2025年も基本はFortran/C/C++、MPI/SHMEM、OpenMP（共有メモリ）、GPU向けにCUDA/HIP/SYCL/OpenACC/OpenCL、ライブラリとしてKokkosが導入されるに留まる。スクリプトはPythonが主流に。
- なぜ新言語が広がらないか：既存コード資産の長寿、性能と移植性の厳しい要求、コンパイラ・ランタイムの複雑さ、エコシステム（ライブラリ／デバッガ／プロファイラ）の不足、実運用での検証コストが主因。
- プログラミング難化の本質：GPUやNUMAなどで「データ配置」と「実行場所」の制御が重要に。これを抽象化できないと、言語だけで解決は難しい。ChapelやJuliaのような新言語は生産性を狙うが、採用にはエコシステム成熟が鍵。

## 実践ポイント
- GPU/分散の基礎は必須：MPI＋OpenMP（またはKokkos）＋CUDA/SYCLの基礎を身につける。  
- 性能は「データ局所性」で決まる：NUMA意識、メモリ割当とスレッド親和性を確認する。  
- 移植性重視なら抽象化層を使う：KokkosやSYCLなど性能ポータブルなライブラリを検討。  
- 小規模で試して評価する：新言語／ツールはまずプロトタイプで性能と運用性を検証。  
- コミュニティ参加：ツールチェインやライブラリの成熟には現場のフィードバックが有効。PRやベンチ共有で貢献する。

（参考）HIPSやChapelの取り組みは「高レベル並列表現の実用化」を目指す試みとして注目に値します。
