---
layout: post
title: "vLLM large scale serving: DeepSeek 2.2k tok/s/H200 with wide-EP - vLLM 大規模サービング：Wide‑EPでH200あたり2.2kトークン/秒を達成"
date: 2026-01-14T01:30:53.651Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.vllm.ai/2025/12/17/large-scale-serving.html"
source_title: "vLLM Large Scale Serving: DeepSeek @ 2.2k tok/s/H200 with Wide-EP | vLLM Blog"
source_id: 46602737
excerpt: "Wide‑EPとDBOでH200あたり2.2k tok/sを継続達成、MoE運用でコスト削減へ"
image: "https://blog.vllm.ai/assets/logos/vllm-logo-only-light.png"
---

# vLLM large scale serving: DeepSeek 2.2k tok/s/H200 with wide-EP - vLLM 大規模サービング：Wide‑EPでH200あたり2.2kトークン/秒を達成
DeepSeek×vLLMの最前線――Wide‑EPとDual‑Batch Overlapで「同じGPUあたりの処理量」を劇的に伸ばす方法

## 要約
vLLMがV1エンジンに完全移行し、Wide‑EP（Expert Parallel＋Data Parallel）やDual‑Batch Overlap（DBO）などの最適化で、CoreWeave上のH200クラスタでGPUあたり$2.2\text{k tok/s}$を継続達成した、という報告です。MoE（Sparse Mixture‑of‑Experts）型モデルの推論効率が大幅に改善されています。

## この記事を読むべき理由
日本の開発者／SRE／プロダクト担当者にとって、LLM推論はコストとスループットのトレードオフが運用上最大の課題です。本記事は「同じハードウェアでより多くのトークンを処理する」ための実運用ノウハウと設定（Wide‑EP、DBO、EPLB、分離型(prefill/decode)サービング）をわかりやすくまとめており、国内でのコスト削減・スケール設計に直接役立ちます。

## 詳細解説
- V1エンジン移行とコミュニティの裏付け  
  vLLMはv0のエンジンコードを完全に置き換え、V1をベースに最適化を続行。多数のコミットと外部ベンチ（InferenceMax 等）での検証を経て実運用レベルに到達しています。

- Wide‑EP（Wide Expert Parallel）とは何か  
  DeepSeek系の大規模MoEモデルは「実際に使われるパラメータが一部だけ」かつ、MLA（multi‑head latent attention）でKVキャッシュ管理が重要です。Wide‑EPは次を組み合わせます：  
  1) Expert Parallel（EP）で専門家（experts）をランク間で共有してKVキャッシュ効率を最大化  
  2) Data Parallel（DP）で有効バッチサイズとメモリ効率を確保  
  これにより、テンソル並列（TP）よりもMLA系で効率的にGPUメモリを使えますが、EP度合いを上げるとランク間同期通信が増えるため、高速なall‑to‑all実装（DeepEPやPerplexity MoEカーネル等）が不可欠です。

- Dual‑Batch Overlap（DBO）で通信と計算を重畳  
  DBOはマイクロバッチ処理を並列で進行させ、collective通信（all_reduce / all_to_all）と計算の重なりを作る戦略です。vLLMはマイクロバッチワーカーを使いCUDAグラフやMoEカーネルと連携して、通信待ち時間を有効に埋めることでGPU利用率を向上させています。

- Expert Parallel Load Balancing（EPLB）  
  推論時のトークンルーティングは学習時の均等分配から外れることがあり、EPランク間の負荷不均衡が発生します。EPLBはスライディングウィンドウで負荷を計測し、論理→物理のエキスパートマッピングを動的にシャッフル（再配置）して負荷を平準化します。再起動不要で実行時に適用できる点が実用的です。

- Disaggregated prefill/decode（分離型サービング）  
  prefill（コンテキストの埋め込み）とdecode（生成）を役割分担して分散させるパターンは、EP配置で特に効果的です。あるランクのリクエストが別ランクのエキスパートを呼ぶ際の待ち合わせをうまく扱い、単一の重いリクエストが全体を停滞させる問題を緩和します。

- 実測値と要因  
  CoreWeave上のH200+Infiniband（ConnectX‑7）で$2.2\text{k tok/s/H200}$を継続。主な寄与はカーネル最適化（SiLU融合、Cutlass QKV、TP注意のバグ修正）、DBO導入、DeepEPオールトゥオールなどです。これによりレプリカ数を減らし、token/ドルを下げられるのが運用上の利点です。

- エコシステム連携  
  llm‑d（Kubernetes向け）、Dynamo（高スループット低レイテンシ設計）、Ray Serve LLM（Rayエコシステム統合）など、複数の導入経路が提示されています。国内のKubernetesやRay基盤とも親和性が高く、既存のクラスタに組み込みやすい点も重要です。

## 実践ポイント
- すぐ試すフラグ（vLLM CLI）  
  - Expert Parallel: --enable-expert-parallel  
  - Dual‑Batch Overlap: --enable-dbo（しきい値は --dbo-decode-token-threshold で調整）  
  - Expert Load Balancer: --enable-eplb（ウィンドウ／間隔の調整が可能）

- インフラ提示（実行環境の参考）  
  - 高帯域・低遅延ネットワーク（Infiniband + ConnectX‑7相当）で通信ボトルネックを解消すると効果が出やすい。  
  - H200のような大容量GPUと最新カーネルの組合せが推奨。H100等と比較検討する場合はベンチを必ず取ること。

- デプロイ戦略の選び方  
  - 小〜中規模：Ray Serve LLMで手早く試作。KVキャッシュやprefix affinityが利く。  
  - 本番大規模：llm‑dやDynamoのパスでWide‑EP/Disaggregatedパターンを再現して安定化。  
  - ベンチ：prefill/ decodeで分けた実運用ライクな負荷を用意し、tokens/s と token/ドルを測定する。

- 運用上の注意点  
  - EP度合いや再配置（EPLB）のパラメータはワークロード依存。まずは観測ログで負荷分布を把握してから調整する。  
  - カーネルやCUDAグラフ周りの最適化は環境依存性が高いので、カスタムビルドやライブラリのバージョン管理を厳密に。

まとめ：Wide‑EP＋DBO＋EPLB＋分離型サービングの組合せは、MoE系の最先端モデルをより少ないGPUで回すための実効的な手段です。国内でもコスト最適化やオンプレ運用を考えるチームは、vLLMとllm‑d／Dynamo／Rayの導入パスを検討すると良いでしょう。最新のロードマップやカーネル情報は公式ドキュメントで随時確認してください。
