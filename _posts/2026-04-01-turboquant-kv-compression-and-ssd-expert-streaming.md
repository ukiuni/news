---
layout: post
title: "TurboQuant KV Compression and SSD Expert Streaming for M5 Pro and IOS - M5 ProとiOS向けTurboQuant KV圧縮とSSDエキスパートストリーミング"
date: 2026-04-01T19:25:50.571Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/SharpAI/SwiftLM"
source_title: "GitHub - SharpAI/SwiftLM: ⚡ Native MLX Swift LLM inference server for Apple Silicon. OpenAI-compatible API, SSD streaming for 100B+ MoE models, TurboQuant KV cache compression, + iOS iPhone app. · GitHub"
source_id: 47604354
excerpt: "TurboQuant圧縮とSSDゼロコピーでM5 Pro/iOS上で122B級モデルを実用化"
image: "https://opengraph.githubassets.com/b41362fcb1c93aa809f0c97fb110fb74cec7780d5cc464d844c07e17e60b5681/SharpAI/SwiftLM"
---

# TurboQuant KV Compression and SSD Expert Streaming for M5 Pro and IOS - M5 ProとiOS向けTurboQuant KV圧縮とSSDエキスパートストリーミング
M5 Proで122B級モデルを動かす──KVキャッシュ圧縮とSSDゼロコピーで「メモリの壁」を突破する手法

## 要約
Apple SiliconネイティブのSwiftLMは、Metal上で動作するTurboQuantベースのKVキャッシュ圧縮と、MoE（Mixture of Experts）レイヤをNVMeからGPUへゼロコピーするSSDストリーミングで、M5 Proのようなマシンで100B〜122B級モデルを実用的に動かせる仕組みを提供する。

## この記事を読むべき理由
日本でもApple Silicon搭載MacやiPhoneでオンデバイス推論・プライバシー重視の運用を検討する場面が増えている。SwiftLMのアプローチは「大きなモデル＝クラウド頼み」を変える可能性があり、コスト削減や遅延改善、法規制対応に直結するため要注目。

## 詳細解説
- ネイティブ実装：Swift + Metalで完全ネイティブ動作。PythonやGILに依存せず、単一バイナリで高速に動く点が特徴。
- OpenAI互換API：/v1/chat/completionsなど既存クライアントをほぼそのまま利用可能。
- TurboQuantハイブリッド：V2（高速・線形）とV3（高品質・非線形）を融合。
  - 正規化：各ベクトルはまず正規化される（$\hat{x} = x / \|x\|$）。
  - WHT回転：Fast Walsh–Hadamard Transformで外れ値を分散させる。
  - 3ビットのLloyd–Max非線形量子化で座標を符号化し、残差をJohnson–Lindenstrauss（QJL）で1ビット補正する。結果的にKVキャッシュは約$3.6$ bits/dim（V-cacheは$3.125$ bits/dim）程度に圧縮され、FP16比で約3.5×の節約を達成。
  - 実装はC++エンコーディング経路とMetalシェーダでデコンプレッションを行い、Pythonオーバーヘッドを排除。
- SSD Expert Streaming：MoEのエキスパート行列をNVMeからGPUコマンドバッファへ直接マッピング（ゼロコピー）することで、macOSの統合メモリをスワップ／破壊せずに巨大モデルを扱える。M5 Pro（64GB）でQwen3.5-122Bのようなモデルが動作可能と報告。
- 実用上の注意：4-bit量子化が実運用の安全圏とされ、2-bit等の過度な量子化は出力のJSON構造を壊すなど不安定化のリスクあり。
- iOS対応：SwiftLM Chatアプリがあり、HuggingFaceからモデルをダウンロードして端末上で推論可能。Xcodeプロジェクトは生成スクリプトで再作成する設計。

## 実践ポイント
- まずはリリースの事前ビルドをダウンロードして試すのが最短。
- macOSサーバ起動例（bash）:
```bash
.build/release/SwiftLM --model Qwen3.5-122B-A10B-4bit --stream-experts true --port 5413
```
- 大型MoEを扱う場合は必ず`--stream-experts=true`を有効にし、`--gpu-layers`でGPU割当を調整する。
- 量子化は段階的にテストし、生成品質（特にJSONツール呼び出し）の検証を行う。
- iOSで試す場合はリポジトリのgenerate_xcodeproj.pyでプロジェクトを再生成し、XcodeでTeam設定→実機でビルドする。

以上を踏まえ、Apple Silicon上で巨大モデルをオンデバイス運用するための現実的な選択肢としてSwiftLMは注目に値する。
