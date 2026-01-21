---
layout: post
title: "So, why *should* GNOME support server side decorations? - なぜGNOMEはサーバーサイド装飾を採用すべきか"
date: 2026-01-21T16:44:02.185Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blister.zip/posts/gnome-ssd/"
source_title: "So, why *should* GNOME support server side decorations? :: Blister's blog"
source_id: 701060978
excerpt: "GNOMEがSSDを採用すればウィンドウ崩壊を防ぎ、互換性とWayland移行が加速する。"
image: "/posts/gnome-ssd/cover.png"
---

# So, why *should* GNOME support server side decorations? - なぜGNOMEはサーバーサイド装飾を採用すべきか
ボタンのズレを終わらせる：GNOMEがSSDを受け入れるべき理由

## 要約
サーバーサイド装飾（SSD）はデスクトップ側でタイトルバーを描画する方式で、GNOMEが現状で主に採るクライアントサイド装飾（CSD）と対立する。SSD対応を加えればアプリ互換性、見た目の一貫性、Wayland普及への障壁低減につながる。

## この記事を読むべき理由
日本の企業やクリエイターが使うマルチプラットフォームアプリ（例：DaVinci Resolve等）や業務系ツールで、GNOME上でウィンドウ操作が壊れる事例があり、デスクトップの断片化は開発コストやWayland採用の阻害要因になっています。SSD対応はその改善策です。

## 詳細解説
- 用語整理：  
  - SSD（Server Side Decorations）＝デスクトップ（合成サーバ）がタイトルバーを描く。  
  - CSD（Client Side Decorations）＝アプリ自身がタイトルバーを描く（GNOMEはこれを推奨）。  
  - xdg-decoration＝SSD/CSDを調整するWaylandプロトコル（現状「非安定」だが事実上広く採用）。
- 現状の問題点：  
  - 一部アプリはCSDを正しく扱えず、移動やリサイズができない、タイトルバーが消えるなどの不具合が起きる。  
  - 対応のために使われるlibdecorは“応急処置”で見た目や挙動が各アプリでバラバラになる。  
  - GNOMEがSSDを拒むため、xdg-decorationは事実上の標準ながらGNOMEは非対応で断片化を助長している。
- GNOMEがSSDを受け入れると得られる効果：  
  - サードパーティアプリがネイティブなタイトルバーを得て見た目・操作が一貫する。  
  - 他デスクトップでGNOMEアプリを使う際、SSDを尊重できるので相互互換性が向上する。  
  - 開発者の手間とバグが減り、Wayland対応を進めやすくなる。
- 反対意見と反論：  
  - 「xdg-decorationは仕様外」→多くの実装が存在し、実運用では事実上の標準になっている。  
  - 「装飾はアプリの責任」→ファイルダイアログなどと同じく、選択肢としてデスクトップ提供を許容するのは現実的で互換性を高める手法。

提案される実装イメージ：GNOME側でxdg-decoration等のプロトコルを実装し、統一されたタイトルバーが望ましいアプリにはSSDを適用。GNOMEネイティブ設計（統合ヘッダーバー）を壊さないよう、アプリ側の意図は尊重しつつ「ユーザーが強制的にタイトルバーを付ける」オプションを用意する。

## 実践ポイント
- 開発者向け：アプリは可能ならxdg-decorationに対応し、CSDに依存する実装はフォールバックを用意する。libdecorは一時的な対策と考える。  
- ユーザー向け：GNOMEで動かないアプリはバグ報告を出し、アプリ側にSSD対応の要望を伝える。  
- デスクトップ開発者／ディストリビュータ向け：mutter/GNOME側でxdg-decorationを検討し、ユーザー選択肢（強制タイトルバー等）を実装することで断片化を減らす。
