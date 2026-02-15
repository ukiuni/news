---
layout: post
title: "Show HN: VOOG – Moog-style polyphonic synthesizer in Python with tkinter GUI - VOOG — Python/tkinterで作るMoog風ポリフォニック・シンセ"
date: 2026-02-15T21:25:50.000Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/gpasquero/voog"
source_title: "GitHub - gpasquero/voog: VOOG — Virtual Analog Synthesizer (Moog-style polyphonic synth with GUI)"
source_id: 47026768
excerpt: "Python/tkinter製Moog風ポリシンセ、ラダーフィルタとMIDIで即演奏・改造可"
image: "https://opengraph.githubassets.com/56032e1dbf0fc64071ec53ecb603dcd28fd7949e9a27cc9850fa763b3263807f/gpasquero/voog"
---

# Show HN: VOOG – Moog-style polyphonic synthesizer in Python with tkinter GUI - VOOG — Python/tkinterで作るMoog風ポリフォニック・シンセ
Pythonで動くMoog風シンセをGUIで直感操作、学習から即演奏まで使えるオープンソースプロジェクト

## 要約
VOOGはPython（tkinter）で作られた仮想アナログ・ポリフォニックシンセ。Moogライクなラダーフィルタや3オシレーター、ADS R/LFO、MIDI対応を備え、学習用途からサウンドデザインまで使える軽量なツール。

## この記事を読むべき理由
DSPやシンセ設計を実際のコードで学びたいエンジニアや、手軽にカスタム音源を作ってみたい音楽／ゲーム開発者に最適。Pythonで動くため改造や実験がしやすく、日本のDIY／教育用途にも親和性が高い。

## 詳細解説
- 基本構成：3つのオシレーター（sine/saw/square/triangle）＋ノイズで音源を生成。各オシレーターにオクターブ・セミトーン・デチューン・レベル制御あり。  
- フィルタ：Moogラダーフィルタ（24dB/oct、Huovilainenモデル）を実装。カットオフ・レゾナンスにフィルタ用エンベロープを割り当て可能。  
- エンベロープ／LFO：デュアルADS R（アンプ／フィルタ）と4波形LFO。LFOはフィルタ・ピッチ・アンプ等へモジュレーション可能。  
- ポリフォニー／音声管理：4マルチティンブラルチャンネル×各8音ポリ（最大同時音数は実装次第）。ボイスアロケータとボイススティーリングを備える。  
- 入出力：sounddevice+numpyでオーディオ出力。MIDIはmido＋python-rtmidiで任意接続（オプション）。QWERTY仮想鍵盤＋マウスで演奏可。  
- UI／操作：Subsequent 37風のダークテーマと回転ノブGUI（ドラッグ/スクロールで微調整）、プリセット保存は ~/.synth_patches/ に保存。  
- 実装構造：dsp（oscillator/filter/envelope/lfo/glide/noise）、engine（audio_engine/channel/voice/voice_allocator）、gui、midi、patch、cli といったモジュール分割で学習しやすい。

## 実践ポイント
- まず動かす（推奨環境：Python 3.13+、tkinter）:
```bash
git clone https://github.com/gpasquero/voog.git
cd voog
python3.13 -m venv .venv
source .venv/bin/activate
pip install numpy sounddevice
# MIDI対応が必要なら:
pip install mido python-rtmidi
```
- GUI起動:
```python
python -m synth --gui
```
- すぐ試す：内蔵プリセットを読み、フィルタのCutoff/ResoやエンベロープのA/Dを動かして挙動を観察。QWERTYで弾いてレイテンシを確認する。  
- 日本での応用例：ラズベリーパイや教育ワークショップ、ゲーム用効果音のプロトタイピング、DAWへはMIDI経由で連携。ローカル日本語プリセットやUI改良、MIDIマッピングの追加で日本コミュニティ向け貢献が可能。  

興味があればリポジトリでソースを追い、フィルター/オシレーターのアルゴリズム（Huovilainenなど）を読み解くと学びが深まる。
