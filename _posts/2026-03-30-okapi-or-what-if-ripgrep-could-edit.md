---
layout: post
title: "Okapi, or “What if ripgrep Could Edit?” - Okapi：もしripgrepが編集もできたら？"
date: 2026-03-30T08:01:50.605Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kocharhook.com/post/6/"
source_title: "Okapi, or “What if ripgrep Could Edit?” &middot; &gt; kin stash"
source_id: 1123903273
excerpt: "数万行のOCR誤りを原画像参照で高速一括修正するOkapi実践記"
image: "https://kocharhook.com/post/6/featured.jpg"
---

# Okapi, or “What if ripgrep Could Edit?” - Okapi：もしripgrepが編集もできたら？
「数万行のOCRミスをエディタで一括修正する」──隙のないアーカイブ作業を可能にする新ツールの実践リポート

## 要約
ripgrepの探索力とテキストエディタの編集力を組み合わせた「Okapi」を使い、何万行ものOCR（scanno）をコンテキスト付きで高速に見つけて一括修正できる仕組みを紹介する記事です。

## この記事を読むべき理由
大量の文書デジタル化・アーカイブ（官公庁資料、古新聞、戸籍など）が進む日本でも、OCRの誤認識は現場の大きな負担です。手作業でファイルを開いて直す方法は非現実的になっており、Okapiのアプローチは作業効率を劇的に改善します。

## 詳細解説
- 背景：著者は米国のOfficial Register（過去150年分の公務員名簿）をデジタル化する作業で、良質なOCR（olmOCR）を使っても多数の「scanno（例：III が Ill に誤変換される）」が残る問題に直面。単純な正規表現置換では誤置換や見落としが発生する。
- アプローチ：ripgrepで正規表現にヒットした行を一つの「編集バッファ」に集約し、gitのinteractive rebase風にファイル別のエイリアス/行番号で紐付け。エディタ（例：Sublime）のマルチセレクトで複数ファイルの該当行を同時編集し、編集が終われば各ファイルへ保存するワークフローを実現。
- 実装の肝：
  - OkapiはRustで実装され、ripgrepの検索精度と速度を活用。
  - 画像とテキストの連携：各列イメージはTesseractでラインごとのバウンディングボックス付きJSONを事前生成。対象テキスト行とTesseract行を正規化＋トライグラムによるファジーマッチで対応付け、該当領域を切り出してUUEncodedで返す。
  - エディタ連携：Sublimeプラグインがカーソル移動に応じて該当行の画像領域をHTMLオーバーレイで表示。テキストだけでなく原画像を同時に見ながら判断できるため、 ambiguous な修正（例：Fli → Eli/Flin/…）が速く正確になる。
  - コマンド例（簡潔なフラグ）：
    - okapi III
    - okapi "Dan[^l ]\b"
    - okapi "Mich\wl" -e "Michel"
    - okapi Fli -c ..15

## 実践ポイント
- 小さく試す：まずripgrepで問題パターンを洗い出し、Okapiで編集バッファにまとめてみる。
- 画像連携を用意する：Tesseractで行バウンディングボックス付きJSONを先に生成すると、テキスト→画像の照合が劇的に効く。
- ファジーマッチ戦略：単純置換は危険。正規化＋トライグラムなどの距離指標で候補を絞ると誤修正が減る。
- エディタ機能を最大活用：マルチカーソル／マルチセレクトで同種の誤りを一括修正し、残りは画像参照で微修正する運用がおすすめ。
- 日本語環境での注意：縦書き資料や旧字、ルビ混在などはTesseract挙動が変わるため、事前にOCR設定（モデル・言語パラメータ）やノーマライズ処理をカスタマイズする。

OkapiはHomebrewでインストール可能で、ソースやIssue/PRも公開されています。大量ドキュメントの現場改善に直結する実用的なアイデアなので、デジタルアーカイブやレガシーデータ整備に携わる人は一度試してみてください。
