---
layout: post
title: "Show HN: I trained a 9M speech model to fix my Mandarin tones - 9Mパラメータの中国語発音チューターを作った"
date: 2026-01-31T02:36:11.654Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://simedw.com/2026/01/31/ear-pronunication-via-ctc/"
source_title: "A 9M-parameter Mandarin pronunciation tutor - SimEdw&#39;s Blog"
source_id: 46832074
excerpt: "ブラウザで動く9Mモデルで中国語の声調ミスを高精度検出、13MBで実装可能"
---

# Show HN: I trained a 9M speech model to fix my Mandarin tones - 9Mパラメータの中国語発音チューターを作った
魅せるタイトル: ブラウザで動く9Mの中国語発音チェッカー――トーンを「聞いて直す」小型モデルの作り方

## 要約
元記事は、約300時間の音声データで学習したConformer+CTCモデル（最小9Mパラメータ）をブラウザ上で動かし、マンダリンの声調（トーン）ミスを厳密に検出・評価する取り組みを紹介しています。

## この記事を読むべき理由
トーンの判定は学習者にとって最も難しい点の一つ。日本の語学学習アプリやオフラインでのプライバシー重視ソリューションに直結する「小型で高精度・オンデバイス」モデル設計の実例だからです。

## 詳細解説
- アーキテクチャ：ConformerエンコーダをCTC損失で学習。局所的なスペクトル特徴は畳み込み、長距離依存は注意機構で捕らえる設計が理由。
- CTCを選んだ理由：Seq2seq型だとモデルが補正してしまい「実際に発された音」を評価できない。CTCは各フレーム（約40msごと）に確率分布を出し、空白トークンを使って生の発話を扱う。
- 強制アライメント：出力行列に対してViterbiで最適経路を求め、期待するピンイン+トーン（例 ni3 → hao3）に対応する時間領域を特定する。
- トークン化：漢字ではなく「ピンイン＋トーン」を第一級トークンに。zhong1 と zhong4 は別トークン。語彙は約1,254トークン（+ <unk>, <blank>）。
- データと学習：AISHELL-1 と Primewords を合わせ約300時間。SpecAugment を適用。4×NVIDIA RTX 4090 で学習に約8時間。
- モデル縮小と性能：75M → 35M → 9M と削減しても精度はほとんど落ちず、タスクは「データ依存」であることを示唆。
  - 75M: TER 4.83% / Tone accuracy 98.47%
  - 35M: TER 5.16% / Tone accuracy 98.36%
  - 9M: TER 5.27% / Tone accuracy 98.29%
- 量子化と配布：FP32で約37MB、INT8量子化で約11MBに縮小。onnxruntime-webでブラウザ動作が可能で、実デモは ~13MB 程度のダウンロード。
- 実装上の注意点：先頭や沈黙フレームのアライメントがスコアを消すバグがあり、空白確率が高いフレームを除外してスコアリングすることで信頼度が回復。

python
```python
def _filter_nonblank_frames(span_logp: torch.Tensor, blank_id: int = 0, thr: float = 0.7):
    """Only keep frames where the probability of <blank> is below a threshold.
    If we filter everything (total silence), we fall back to scoring the whole span.
    """
    p_blank = span_logp[:, blank_id].exp()
    keep = p_blank < thr
    if keep.any():
        return span_logp[keep]
    return span_logp  # Fallback
```

- 課題と次の一手：読み上げ・朗読データ中心の学習データに偏っているため会話体や子供の声で弱い。Common Voice 等の会話データ追加が有効。

## 実践ポイント
- デモを試す：オンデバイスで手早くトーン評価を試し、学習フィードバックに使える（リンクは元記事）。
- 小型モデルを目指すなら：データ増強（SpecAugment）＋INT8量子化で配布コストを下げる。onnxruntime-webが即実装の近道。
- 発音評価を設計する際：漢字ではなく「ピンイン＋トーン」トークンを使うと誤りが明示される。
- 精度向上の優先順位：モデル拡大より多様なデータ収集（会話／子供／雑音下）を優先するのが効果的。
- UI実装の注意：無音フレームを除外するなど、フレーム単位の信頼度処理を入れると誤判定が劇的に減る。

興味があれば、これを日本語学習アプリや発音矯正ツールに応用する道筋が見えます。
