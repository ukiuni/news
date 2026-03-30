---
layout: post
title: "NumPy as Synth Engine - NumPyをシンセエンジンに"
date: 2026-03-30T17:54:54.455Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kennethreitz.org/essays/2026-03-29-numpy_as_synth_engine"
source_title: "NumPy as Synth Engine - Kenneth Reitz"
source_id: 862018225
excerpt: "NumPyだけで弦・打楽器・オルガンを物理モデルから再現し、自由に音色や調律を操作できる方法を紹介"
image: "https://kennethreitz.org/og-image/essays/2026-03-29-numpy_as_synth_engine.png"
---

# NumPy as Synth Engine - NumPyをシンセエンジンに
PythonとNumPyだけで「楽器を数学で再現する」——コードを読めば音の仕組みがわかる、そんな驚きの話

## 要約
NumPy/SciPyだけで弦楽器やタブラ、ジャンベ、ハモンドオルガンまで物理モデルで合成してしまう話。録音ではなく「数式から直接生成」するため、音色や調律を自在に変えられるのが肝。

## この記事を読むべき理由
- サンプルライブラリに頼らず音を「物理的に」作る手法は、音楽ソフト／教育ツール／研究用途で強力。  
- 日本の伝統楽器（琴・三味線・太鼓など）や歴史的調律を再現したい開発者・研究者に実用的なヒントを与える。

## 詳細解説
- コアとなる手法：Karplus–Strong（弦モデル）。ランダムノイズを長さが1周期となる遅延バッファに入れ、隣接サンプルとの平均を繰り返すだけでプラック音が得られる。平均化は高域を削る（ローパス動作）ため、実際の弦の減衰に似た音になる。周期は $period = \mathrm{SAMPLE\_RATE}/hz$ のように決まる。  
- 楽器差の出し方：同じアルゴリズムでも周辺処理で別物になる。例えば
  - アコースティックギター：複数のバンドパス（ボディの共鳴周波数）を重ねる。  
  - エレキギター：コームフィルタ（遅延コピーを引く）で特定倍音をキャンセル／強調してピックアップ特性を模す。  
  - ハモンド：複数正弦波を重ねる加算法（ドローバーの比率で音色が決まる）。  
- 打楽器の物理モデリング：タブラは皮膜（バンドパスノイズ）・殻の共鳴（正弦波）・syahiによる特定倍音・手によるピッチスイープなどを重ねて各打撃音を再現。クロスチョーク（ある打撃が別の鳴りを瞬時に減衰させる）も短いフェードで実装し、リアルな奏法を再現する。  
- 実装スタック：NumPy配列が「シンセエンジン」、scipy.signalがフィルタ設計と畳み込み／フィルタ処理、numpy.random/numpy.sin等がノイズ／発振源。結果として「コードがそのまま物理を説明する」メリットがある。  
- もう一つの利点：すべてを数値で生成するため、ピッチや調律を任意に変えても正しい物理挙動が保たれる（歴史的調律・ジャストイントネーションの再現が容易）。

簡単なイメージ（Python）:
```python
python
import numpy as np
SAMPLE_RATE = 44100
def karplus_strong(hz, length_s=1.0):
    period = int(SAMPLE_RATE / hz)
    buf = np.random.uniform(-1,1,period)
    out = np.zeros(int(length_s*SAMPLE_RATE))
    for i in range(len(out)):
        out[i] = buf[i % period]
        nxt = (i+1)%period
        buf[i%period] = 0.5*(buf[i%period]+buf[nxt])*0.999
    return out
```

## 実践ポイント
- まずKarplus–Strongを試す：コードは短く、音の変化が直感的に分かる。周期長・減衰係数・初期ノイズをいじるだけで音色が劇的に変わる。  
- フィルタで「体」を作る：バンドパスで共鳴ピーク（ボディや殻）を追加すると一気に楽器感が増す。scipy.signal.butter＋lfilterが手軽。  
- 打楽器は「層の重ね合わせ」：皮膜＝バンドパスノイズ、殻＝正弦波、トランジェント＝短いノイズ、といった要素を合成する。短いフェードでクロスチョークを実装すると演奏性が劇的に向上。  
- 調律実験：サンプル音源では不可能な歴史的／非等分割調律を試し、楽器の「本来の響き」を再現してみる。  
- 性能面：Pythonは学習・プロトタイピングに最適。最終的なリアルタイム用途はC拡張や音声DSPフレームワークへの移植を検討。

短時間で「コードから音の物理を理解できる」楽しさが本記事の肝。サンプルに頼らない合成は、音楽制作・教育・文化保存で大きな可能性を開きます。
