---
layout: post
title: "Wit, unker, Git: The lost medieval pronouns of English intimacy - ウィット、アンカー、ギット：中世に失われた英語の“二人だけ”を示す代名詞"
date: 2026-04-09T12:10:18.891Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.bbc.com/future/article/20260408-the-extinct-english-words-for-just-the-two-of-us"
source_title: "Wit, unker, git: The lost medieval pronouns of English intimacy"
source_id: 47701572
excerpt: "消えた古英語の双数代名詞（wit等）が示す歴史的変化とNLPへの示唆"
image: "https://ychef.files.bbci.co.uk/624x351/p0nc7ttl.jpg"
---

# Wit, unker, Git: The lost medieval pronouns of English intimacy - ウィット、アンカー、ギット：中世に失われた英語の“二人だけ”を示す代名詞
「二人だけ」を示す古い英語の代名詞が消えた理由──言語接触と簡略化が生んだ意外な欠落

## 要約
古英語には「我々二人」を示す dual（双数）代名詞――例：wit（we two）、uncer/unker（our for two）、git（you two）――があり、12〜13世紀ごろに消滅した。北欧語やノルマン語との接触、社会的礼節の変化、言語の簡略化が主な要因だ。

## この記事を読むべき理由
言語の小さな仕組み（代名詞）が歴史的・社会的変化に敏感に反応する様子は、自然言語処理（NLP）、多言語UX、ローカリゼーション、文化的文脈の設計に直接関わるため、日本のエンジニアや翻訳者にも実務的な示唆を与える。

## 詳細解説
- dual（双数）とは：単数・複数に加え「ちょうど二人」を表す文法カテゴリ。古英語はこれを持ち、詩や親密表現で特有の効果を出していた（例：古詩「Wulf and Eadwacer」の uncer giedd = 「二人の歌」）。
- 消滅の経緯：言語は簡略化する傾向があり、汎用の複数形 we で二人も表せるため生存理由が薄まった。さらにヴァイキング（古ノルド語）の侵入で they/them/their を取り込み（元の hie を置換）、1066年以降のノルマン支配でフランス語 vous の敬称機能が英語の you（単数・複数兼用）を広め、thou/thee 系が縮退したことが加速因となった。
- 類似と対照：現在でも双数を残す言語（アラビア語や一部のスラヴ語）や、英語方言での複数you（ye, yous, you all）という現代的ワークアラウンドがある。中英語期には Chaucer らが単数の singular they を用いた記録もある。
- 技術的含意：代名詞形態の縮退は形態素情報の喪失を意味し、古語や方言、歴史テキストの解析では代名詞解決（coreference resolution）が難しくなる。翻訳やトランスクリプションで「二人だけ」の意味をどう再現するかは設計上の課題。

## 実践ポイント
- NLP/解析：歴史テキストや方言を扱う際は双数を想定したルールや辞書を用意する（正規化・注釈で意味を保持）。
- ローカリゼーション：UIで「あなた（単）/あなたたち（複）」を扱う言語差に注意。英語の you は文脈で曖昧になり得るため明示的ラベル（you all / you (plural)）を検討。
- 翻訳・コンテンツ制作：古典やファンタジーで「二人だけ」の親密さを表現したい場合、英語の現代語には直接対応語がないことを利用して日本語的表現（私たち二人／二人きり）を工夫して残す。
- クリエイティブ活用：失われた語（wit, unker など）をブランド名やストーリーテキストに取り入れると、歴史的・詩的なニュアンスを演出できる。
