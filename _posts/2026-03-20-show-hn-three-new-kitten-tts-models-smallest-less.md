---
layout: post
title: "Show HN: Three new Kitten TTS models – smallest less than 25MB - Kitten TTS：最小モデルは25MB未満の新TTS"
date: 2026-03-20T03:09:20.415Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/KittenML/KittenTTS"
source_title: "GitHub - KittenML/KittenTTS: State-of-the-art TTS model under 25MB 😻 · GitHub"
source_id: 47441546
excerpt: "CPUだけで高音質を実現、25MB未満の超軽量Kitten TTSでエッジ端末に即導入可能"
image: "https://opengraph.githubassets.com/9b94c235789e0610ae54cbac38a90f443403fbb0595476242996a268ef01e770/KittenML/KittenTTS"
---

# Show HN: Three new Kitten TTS models – smallest less than 25MB - Kitten TTS：最小モデルは25MB未満の新TTS
魅力的タイトル: CPUだけで高音質、しかも超軽量──Kitten TTSで「声」を手のひらに

## 要約
Kitten TTSはONNXベースのオープンソースTTSで、15M〜80Mパラメータ（ディスク上25〜80MB）の軽量モデルをCPUで高品質に合成できるライブラリです。開発プレビューとして公開され、商用サポートも用意されています。

## この記事を読むべき理由
エッジ端末や組み込みサービスでGPUなしに動く高品質TTSは、日本のスマート家電・音声UI・アクセシビリティ用途で即戦力になります。モデルサイズが小さいため配布・アップデート運用も楽です。

## 詳細解説
- アーキテクチャと実行環境: ONNXで最適化された推論を行い、GPU不要でCPU上で動作。ロードや推論の軽量化に優れるためエッジ用途に適合します。  
- モデルラインナップ: 
  - kitten-tts-mini: 80M パラメータ（約80MB）  
  - kitten-tts-micro: 40M（約41MB）  
  - kitten-tts-nano: 15M（約56MB）および int8 量子化版（25MB）  
  ※一部ユーザーは int8 版で問題を報告しているため注意。  
- 音質/機能: 出力は24 kHz、8種類の組み込みボイス（Bella, Jasper,...）。再生速度の調整や数値・通貨などの前処理機能あり。  
- 現状と将来: 現在は開発プレビューでAPIが変わる可能性あり。ロードマップにモバイルSDKや多言語対応が掲げられているため、日本語やモバイル向けの改善が期待されます。

## 実践ポイント
- インストール（推奨: 仮想環境）:
```python
python
pip install https://github.com/KittenML/KittenTTS/releases/download/0.8.1/kittentts-0.8.1-py3-none-any.whl
```
- 最短サンプル:
```python
python
from kittentts import KittenTTS
model = KittenTTS("KittenML/kitten-tts-mini-0.8")
audio = model.generate("This high-quality TTS model runs without a GPU.", voice="Jasper")
import soundfile as sf
sf.write("output.wav", audio, 24000)
```
- 選び方: デバイスのメモリと配布帯域でモデル（mini/micro/nano）を選ぶ。超軽量が必要ならint8版を試すが、問題が出たら通常版へ戻す。  
- 日本市場での活用例: スマート家電の案内音声、読み上げ機能付きアプリ、オフライン対応の観光案内端末、アクセシビリティ強化。  
- 試す場所: Hugging Face Spacesのデモで手早く品質確認。問題はGitHub Issuesへ報告。

興味があれば公式リポジトリ（KittenML/KittenTTS）とデモをチェックして、実機での検証を始めてください。
