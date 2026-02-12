---
layout: post
title: "GOTO Considered Good, Actually - GOTOは実は良い（本当に）"
date: 2026-02-12T22:42:30.530Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://adamledoux.net/blog/posts/2026-02-09-GOTO-Considered-Good--Actually--or--i-made-a-tool-for-writing-casio-calculator-games-using-twine-.html"
source_title: "GOTO Considered Good, Actually (or: i made a tool for writing casio calculator games using twine)"
source_id: 1134329861
excerpt: "古いカシオ電卓で動くTwine風分岐小説をGOTO変換で簡単に実機で遊べる"
image: "https://adamledoux.net/blog/images/adam.png"
---

# GOTO Considered Good, Actually - GOTOは実は良い（本当に）
GOTOで作る！カシオ電卓で動くTwine風インタラクティブ小説の作り方

## 要約
古いカシオのグラフ電卓をターゲットに、Twineのtwee形式をCasio BASICに変換するトランスパイラ（tweeul8r）を作った話。GOTOベースの分岐で、電卓上で遊べる短いインタラクティブ小説が動きます。

## この記事を読むべき理由
レトロなハードで「手軽に作れるインタラクティブ作品」を作るアイデアは、日本の学生やコミュニティ向けワークショップ、教育用途、レトロコンピューティング愛好家に刺さります。カシオは国内で馴染みあるメーカーなので、手元の電卓を遊びや学びに活かせます。

## 詳細解説
- 元ネタは作者が拾ったカシオのグラフ電卓とCasio BASIC。Casio BASICはシンプルな入出力とGOTOベースの分岐が基本で、これがTwine風の分岐型物語にマッチします。
- 作者はTwine（twee）からCasio BASICへ変換するトランスパイラ「tweeul8r」を作成。tweeの物語ノードを解析して、GOTOで遷移するCasioプログラムに出力します。
- 制約事項：電卓のメモリ制限により最大ストーリー長は小さめ、マクロ機能は未対応などの制限があります。またテキスト表示幅・行数にも注意が必要です。
- 配布方法：出来上がったプログラムはCAT形式（Casioのプログラムファイル）で出力され、作者はitch.ioにブラウザ上で動くエミュレータ版とCATファイルを公開。USB経由で実機に転送すれば実際の電卓で遊べます。
- 開発ワークフロー：Twine 1エディタでストーリーグラフを作成 → twee形式でエクスポート → tweeul8rで変換 → エミュレータでテスト → CATを電卓へ転送、という流れ。

## 実践ポイント
- まずはTwine 1で短い分岐ストーリーを作る（短いパッセージを多用するのが吉）。
- テキスト量は抑える：電卓の画面・メモリ制約を忘れずに。長文は分割して表現。
- マクロや複雑な関数は使わず、シンプルな分岐で設計する。
- エミュレータで動作確認してからCATファイルをUSBで転送する（実機での表示確認が重要）。
- 教育・ワークショップ向けには「プログラミング入門＋物語制作」の教材として最適：GOTOによる制御フローの学習にもなる。

興味があれば、作者のページのitch.ioエミュレータや配布ファイルを試してみてください。
