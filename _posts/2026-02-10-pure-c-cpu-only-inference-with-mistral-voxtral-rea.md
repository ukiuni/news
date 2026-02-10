---
layout: post
title: "Pure C, CPU-only inference with Mistral Voxtral Realtime 4B speech to text model - Mistral Voxtral Realtime 4B の純C版 音声→テキスト推論"
date: 2026-02-10T06:44:29.073Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/antirez/voxtral.c"
source_title: "GitHub - antirez/voxtral.c: Pure C inference of Mistral Voxtral Realtime 4B speech to text model"
source_id: 46954049
excerpt: "GPU不要の純C実装でMac上で低遅延にVoxtral 4Bをffmpeg連携で即時文字起こし可能"
image: "https://opengraph.githubassets.com/7079b23f398a49afc598baffc398a0d44fb39620a1c0f7eb4f6d7ff82240e8e5/antirez/voxtral.c"
---

# Pure C, CPU-only inference with Mistral Voxtral Realtime 4B speech to text model - Mistral Voxtral Realtime 4B の純C版 音声→テキスト推論
MacでGPU不要・ffmpegと即時連携できる「純C」Voxtral――依存ゼロで組み込みやオンプレ運用がぐっと身近に。

## 要約
antirezが公開したvoxtral.cは、MistralのVoxtral Realtime 4Bを外部依存なしで純C実装した推論エンジン。Apple SiliconではMetal（MPS）で高速化し、ストリーミングAPIとffmpeg連携で低遅延の文字起こしが可能です。

## この記事を読むべき理由
日本の開発現場では、クラウド依存・GPU環境が無いケースやプライバシー重視のオンプレ利用が多い。依存を減らしたC実装は、組み込みアプリや社内サーバー、ローカルでの自動議事録化などに直接使える現実的な選択肢を提供します。

## 詳細解説
- 実装の核：完全なCで書かれ、標準ライブラリ以外に依存しない（MPS以外はOpenBLASでのビルドも可）。モデル重みはsafetensorsのBF16でメモリマップ読み込みして高速起動。
- ハードウェア：Apple SiliconではMetal/MPSで融合演算やバッチ注意機構を使い高速。Intel/LinuxはOpenBLASを利用（bf16→fp32変換で遅め）。
- ストリーミングとAPI：vox_stream_tというストリーミングC APIを提供。音声をチャンクで与えれば、生成されるトークンを逐次取得できる（リアルタイム文字起こしに最適）。
- 音声処理：オーバーラップするチャンクエンコーダでメモリ使用量を入力長に依存させず固定化。stdinパイプやmacOSのマイク入力（--from-mic）をサポート。
- レイテンシ制御：-I <秒>でエンコーダ処理間隔を指定。小さくすると応答性向上だがGPUオーバーヘッド増、1.0–2.0秒が実運用で良好な折衷点。
- ローリングKVキャッシュ：デコーダのKVキャッシュはスライディング窓（8192トークン）で自動圧縮し、長時間音声でもメモリを抑制。
- 代替トークン：--altで不確実性の高い候補語を表示可能（同音語や曖昧箇所の確認に有用）。
- ビルドとサイズ：make mps / make blasでビルド。モデルは約8.9GBで download_model.sh で取得。Python参考実装も同梱（学習用）。

CLIの基本例（ffmpeg経由でMP3を即時文字起こし）:
```bash
# bash
ffmpeg -i podcast.mp3 -f s16le -ar 16000 -ac 1 - 2>/dev/null | \
  ./voxtral -d voxtral-model --stdin -I 1.5
```

## 実践ポイント
- Apple Siliconならまず make mps を試す（MPSで最速）。モデルは約9GBなのでストレージに注意。
- リアルタイム用途は -I 1.0〜2.0 が実用的。0.5未満はGPUコストが跳ね上がる。
- ffmpegと --stdin 組み合わせで任意フォーマットを即変換→文字起こしできる（バッチ処理やパイプラインに最適）。
- マイク入力（macOS）でオンデバイスの会議録音ツールを短期間で作れる。プライバシー重視の社内運用に向く。
- 長時間音声はKVキャッシュの動作を確認しておく（巨大連続音声での挙動検証を推奨）。
- CのストリーミングAPI（vox_stream_t）を使えば、既存のC/C++サービスに低遅延で組み込める。

興味があればリポジトリの README と python_simple_implementation.py をまず眺め、Apple Silicon環境で簡単なffmpeg→voxtralパイプを試すのが手早い出発点です。
