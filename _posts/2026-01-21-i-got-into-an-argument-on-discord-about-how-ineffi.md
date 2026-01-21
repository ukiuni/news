---
layout: post
title: "I got into an argument on Discord about how inefficient CBR/CBZ is, so I wrote a new file format - DiscordでCBR/CBZの非効率さを議論したら、新しいファイル形式を作ってしまった"
date: 2026-01-21T05:59:47.594Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://old.reddit.com/r/selfhosted/comments/1qi64pr/i_got_into_an_argument_on_discord_about_how/"
source_title: "I got into an argument on Discord about how inefficient CBR/CBZ is, so I wrote a new file format. It's 100x faster than CBZ. : selfhosted"
source_id: 865226195
excerpt: "CBZを100倍速くし重複削減も叶える新漫画形式BBF、変換ツールとライブラリ公開"
image: "https://preview.redd.it/eswczyx88jeg1.png?overlay-align=bottom,left&amp;crop=1200:628.272251309,smart&amp;overlay-height=15p&amp;overlay=%2Fwatermark%2Ft5_32hch.png%3Fs%3Dae52fa7e9db04a687279d0f5171d935dd0d79ffd&amp;width=1200&amp;height=628.272251309&amp;auto=webp&amp;s=1bb72544ac69655b733df8ef4afaba57aa9af9c1"
---

# I got into an argument on Discord about how inefficient CBR/CBZ is, so I wrote a new file format - DiscordでCBR/CBZの非効率さを議論したら、新しいファイル形式を作ってしまった
CBZを100倍速くすることを目指した「Bound Book Format（BBF）」登場 — 漫画アーカイブの常識が揺れるかも

## 要約
CBZ（画像群をZIPにした漫画ファイル）が抱える「ランダムアクセスの遅さ」「冗長な重複」「検証の遅さ」を解決するため、Zero‑copy／フッター索引／並列ハッシュなどを組み合わせた新フォーマットBBFが公開された。変換ツールとライブラリも公開済みで、自己ホスト漫画ライブラリやリーダーへの実装が期待される。

## この記事を読むべき理由
日本は世界屈指の漫画大国で、長期連載作品や大量の巻をローカルに保管する需要が高い。スマホや低消費電力の端末で「ページめくりが重い」「同じ画像が何度も保存されている」と感じたことがあるなら、BBFは実用的な改善案になる可能性が高い。

## 詳細解説
- CBZ/CBRの問題点（簡潔）
  - CBZは実態はZIP：ランダムアクセス時にアーカイブ全体を処理することが多く、ページ送り・シークでCPUが爆発的に使われる。
  - メタデータは外部ファイル（ComicInfo.xml）に頼ることが多く、フォーマット的に一貫性がない。
  - 同じ「表紙」「空白ページ」「スタッフ画像」が複数巻で重複保存され、ストレージを浪費する。
  - 整合性チェックが遅く、大規模ライブラリでの検証コストが高い。

- BBF（Bound Book Format）が狙う改善点
  - Zero‑Copyアーキテクチャ：ファイルを4KBアラインで配置し、ディスク上のデータを直接メモリ／GPUにマッピング（mmap）してコピーを排除。これにより読み出しのオーバーヘッドを大幅に削減。将来的にはDirectStorage（GPU直結型読み出し）との親和性もある設計。
  - フッター型インデックス：中央ディレクトリを逐次スキャンする代わりに、フッターのみ読めば各ページの位置が分かる構造で高速初期化が可能。
  - XXH3による並列ハッシュ：各アセットに対するXXH3ハッシュを並列に計算して高速に整合性チェックが可能。ページ単位の検証や全体検証が短時間で終わる。
  - コンテンツ重複排除（デデュープ）：同一画像を一度だけ保存して複数箇所から参照する方式で、長期連載や複数フォーマット混在でも容量削減が期待できる。
  - ネイティブメタデータ／章情報：XMLに頼らずフォーマット内にメタデータやチャプターを埋め込めるため、リーダー側での取り扱いが容易。
  - 非破壊性：画像はビット単位でそのまま保存し、再エンコードしない（画質劣化なし）。

- 実装・配布
  - コア実装（C++）とスペック、Pythonバインディング／CLIが公開されている（MITライセンス）。
    - C++: https://github.com/ef1500/libbbf
    - Python: https://github.com/ef1500/libbbf-python （pipで libbbf が入る）
  - 既存CBZ⇄BBFの双方向変換ツール（cbx2bbf, bbf2cbx）あり。既存のCBZ資産を失わずに移行できる。
  - 現状の課題：採用にはリーダー側の対応、エコシステム（仕様の明文化・標準スペック）が必要。開発者は仕様文書の整備や実装例を求めている。

## 実践ポイント
- まず試す（手順）
  - Pythonパッケージを使えばローカルで簡単に試せる：
```bash
# bash
pip install libbbf
cbx2bbf my_collection.cbz   # CBZをBBFに変換（ツール名はリポジトリ参照）
```
- 自分の環境でのベンチを取る：ページめくり／シーク時のCPU使用率と遅延、ライブラリ全体の整合性チェック時間、ディスク使用量の変化を比較する。
- 既存リーダーへ提案する：Tachiyomi派生、Komga、Calibre系、自己ホストのWebリーダーなどでBBFサポートの可能性を議論してみる。特に「重複排除」と「高速シーク」はユーザー体験向上につながりやすい。
- コントリビュート：リポジトリのスペック不足を指摘・補強したり、実装の互換試験や日本語文書化を手伝うと早期採用につながる。
- 導入判断の観点：大量の巻を持つか、低スペック機で閲覧するケースが多いか、既にCBZ中心のエコシステムに依存しているかを基に検討する。

まとめ：BBFは「漫画／マンhwaアーカイブの実用的な問題」をターゲットにした設計で、正しく実装・普及すればセルフホスト環境での体験を大きく改善する余地がある。まずはローカルでの試用と簡単なベンチから始め、コミュニティにフィードバックを送るのが現実的な一歩。
