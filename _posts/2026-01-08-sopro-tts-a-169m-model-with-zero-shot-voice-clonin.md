---
layout: post
title: "Sopro TTS: A 169M model with zero-shot voice cloning that runs on the CPU - CPUで動くゼロショット声クローン対応の軽量TTS「Sopro」"
date: 2026-01-08T21:57:51.051Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/samuel-vitorino/sopro"
source_title: "GitHub - samuel-vitorino/sopro: A lightweight text-to-speech model with zero-shot voice cloning"
source_id: 46546113
excerpt: "CPUで動く169Mの軽量TTS、3–12秒の参照で声をゼロショット再現"
image: "https://opengraph.githubassets.com/b1f9ffd5d95131cd99259542884be23ff2a5d5fac60c0a4a0053bf0d5c239993/samuel-vitorino/sopro"
---

# Sopro TTS: A 169M model with zero-shot voice cloning that runs on the CPU - CPUで動くゼロショット声クローン対応の軽量TTS「Sopro」
CPUだけで動く、手軽に試せる英語TTS。ゼロショットで短い参照音声から話者を模倣でき、低コストでローカル音声生成を試せます。

## 要約
Soproは169Mパラメータの軽量テキスト読み上げモデルで、WaveNet系の拡張畳み込みと軽量なクロスアテンションを使い、3–12秒の参照音声からゼロショットで声をクローンできます。CPU上での実行が可能で、M3ベースで約0.25のRTF（30秒音声を7.5秒で生成）を達成しています。

## この記事を読むべき理由
日本でも「プライバシー重視のローカル音声合成」「少ない算力でのオンデバイス実行」「短いサンプルで声を再現するカスタム音声UX」は注目分野です。Soproは低予算・少ない計算資源で試せるため、プロトタイプ開発や実験用途にぴったりです。

## 詳細解説
- アーキテクチャ: Transformerではなく、拡張畳み込み（WaveNet風のdilated convs）に軽量クロスアテンションを組み合わせた構成。これにより計算効率を重視しつつ音声生成が可能。
- 主要スペック:
  - パラメータ数: 約169M
  - ゼロショット音声クローン: 参照音声3〜12秒が推奨
  - ストリーミング対応と非ストリーミング対応の両方を提供
  - CPU実行の目安: M3で0.25 RTF（実環境で変動）
- 入力・制御:
  - CLI／Python APIあり。スタイル強度（--style_strength）や早期停止判定（stop_threshold / stop_patience）などの制御パラメータで類似度や生成長さを調整可能。
  - 数式や略語は事前に読み方を整える（例: "1 + 2" → "1 plus 2"）と発音が安定する。
- 制約と注意:
  - 学習データは主に英語コーパス（LibriTTS, Common Voice等）で、日本語は未対応。日本語で良好な結果を得るには日本語データで再学習や微調整が必要。
  - マイク品質・ノイズに敏感で、OOD（訓練外）話者では声の類似が落ちる場合がある。
  - ストリーミング版は非ストリーミング版とビット精度が異なり、最高品質を求めるなら非ストリーミングを推奨。
  - 生成長さは約32秒（400フレーム）で安定性が低下するため、長尺は分割して処理すると良い。
- 実装／環境ヒント:
  - 開発者はL40S GPU一枚で訓練したと明言。ローカルでの実験コストが低いのが特徴。
  - 特定環境ではtorchのバージョンで性能差が出る（例: M3ではtorch==2.6.0が高速だったとの報告）。  

簡単な実行例（インストールとCLI）は次の通り。

bash
pip install sopro

bash
soprotts \
  --text "Sopro is a lightweight 169 million parameter text-to-speech model." \
  --ref_audio ref.wav \
  --out out.wav

python
from sopro import SoproTTS
tts = SoproTTS.from_pretrained("samuel-vitorino/sopro", device="cpu")
wav = tts.synthesize("Hello! This is a non-streaming Sopro TTS example.", ref_audio_path="ref.wav")
tts.save_wav("out.wav", wav)

## 実践ポイント
- とりあえず試す: pipでインストールして、手持ちのクリアな3〜12秒の参照音声で実験してみる。まずは非ストリーミングで品質確認。
- パラメータ調整: 声の類似度を高めたいときは --style_strength を微調整。生成が途中で止まる／止まらない問題は stop_threshold / stop_patience を調整。
- 日本語対応の道筋: 日本語音声を使うなら、日本語コーパスで再学習またはファインチューニングが必要。まずは英語で挙動を掴み、声表現の仕組みを学んでからローカライズするのが現実的。
- 実運用上の注意: プライバシーのためにローカル実行は有効。ただし商用利用や配布時はApache-2.0のライセンス条項を確認すること。
- 品質向上: 録音環境（マイクとノイズ対策）を整えることでクローン精度が大きく改善する。

Soproは「少ない計算で声を試せる」魅力的な出発点です。英語中心の現状を理解した上で、日本語応用やオンデバイス実装のプロトタイプに活用してみてください。
