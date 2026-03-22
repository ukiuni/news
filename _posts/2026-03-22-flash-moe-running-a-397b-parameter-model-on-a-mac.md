---
layout: post
title: "Flash-Moe: Running a 397B Parameter Model on a Mac with 48GB RAM - Flash-MoE：48GBのMacで397Bモデルを動かす"
date: 2026-03-22T12:22:59.584Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/danveloper/flash-moe"
source_title: "GitHub - danveloper/flash-moe: Running a big model on a small laptop · GitHub"
source_id: 47476422
excerpt: "48GBのMacでSSDストリーミング＋Metalで397B級モデルを実用速度で動かす手法"
image: "https://opengraph.githubassets.com/aa007a2d307e061e633ad1a97e3e7bd8b4de7e1efb53569de2671fcf9f6aed9a/danveloper/flash-moe"
---

# Flash-Moe: Running a 397B Parameter Model on a Mac with 48GB RAM - Flash-MoE：48GBのMacで397Bモデルを動かす

Macで397Bパラメータ級モデルを“普通のノート”で動かす衝撃 — 48GB RAMのMacBook上で「Qwen3.5-397B」相当をSSDストリーミング＋Metalで動かす手法を解説。

## 要約
SSDから専門家（expert）パラメータをオンデマンドで読み込み、C/Objective‑C＋手書きのMetalシェーダでGPUをフル活用して、397Bモデル相当を48GB RAMのMacで実用的な速度で動かしたプロジェクトです。

## この記事を読むべき理由
大規模モデルは「クラウド必須」ではなく、ローカルの高性能ノートでも工夫次第で実用化できることを示す実践的なケーススタディで、日本の開発者や研究者がコスト／プライバシー面で自前運用を検討する際に直接役立ちます。

## 詳細解説
- モデル構成：60層（45層の線形注意＋15層の通常注意）、各層512個のexpertからK=4活性化、隠れ次元4096。Mixture‑of‑Experts (MoE) 構成。
- SSDエキスパート・ストリーミング：209GB相当のexpertを4ビット量子化でSSDから並列pread()し、1トークンあたり必要なK=4だけを読み込む。OSのページキャッシュを信頼する「Trust the OS」設計で自前キャッシュは不使用。
- データ表現最適化（FMA最適化）：4ビット→実数復元＋行列ベクトル積をGPUのFMA命令に合わせて再配列し、内ループ速度を約12%改善。
- Metalカーネル群：量子化デコンバート（2/4bit）、SwiGLU、RMS正規化、バッチ注意、RoPEのGPU融合、MoE結合/ゲーティングなどを手書きで最適化。
- 遅延実行（Deferred Expert Compute）：expertフォワードをGPUへ非同期投入して、CPU側は次のレイヤ準備を行いパイプラインを維持。
- ハードウェア制約：AppleシリコンはSSD DMAとGPUが同じメモリコントローラを共有するため、SSD → GPU → SSDの直列パイプラインが実測で最適。GPUの帯域がボトルネック。
- 実測性能：4ビット設定で約4.4 トークン/秒（良品質、ツール呼び出し対応）。2ビットは高速化するがJSON/ツール呼び出しで不安定。
- エンジニアリング発見：カスタムキャッシュや圧縮の多くは逆効果で、標準的なOSページキャッシュ＋GPU最適化が最速という結果。

## 実践ポイント
- 推奨設定は「4-bit experts（プロダクション向け）」。2-bitは速度は出るがツール連携で壊れる可能性あり。
- 必要なHWは高速NVMe SSD（連続読み出し数GB/s）＋Mシリーズの大GPU帯域。メモリは48GBあればページキャッシュを活かせる。
- 試すときはリポジトリの metal_infer をビルドして実行（例: make して ./infer --prompt "Hello" --tokens 20）。（実行前にpacked_experts等の重いデータが必要）
- 学べる設計観点：GPU命令レベル最適化（FMA活用）、I/Oを前提にしたレイヤ単位パイプライン設計、そして「まずOSを信頼する」というシンプルなキャッシュ戦略。
- 日本の現場では、クラウドコスト削減やデータ秘匿が必要なアプリで本手法の応用余地が大きい。ローカル推論の選択肢として注目すべき事例です。
