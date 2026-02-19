---
layout: post
title: "Making a font with ligatures to display thirteenth-century monk numerals - 9,999個の合字で13世紀修道士の数字を表示するフォントを作る"
date: 2026-02-19T01:37:12.535Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://digitalseams.com/blog/making-a-font-with-9999-ligatures-to-display-thirteenth-century-monk-numerals"
source_title: "Making a font with 9,999 ligatures to display thirteenth-century monk numerals &mdash; Digital Seams"
source_id: 47024585
excerpt: "OpenType合字9,999個で中世システルシアン数字を検索・コピー可能に再現する手法"
image: "http://static1.squarespace.com/static/598a2436f7e0ab837d08f4c6/t/6988cab5f56f56652b3541b5/1770572486488/cistercian-font-preview.png?format=1500w"
---

# Making a font with ligatures to display thirteenth-century monk numerals - 9,999個の合字で13世紀修道士の数字を表示するフォントを作る
9,999の合字で中世の「システルシアン数字」をフォントだけで再現する方法

## 要約
OpenTypeの合字(ligature)を使い、4桁までを一つのグリフに置き換えることで「システルシアン数字」をフォントだけで表示する実験的プロジェクト。検索やコピーができる「見た目だけ変える」アプローチが特徴。

## この記事を読むべき理由
フォントの合字機能を使うと、表示を大きく変えつつ文字列の機械可読性を保てます。日本のUI/ツール開発者やタイプ技術に興味がある人にとって、新しい表現手法と注意点（アクセシビリティ／悪用リスク）が学べます。

## 詳細解説
- アイデア：Chris HeilmannらのCistercian（システルシアン）数字ジェネレータのSVGパスを使い、数値列に対応する合字グリフを用意。元テキストは普通の数字（例: "1234"）のまま、フォントが対応する合字に差し替えて描画する。
- 実装要点：OpenTypeのfeature「liga」で大量の置換ルールを記述する。例:  
  feature liga { sub one zero zero zero by cistercian_1000; sub one zero zero one by cistercian_1001; … }  
  合字マッチは貪欲（greedy）なので、4桁から定義を始めることで長い数列でもまとまったグリフに変換できる（例えば123456は「1234」と「56」に分割）。
- 表示と操作性：見た目は一つの絵だが、テキストは数値のままなのでCtrl‑F検索、コピー＆ペースト、スクリーンリーダーへの影響（注：大きく変えるとアクセシビリティ問題になる可能性あり）などが生じる。
- 文字論的興味：桁の配置（四象限の順序）が一般的な左→右の期待とは異なり「中間エンディアン」的になる点や、横軸・縦軸の書き方の歴史的差異が解説されている。
- 実装補足：作者は生成コードの多くをAIで作成したと明記。ソースはGitHub（bobbiec/cistercian-font）で公開。

## 実践ポイント
- デモを試す：まずブラウザで作者のデモを触って検索／選択動作を確認する。
- 小さなフォント実験から：合字は数百〜数千定義で試せる。まず短い置換（2〜4文字）で動作確認をしてからスケールする。
- アクセシビリティを配慮：表示を派手に置き換えるとスクリーンリーダーや検索挙動が混乱する可能性があるため、視覚表現とテキスト意味の一致を保つ設計を優先する。
- セキュリティ／倫理：フォントで表示を偽装する技術は便利だが、誤解や悪用（表示トリック）につながるため用途を慎重に検討する。
- 参考実装を読む：興味があれば元作者のGitHubリポジトリを参照して、OpenTypeルールの生成スクリプトやSVG→グリフ変換の方法を学ぶ。
