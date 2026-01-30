---
layout: post
title: "Solving Fossil's ASCII art CAPTCHA in 171 characters - FossilのASCIIアートCAPTCHAを171文字で解読"
date: 2026-01-30T00:51:01.864Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.nns.ee/2026/01/29/fossil-captcha-solver/"
source_title: "Solving Fossil's ASCII art CAPTCHA in 171 characters"
source_id: 928114596
excerpt: "171文字のPythonワンライナーでFossilのASCII CAPTCHAを瞬時に突破する技"
---

# Solving Fossil's ASCII art CAPTCHA in 171 characters - FossilのASCIIアートCAPTCHAを171文字で解読
たった171文字で解読！Fossilの“可愛い”テキストCAPTCHAを一刀両断する最短テクニック

## 要約
Fossil SCM のテキストベースCAPTCHA（5×7のビットマップをUnicodeブロックで描画）を、識別に十分な2行だけを使ってパターン化し、XOR＋剰余を使った短いルックアップで171文字のPythonワンライナーで解く話。

## この記事を読むべき理由
キャプチャ回避や画像認識の入門的発想、ビットパッキング／コードゴルフのテクニック、そして「単純なテキストCAPTCHAがいかに脆弱か」を短く学べます。日本の開発者にも実務で役立つ思考法です。

## 詳細解説
- フォント仕様：Fossilは16進数字を5×7ビットマップで定義し、表示は「オン＝██（2文字）」「オフ＝スペース×2」で、文字間にさらに2スペース。1桁は幅12文字。
- 素朴な対処法：全16文字分を事前レンダリングして照合すると確実だがデータ量が大きい。
- 削減アイデア：7行のうち任意の2行の組み合わせで16文字が一意に判別できることを探索し、(3,6)行が有効と判明。これで各桁は10ビット（$2\times5$）に圧縮される。
- ルックアップ短縮：10ビット値をそのまま使うと密度が低いので、ある剰余（mod 43）で一意にマップできることを発見し、43文字のスパーステーブルで高速化。
- さらに最適化：値にXORを入れてから小さな剰余にする（例: ^293 %21）とルックアップが21文字に短縮できる。ビット位置の式は $5\cdot (r<4) + 4 - c$ で、行 r と列 c の組で適切にビットを割り当てる。
- ちょっとした省略術：ブロック文字判定を "=='██'" ではなく 文字コード比較の ">'!'" にして1文字分削る荒業（'█' のコードは大きく ' ' より明確に大きいため）。

最終的に得られた171文字のワンライナー（可読性優先に少し改行・空白を省いた形）：

```python
s = lambda t:(L:=t.split('\n')) and ''.join(
 '2f1?8e?b374a6c95d??0?'[
  (sum(((L[r][p+c+c]>'!')<< (5*(r<4)+4-c)) for r in (3,6) for c in range(5))^293)%21
 ] for p in range(0,len(L[0]),12))
```

## 実践ポイント
- 解析者向け：まずフォントの最小識別セット（行や列の組合せ）を探すと、処理量を劇的に削減できる。XOR＋剰余の組合せは「値を散らす」小技として有効。
- 防御者（サービス提供側）向け：テキストベース／単純ビットマップCAPTCHAは簡単に突破される。視覚ノイズやランダム変形、実用的な証明作業（PoW）や認証フローを導入すべき。
- 学習用途：ビット演算、真偽値の整数化、シフト演算、テーブル圧縮といった基礎概念の良い練習になる。

（参考元：Rasmus Moorats によるブログ記事「Solving Fossil's ASCII art CAPTCHA in 171 characters」）
