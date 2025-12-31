---
layout: post
title: "When square pixels aren't square - 正方形ピクセルが必ずしも「正方形」じゃないとき"
date: 2025-12-31T15:38:48.271Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://alexwlchan.net/2025/square-pixels/"
source_title: "When square pixels aren't square"
source_id: 46443988
excerpt: "ピクセル比の見落としで動画表示が崩れる原因とffprobeでの対処法解説"
---

# When square pixels aren't square - 正方形ピクセルが必ずしも「正方形」じゃないとき
驚きの落とし穴：表示サイズが違う動画にハマらないための「ピクセル比」入門

## 要約
ストレージ上のピクセル解像度（SAR）だけを見ると、実際の表示サイズ（DAR）と食い違い、レイアウト崩れやレターボックスが発生する。解決策はピクセルアスペクト比（PAR／sample aspect ratio）を考慮して表示アスペクト比を算出すること。

## この記事を読むべき理由
モバイル中心の日本市場では縦長動画（YouTube Shorts 等）や古いSD素材を扱う機会が多く、読み込み前に確実なレイアウトを確保することがUXに直結する。知らないと微妙なズレで累積レイアウトシフト（CLS）や視覚的不具合を招く。

## 詳細解説
動画には少なくとも次の3つの概念がある：
- SAR（Storage Aspect Ratio）: ストレージ上の幅×高さ（例 1920×1080）。フレームデータそのもののサイズ。  
- PAR（Pixel Aspect Ratio / sample_aspect_ratio）: 1ピクセルの縦横比（例 45:64）。ピクセルが正方形でない場合に 1 とはならない。  
- DAR（Display Aspect Ratio）: 実際に画面に表示されるサイズ。 SAR に PAR を掛け合わせた結果になる。

数式で表すと：
$$
DAR = SAR \times PAR
$$

例えば SAR が 1920（幅）で PAR が 45:64 の場合、表示幅は
$$1920 \times \frac{45}{64} = 1350$$
となり、QuickTime が表示する 1350×1080 に一致する。

問題が起きる典型例：
- ストレージ幅だけを使って CSS の `aspect-ratio` を指定していると、実際の再生時にブラウザがピクセル比を適用して表示サイズを変え、レイアウトが更新される（CLS）。
- 縦横どちらかが 1:1 の保存解像度でも PAR によって縦長／横長に表示されるケース（特に Shorts 等）もあるため、保存解像度＝表示解像度と仮定できない。

ツールでの確認方法：
- ffprobe で stream の `width,height,sample_aspect_ratio` を取得するのが確実。
- pymediainfo 等は近い値を返すが丸め誤差が入ることがあるので、正確性を求めるなら ffprobe の JSON 出力を使う。

実例コマンド（確認用）：
```bash
# ffprobe で幅・高さ・sample_aspect_ratio を JSON 出力
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,sample_aspect_ratio -print_format json "video.mp4"
```

実際の処理では、PAR が無ければ 1 を使い、SAR の幅に PAR を掛けて表示幅を算出し整数に丸める（切り捨てではなく四捨五入が望ましい）。

短い Python 実装例（要 subprocess／json）:
```python
# python
from fractions import Fraction
import json, subprocess
from pathlib import Path

def get_display_size(path: Path):
    cmd = [
        "ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height,sample_aspect_ratio",
        "-print_format","json", str(path)
    ]
    out = subprocess.check_output(cmd)
    info = json.loads(out)
    s = info["streams"][0]
    par = Fraction(s.get("sample_aspect_ratio", "1:1").replace(":", "/"))
    disp_w = round(int(s["width"]) * par)
    disp_h = int(s["height"])
    return disp_w, disp_h
```

## 実践ポイント
- ブラウザに事前に伝える aspect-ratio は表示アスペクト比（DAR）を使う。例えば CSS なら計算した表示幅/表示高さを `aspect-ratio` に渡す。
- 動画処理パイプラインのどこかで意図せず PAR が付与されることがある（特に短尺縦動画やサムネ処理）。入力ファイルの `sample_aspect_ratio` を常にチェックする運用を導入する。
- ffprobe の JSON 出力を使えば自動化が容易。パイプラインやビルド時に DAR を算出してメタデータとして保存しておくとフロントエンド側での再計算を防げる。
- 丸めは round() を使う：float での計算や int() の切り捨てはピクセル単位で見たときに差異を生むことがある。

## 引用元
- タイトル: When square pixels aren't square  
- URL: https://alexwlchan.net/2025/square-pixels/
