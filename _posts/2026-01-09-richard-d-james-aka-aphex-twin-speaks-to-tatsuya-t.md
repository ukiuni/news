---
layout: post
title: "Richard D. James aka Aphex Twin speaks to Tatsuya Takahashi - リチャード・D・ジェイムス（Aphex Twin）が髙橋竜也に語る"
date: 2026-01-09T00:49:25.096Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://web.archive.org/web/20180719052026/http://item.warp.net/interview/aphex-twin-speaks-to-tatsuya-takahashi/"
source_title: "Aphex Twin Speaks To Ex. Korg Engineer Tatsuya Takahashi | WARP | Item"
source_id: 46546614
excerpt: "Aphex Twinと高橋が語るMonologueで作る微妙なチューニングとslopの音響設計"
image: "https://web.archive.org/web/20180719052026im_/http://item.warp.net/wp-content/uploads/2017/06/AFX-Facebook-Image.png"
---

# Richard D. James aka Aphex Twin speaks to Tatsuya Takahashi - リチャード・D・ジェイムス（Aphex Twin）が髙橋竜也に語る
アナログの「狂い」をデザインする：Aphex Twin×髙橋竜也が語るマイクロチューニングと“スロップ”の魔力

## 要約
Aphex Twin（Richard D. James）と元Korg技術者髙橋竜也の対談で、Korg Monologueへのマイクロチューニング実装、サンプルレートや意図的な揺らぎ（“slop”）など、音響設計と創作の境界をめぐる技術的かつ哲学的な話が展開される。

## この記事を読むべき理由
- Korgや日本発の楽器設計に関心がある読者に、プロの視点で「規格」と「創造性」の両立を学べる。
- マイクロチューニングや意図的な不完全さ（drift/slop）は、現代の音楽制作で差別化できる実践的な手法だから。

## 詳細解説
- マイクロチューニングとは：12平均律から外れた音階を定義する仕組み。Monologueはユーザーがリアルタイムでスケールを編集でき、Scala形式の読み書きも可能で、これにより既存のチューニング資産と連携できる。
- なぜ重要か：作曲者は国際標準（例：A=440Hz）に従うか、自分の耳に従うかを選べる。Aphex Twinは機材のマスター・チューニングを変えて楽曲基盤を作ることを常套手段としてきたと語る。
- アナログの“狂い”（1v/octaveやアナログ素子の不完全さ）：DX系・SH系などで見られる微妙なズレが音色の魅力になる。髙橋は設計段階で「回路は完璧でなくていい、音が良ければ良い」との教えを紹介する。
- “Slop”とオシレーターのオートチューニング：現代機では「揺らぎ」をパラメータ化して意図的に作ることが増えている。Monologue系では未使用時にオシレーターが再調整されることで「動いているが外れない」感じを実現している。
- サンプルレートの差：48 kHzが業界標準だが、機材によっては31.25 kHzなど異なるレートを使うことがあり、それが音色の個性になる（volca系列の例）。
- ツールとワークフロー：Monologueのエディタ／ライブラリ機能により、簡易なGUIでスケール編集→エクスポート／インポート（Scala）という流れが実現され、実験の門戸が広がった。

## 実践ポイント
- MonologueやScala互換のツールでまず1つスケールを作ってみる。既存のScalaファイルを読み込んで微調整するだけでも表情が変わる。
- モノフォニック機でマイクロチューニングを試すなら、ディレイやリバーブ（フィードバック高め）を併用すると変化が聴き取りやすい。
- 「slop」やdetuneパラメータをオンにして、系統的に楽曲に合う揺らぎ量を記録する。ジャンルや音像で最適値は変わる。
- サンプルレートの違いを意図的に作る（サンプリング→リサンプル）とノスタルジックな色づけができるので、ボトムアップで音作りに取り入れる。
- 教育的には、子ども向けワークショップ（例：簡単なシマティクスや可視化）で音の物理を扱うとチューニング概念が直感的に理解できる。

短めにまとめると、Monologueの事例は「規格に従う便利さ」と「不完全さをデザインする楽しさ」を両立させる好例。日本の楽器設計や音響制作に携わる人なら、一度自分の手でマイクロチューニングと揺らぎを試してみる価値が高い。
