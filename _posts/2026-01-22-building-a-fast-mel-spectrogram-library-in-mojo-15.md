---
layout: post
title: "building a fast mel spectrogram library in mojo (1.5-3.6x faster than librosa) - Mojoで高速メルスペクトログラムを作る（librosaより高速）"
date: 2026-01-22T10:45:04.743Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://devcoffee.io/blog/building-a-fast-mel-spectrogram-library-in-mojo/"
source_title: "Building a Fast Mel Spectrogram Library in Mojo | Dev Coffee"
source_id: 420525949
excerpt: "MojoでWhisper互換メル変換がlibrosa比1.5–3.6倍高速化"
image: "https://devcoffee.io/og-default.jpg"
---

# building a fast mel spectrogram library in mojo (1.5-3.6x faster than librosa) - Mojoで高速メルスペクトログラムを作る（librosaより高速）
Whisper前処理が劇速に：Mojoでlibrosaを超えたメル変換の舞台裏

## 要約
Mojoでゼロから作ったメルスペクトログラム実装が、短尺で2–3x、長尺で20–27%ほどlibrosa（NumPy/SciPyバックエンド）を上回る性能を出した。10段階の最適化で内部的に約24xの高速化を達成している。

## この記事を読むべき理由
Whisper系の音声前処理（メル変換）は推論レイテンシに直結します。日本のリアルタイム音声サービス／会議文字起こし／字幕生成で「速さ」と「再現性（Whisper互換出力）」を両立したい開発者に有益です。

## 詳細解説
- 背景設計  
  - Whisper互換パラメータに固定（16kHz, n_fft=400, hop=160, n_mels=80）して正確性を担保。FFIでRust/Pythonと連携可能。外部依存を避けメモリレイアウトやアルゴリズムを自前で制御。
  - メモリ配置はSoA（Structure-of-Arrays）、64バイト整列でSIMDとキャッシュ効率を最大化。

- 主要な最適化（概略）  
  0. Naive → 1. Iterative FFT（Cooley–Tukey、キャッシュ寄せ）: 3.0x  
  2. Twiddle（sin/cos）事前計算とキャッシュ: 1.7x → 2.0x  
  3. Sparse filterbank（非ゼロ係数のみ保管）: 1.24x  
  4. @always_inline でホット関数を強制インライン: 小幅改善  
  5. Float32 精度運用でメモリ・SIMDスループット向上: ≈1.07x  
  6. True RFFT（実入力向けに半分のFFTを計算）: ≈1.43x  
  7. RFFTのゼロアロケーション＋Radix-4バタフライ  
  8. コンパイル時CPU検出で可変SIMD幅（AVX-512/AVX2/SSE対応）: 1.12x  
  - 総合で初期476ms → 約20ms（ランダム音声で公正比較）

- 実用的効果  
  - ベンチマーク（ランダム音声, 固定シード）:  
    - 1s: mojo ~1ms vs librosa 2–3ms（2–3x）  
    - 10s: mojo ~7ms vs librosa ~10ms  
    - 30s: mojo ~20ms vs librosa 26–37ms（20–27%優位）  
  - 短いチャンク処理（ストリーミング）で特に利点が大きい。Whisper前処理の遅延削減はリアルタイム体験に直結。

- 失敗と学び（重要）  
  - 「ナイーブSIMD」は遅くなる：未整列メモリ・スカラーループが足を引っ張る。SIMDはポインタベースの整列ロードが鍵。  
  - 四段階FFT（four-step）は音声サイズでは逆効果。Nが非常に大きい場合以外は意味がない。  
  - ビット逆順ルックアップやストライドベースのSIMD化も期待通りでない場合が多い。常にベンチマークで検証。

- 制約と今後  
  - 現時点はWhisper向けデフォルト値に最適化済み。ARM/Apple Siliconではパフォーマンス差が出るため追加プロファイリングが必要。長時間音声はチャンク処理推奨。

## 実践ポイント
1. データ配置を見直す：Complex配列よりSoA（real配列/imag配列）へ。SIMD化が容易になる。  
2. 実入力はRFFTを使う：$N/2+1$ 頻度ビンで済むので計算量半減。  
3. Twiddleは事前に計算・キャッシュ化する：毎フレームのsin/cos計算を避ける。  
4. SIMDは必ず整列ロード＋幅検出で実装（platform-adaptive）。ナイーブ実装は逆効果。  
5. フレーム並列化は長尺で有効（短尺ではスレッドオーバーヘッドに注意）。  
6. まず計測すること：理論的最適化が実機で逆効果になる例が多数ある。  
7. 出力の検証：librosa/Whisper期待値に対して誤差が十分小さいか（例: 1e-4）を確認する。

インストール例:
```bash
# bash
git clone https://github.com/itsdevcoffee/mojo-audio.git
cd mojo-audio
pixi install
pixi run bench-optimized
```

日本のユースケースでは、コールセンターのリアルタイム字幕や会議記録、スマホでの低遅延音声入力などで即時の恩恵が期待できます。まずは自分のワークロードで「測る」ことから始めてください。
