---
layout: post
title: "How far back in time can you understand English? - 英語はどこまで遡って分かるか？"
date: 2026-02-21T17:33:12.954Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.deadlanguagesociety.com/p/how-far-back-in-time-understand-english"
source_title: "How far back in time can you understand English?"
source_id: 47061614
excerpt: "100年刻みで英語を遡り、読解不能になる時代とNLP対策を可視化"
image: "https://substackcdn.com/image/fetch/$s_!94Uq!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dddb379-4714-4730-bb8d-538c26e2d623_1600x1066.jpeg"
---

# How far back in time can you understand English? - 英語はどこまで遡って分かるか？
魅惑の「100年ずつ後退」実験で分かる、英語理解の限界とその技術的意味

## 要約
英語の文章を「100年ずつ古くする」実験で、現代英語がどの時点で急に読めなくなるかを可視化。綴り・文法・語彙の変化が段階的に理解困難さを生む様子を再現している。

## この記事を読むべき理由
言語の時間的変化は、翻訳・ローカライズ、NLP（歴史コーパス処理、ドメイン適応）、古文書デジタイズなど日本のエンジニアやローカライズ担当者に直結する実務的課題を含んでいるため。

## 詳細解説
- 実験の骨子：ブログ記事風の現代英語を出発点に、約100年刻みで筆致・綴り・語彙を「当時らしく」書き換え、千年分を圧縮した連続テキストを作成。読者が何処で読解を断念するかを観察する手法。
- 近代以降（1700–2000年）：綴りの標準化（18世紀以降）により現代英語と安定して互換性が高い。文法は大きく変化しないが「語り口」が日記・旅行記・ブログで変化する。
- 中英語期（~1200–1500年）：綴りの変動・語形変化（語尾の崩壊や語順固定化の途上）が著しく、語彙も大量入れ替わるため読解負荷が急増する。例：þ（thorn）やƿ（wynn）など消えた字形。
- 古英語（~1000年頃）以前：屈折語的な文法・語彙の差が大きく、現代英語話者には事実上別言語に近い。
- 技術的要点：
  - 正書法の標準化タイミングとGreat Vowel Shift（音韻変化）は書記系と発音の乖離を生み、OCRや音声合成で問題が出る。
  - 語彙の消失・意味変化（semantic shift）は語彙ベースの照合や単純な辞書引きでは対処困難。
  - モルフォロジーの簡略化（屈折の消失）は構文解析器の設計に影響する（古形対応が必要）。
  - 中世文字・記号（長s、特殊字）は正規化パイプラインでの前処理対象。

## 実践ポイント
- 歴史テキストを扱う技術者向け
  - 正規化（orthographic normalization）を最初に入れる：古綴り→近代綴りへマッピングしてから解析。
  - 時代情報をモデルに与える：diachronic embedding / time-aware language models を検討。
  - データ拡張：中英語・古英語コーパスでファインチューニング。Hugging Faceや古典コーパスを活用。
  - 特殊字・異字体はUnicode正規化＋ルール辞書で前処理。
- 言語学・ローカライズ実務向け
  - まずは逐次的に「近代英語→中英語→古英語」の短い抜粋を読んで慣れる。Middle English Dictionary / Bosworth–Toller（古英語辞典）がおすすめ。
  - 歴史文書プロジェクトでは、OCR後の人手校正と注釈付与を前提に工程を組む。
- 日本市場での応用
  - 歴史テキスト翻訳サービス、古文書のデジタル公開、教育コンテンツ（英語史入門）で需要あり。NLPスタートアップは「時代を跨ぐ正規化」機能を差別化に使える。

この記事を読めば、英語が「いつ」「どのように」読めなくなるかが感覚として掴め、歴史テキスト処理や時代差を考慮したNLP設計の実務的なヒントが得られます。
