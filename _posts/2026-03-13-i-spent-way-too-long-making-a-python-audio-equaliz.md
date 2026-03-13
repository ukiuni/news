---
layout: post
title: "I Spent Way Too Long Making a Python Audio Equalizer and Learned a Lot - Pythonでオーディオイコライザを作りすぎて学んだこと"
date: 2026-03-13T18:09:53.102Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/@keepingupwithriya/i-spent-way-too-long-making-a-python-audio-equalizer-and-learned-a-lot-6a2e8ff35d08"
source_title: "I Spent Way Too Long Making a Python Audio Equalizer and Learned a Lot | by Keepingupwithriya | Mar, 2026"
source_id: 383577186
excerpt: "FFT正規化やスレッド同期など即実践できるPython製リアルタイムEQ開発の落とし穴と解決法"
---

# I Spent Way Too Long Making a Python Audio Equalizer and Learned a Lot - Pythonでオーディオイコライザを作りすぎて学んだこと
Pythonで作る“ちゃんと動く”リアルタイムEQ：小さなミスとUXが結果を左右する開発メモ

## 要約
FFTのスケール誤り、スレッド競合、UIの使い勝手──小さな問題の積み重ねが「使える」リアルタイムEQと「動くけど使わない」ものを分けた、という話。

## この記事を読むべき理由
オーディオ処理は数学だけでなく実装の細部（正規化、同期、表示）が成功を左右します。日本の趣味・プロの音響実験や教育プロジェクトで「Pythonでまず試す」際に役立つ具体的な落とし穴と解決策がまとまっています。

## 詳細解説
- FFTの正規化：
  - 生のint16値をそのままFFTに入れるとdBスケールが狂う。正しくはサンプルを最大値で正規化してからdBFSに変換する。例えば振幅を32768で割り、dBFSは $20\log_{10}(|x|/32768)$ のように扱うと、無音が低いノイズフロア（例 −60 dBFS）として見える。
- EQカーブの可視化：
  - 各バンドのIIRフィルタを合成した周波数応答をリアルタイムに表示することで、スライダー操作がスペクトルにどう作用するか直感的に分かる。実装には scipy.signal.sosfreqz を利用。
- スレッドとバッファ同期：
  - 入力キャプチャ（44.1kHz）と描画（30fps）が同じバッファを触ると競合でクラッシュやデータ破損が起きる。解決は threading.Lock のような排他制御で「同時アクセスを防ぐ」こと。
- UI/UXの重要性：
  - 見た目や小さなフィードバック（ダークテーマ、スライダーのdB表示、ピークホールド、動作表示、プリセット）は「実用的かどうか」を大きく左右する。6バンド→10バンド（31Hz〜16kHz）など設計の見直しで使いやすくなる。
- ツールチェーン：
  - PyAudio、NumPy、SciPyでプロトタイプは十分可能。ただし低レイテンシが必須の場面では注意が必要。FFT/IIRなど数学は理解すれば実装は比較的素直。

参照コード（作者のGitHub）：https://github.com/Iyeba-Kallon/realtime-audio-equalizer-spectrum-analyzer

## 実践ポイント
- 音声データは必ず最大値で正規化してからFFTへ。dB表現は $20\log_{10}$ を使う。
- 入出力を担当するスレッド間は必ずロックで同期する（threading.Lock）。
- 周波数応答を可視化するなら scipy.signal.sosfreqz を試す。
- UIは小さな改善（値表示、ピークホールド、ステータス）で実用度が劇的に上がる。
- 学習用にまずPythonで試し、後で必要なら低レイテンシ実装に移行すると効率的。
