---
layout: post
title: "Sprites on the Web - Web上のスプライトアニメーション"
date: 2026-02-24T18:33:10.221Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.joshwcomeau.com/animation/sprites/"
source_title: "Sprites on the Web • Josh W. Comeau"
source_id: 397530938
excerpt: "CSSだけで高解像度対応＆容量激減、操作可能なスプライトアニメ入門"
image: "https://www.joshwcomeau.com/images/og-sprites.png"
---

# Sprites on the Web - Web上のスプライトアニメーション
「軽量で制御しやすい！CSSだけで作る“スプライト”アニメーション入門」

## 要約
スプライト（複数コマを横並びした1枚絵）をCSSのobject-fit / object-positionとsteps()で操る手法を解説。GIFより軽く、再生制御や高解像度対応がしやすい利点があります。

## この記事を読むべき理由
モバイル中心の日本市場では表示速度とバンド幅が重要。アイコンや「いいね」アニメーションのような小容量で滑らかな表現を、簡単に実装・制御できるテクニックは即戦力になります。

## 詳細解説
- 基本アイデア：各フレームを横に並べた「スプライトシート」を1枚用意し、HTMLの<img>を「窓」として部分表示する。これを素早く切り替えることでアニメを再現する。
- 画像設計：シート全体の幅÷フレーム数＝1フレームの幅。高DPI対応のため原寸（例：2000×800に5コマ→各400×800）を半分などで表示するとシャープに見せられる。
- CSSのポイント：
  - object-fit: cover で<img>ノードを窓にする（全体を覆うようにスケーリング）。
  - object-position を keyframe アニメで動かし、見せたいコマを切り替える（例：from 0% 0% → to 100% 0%）。
  - animation-timing-function に steps(N, jump-none) を使うと、滑らかに移行せずN段階でジャンプして各コマを等時間表示できる。ループ時は jump-none を使うと最終フレームが抜けない。
- インタラクティブな割り込みの注意：CSSの中断（transition割り込み）でsteps()が期待どおり動かないケースがある。対策として linear と round() を併用する手法や、JSで状態管理する手もある（詳細はインタラクティブ向け実装記事参照）。
- GIFとの比較：GIFは制御・色数・容量で劣ることが多い。スプライトはアニメ速度の変更、再生停止、レイヤー分離（例：燃え・本体を別シートにして重ねる）など柔軟性が高く、最新フォーマット（AVIF/WEBP）で小容量にできる。

## 実践ポイント
- まずは小さなアイコン（例：いいね、トースト通知）で試す。シート横幅÷コマ数でフレームサイズを算出する。
- CSS例（要旨）：
  - .sprite { width: <表示幅>; height: <表示高さ>; object-fit: cover; animation: sprite 1s steps(<コマ数>, jump-none) infinite; }
  - @keyframes sprite { from { object-position: 0% 0%; } to { object-position: 100% 0%; } }
- アクセシビリティ：prefers-reduced-motion を尊重して再生を止める実装を必ず入れる。
- 画像フォーマットはAVIF/WEBPを検討。GIFより圧倒的に軽くなることが多い。
- インタラクティブ操作で滑らかさが必要なら、stepsだけでなくround()やJS制御を組み合わせて割り込みを扱う。
- 日本の環境ではモバイル回線や低スペック端末を想定して、合成レイヤーと最小化画像でファイルサイズを抑えることを優先する。

以上を押さえれば、軽量で制御可能なスプライトアニメーションが手早く実装できます。
