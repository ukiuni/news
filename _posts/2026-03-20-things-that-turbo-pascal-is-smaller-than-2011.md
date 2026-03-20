---
layout: post
title: "Things That Turbo Pascal is Smaller Than (2011) - Turbo Pascal がより小さいものたち"
date: 2026-03-20T04:18:46.304Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://prog21.dadgum.com/116.html"
source_title: "Things That Turbo Pascal is Smaller Than"
source_id: 1029969158
excerpt: "39KBのTurbo Pascalを基準に現代ソフトの肥大化と高速実装の重要性を示す検証記事"
---

# Things That Turbo Pascal is Smaller Than (2011) - Turbo Pascal がより小さいものたち
魅惑のレトロ最適化：39KBのコンパイラが教える「実装する力」の大切さ

## 要約
1986年のTurbo Pascal 3.02（コンパイラ＋IDE）がわずか39,731バイトだった事実を起点に、現代のソフトや資産がいかに肥大化しているかを示す比較記事です。技術は目的ではなく、アイデアを素早く形にする能力が重要だと説きます。

## この記事を読むべき理由
現代の開発で「なぜ小さく高速なツールが価値あるのか」を理解できます。日本のスタートアップや組込み／IoT開発、ネットワーク制約のある現場では特に示唆に富みます。

## 詳細解説
- Turbo Pascal 3（MS-DOS、1986年）はコンパイラ＋エディタを統合し、ビルド速度が非常に速く、商用利用を意識した拡張が入っていました。実行ファイルは39,731バイト。
- 著者はこの「小ささ」を基準に、2011年時点でTurbo Pascalより大きい現代の例を列挙しています（いくつか抜粋）:
  - jquery 1.6（minified）: 90,518 bytes
  - yahoo.com ホームページ: 219,583 bytes
  - iPhone 4S の白画像（apple.com）: 190,157 bytes
  - Mac OS X Lion SDK の zlib.h: 80,504 bytes
  - OS X の touch コマンド: 44,016 bytes
  - Erlang パーサのコンパイル済モジュール erl_parse.beam: 286,324 bytes
  - Wikipedia の C++ ページ（HTML）: 214,251 bytes
- 主張の核心は「技術の規模そのものではなく、どれだけ早く、効率よくアイデアを実装できるか」。小さなツールは起動・ビルドが速く、フィードバックループを短縮します。

## 実践ポイント
- ビルド時間と成果物サイズを計測する（例: ビルドのwall time、生成バイナリのバイト数）。
- 配布物は最適化・ストリップ・圧縮（strip、upx、gzip/brotli）で小さくする。
- 依存を見直し、軽量ランタイムや最小ベースイメージ（Alpineなど）を検討する。
- プロトタイプ段階は「高速ビルド・小さなツール」を優先して反復を早める。
- 組込み／モバイル向けやネットワーク制約下では、資産サイズ削減が直接UX改善とコスト削減につながる。

（出典: James Hague, "Things That Turbo Pascal is Smaller Than", 2011）
