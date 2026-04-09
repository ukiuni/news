---
layout: post
title: "Research-Driven Agents: What Happens When Your Agent Reads Before It Codes - リサーチ駆動型エージェント：コードを書く前に“読む”と何が起きるか"
date: 2026-04-09T18:39:33.226Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.skypilot.co/research-driven-agents/"
source_title: "Research-Driven Agents: What Happens When Your Agent Reads Before It Codes | SkyPilot Blog"
source_id: 47706141
excerpt: "論文やフォークを先に調査し融合最適化でCPU推論を短時間で最大15%改善できた実践手法"
image: "https://blog.skypilot.co/research-driven-agents/assets/banner.png"
---

# Research-Driven Agents: What Happens When Your Agent Reads Before It Codes - リサーチ駆動型エージェント：コードを書く前に“読む”と何が起きるか

AIが論文やフォークを先に「読む」だけで、LLMのCPU推論が短時間で数％〜十数％改善した実話

## 要約
エージェントに「先にリサーチさせる」ループを追加すると、コードだけ見て最適化するより質の高い仮説が出てくる。SkyPilotの実験では、約3時間・4台のクラウドVMで5つのカーネル最適化を見つけ、TinyLlama 1.1B のCPU推論を x86で +15%（テキスト生成）、ARMで +5%（目安）改善した。

## この記事を読むべき理由
多くの日本企業やスタートアップはGPUを常時確保できない・コスト重視でCPU/ARM環境を使う場面が多い。コードだけ追うだけでは見えない「メモリ帯域」や他実装（CUDA/Metal/フォーク）の知見を活用すれば、低コストで実用的な性能改善が得られます。

## 詳細解説
- 問題点：コードだけだと“なぜ遅いか”や外部の代替アプローチが見えない。最初の波ではエージェントがSIMD系マイクロ最適化を試すも効果は僅少で、後に「メモリ帯域ボトルネック」であることが判明（roofline的観点）。
- 手法：autoresearchループに「リサーチ」フェーズ（arXiv、競合フォーク、他バックエンドのコード調査）を追加。エージェントがベンチマークと正当性チェックを自動生成し、SkyPilotで実験をクラウドVMに並列展開して結果を収集・コミット。
- 研究で見つかった示唆：CUDA/Metalや高速フォーク（ik_llama.cpp 等）にある「オペレータ融合」がCPU版に欠けている点が多く、これが改善余地を示唆。
- 実際に入れた最適化（5つのうち代表）：
  1. Softmaxの複数パスを1パスに融合（コピー→スケール→マスクをまとめる）  
  2. RMSNorm のコピー＋スケールを1パスへ融合  
  3. from_float の並列化戦略を動的に切替（行単位／要素単位）  
  4. グラフレベルでの RMS_NORM + MUL 融合（CPUでAVX2/NEON実装）  
  5. FlashAttention の QK タイル処理をAVX2 FMAで1パスに融合  
- 結果：最終的に flash attention を有効にした比較で x86 のテキスト生成が約 +15%（他操作も含めて総合的改善）、ARMでも改善を確認。コストは約 $29（VMとAPI）で3時間程度。

## 実践ポイント
- まず「ベンチマーク＋正当性チェック」を用意する（再現可能なベンチを自動化すること）。  
- エージェントループにリサーチフェーズを追加：arXivだけでなく「競合フォーク」「CUDA/Metal等の他バックエンド」を必ず調べさせる。  
- まずプロファイルして「メモリ帯域か計算バウンドか」を判定（rooflineを意識）。メモリ帯域がボトルネックなら「メモリパス削減＝融合」が有効。  
- 小さく試す：1〜2個のVMで短時間の実験を回し、有望案だけスケールアウト。コストは低く抑えられる（参考：$20 VM + $9 APIで約3時間の実験）。  
- 実装注意：単純に書き換えるとコンパイラのベクトル化に頼らず逆に遅くなることがあるため、明示的なSIMD実装（AVX2/NEON）や段階的A/Bテストが重要。  
- 日本向けの視点：AWSのGraviton（ap-northeast-1など）を使うケース、オンプレやエッジでのCPU推論コスト削減に直結するため、早めに試しておく価値が高い。

短時間・低コストで得られる「読む→試す→改善」ループは、LLMのCPU最適化やコスト効率改善に即効性があります。まずは自プロジェクトでベンチを作り、フォークや他バックエンドの実装を調べるところから始めましょう。
