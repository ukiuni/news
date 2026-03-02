---
layout: post
title: "An Introduction to Folios - フォリオ入門"
date: 2026-03-02T15:47:24.002Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blogs.oracle.com/linux/intro-to-folios"
source_title: "An Introduction to Folios"
source_id: 392757688
excerpt: "フォリオでページ管理を一新し、LinuxのI/O・TLB効率とメモリ回収を劇的改善"
image: "https://blogs.oracle.com/linux/wp-content/uploads/sites/49/2025/10/tree.jpg"
---

# An Introduction to Folios - フォリオ入門
メモリ管理を再定義する「フォリオ」：カーネル性能とメモリ効率が一気に改善する理由

## 要約
フォリオ（folio）は、従来のページ管理（struct page）を置き換え、複数ページをまとめて扱える新しいメモリ記述単位で、I/Oスループットやリクレイム性能、TLB効率を劇的に改善します。導入はLinux 5.16以降で段階的に適用されています。

## この記事を読むべき理由
日本のサーバ／クラウド環境（ARM系サーバやNVMe大量IOを使うケース、メモリ大容量インスタンス）で、カーネル側の微妙な最適化が実運用のスループットやコストに直結します。フォリオはその基礎を変える技術なので、現場のパフォーマンス改善や将来の設計判断に役立ちます。

## 詳細解説
- 背景：ハードウェアは「物理ページ（base page）」単位でメモリを扱う。カーネルは各物理ページに対してstruct page（従来64バイト相当）でメタデータを持つため、大容量メモリ環境では説明用のメモリが無視できない割合を占める。
- 問題点：物理的に連続した大きな領域（huge pages等）を扱うときは複数のstruct pageをまとめて「compound page（head/tail）」にするが、関数呼び出し側はheadかtailか判定する必要がありオーバーヘッドが発生する（compound_head()の参照コスト）。
- Ottawa解釈（性能寄り）：folioは「その構造体が単一ページか、必ずheadページである」ことを保証するデータ構造。これによりcompound判定コストが消え、カーネルコンパイルで約7%向上などの効果が観測された。さらにページキャッシュやリクレイムが大きな単位（large folio）で動けるため、I/Oやメモリ回収のスループットが大幅改善（実装報告で24%〜241%の改善例）。
- mTHP（multi-size THP）：ARMやx86の複数ページサイズを効果的に使えるようになり、TLBミス削減で5%〜20%の性能改善に寄与。folioはサイズ変更や分割を自然にサポートするのでmTHP実現を容易にする。
- New York解釈（メモリ削減寄り）：struct page自体を小さなメモリ記述(memdesc、8バイト相当)に置き換え、物理的連続範囲ごとに少ないオブジェクトで済ませることでstruct page領域を大幅削減（最大で約87.5%の構造体サイズ削減ポテンシャル）。ただしkernel内部の全種別メモリへ展開するには段階的対応が必要。

コード例（従来の問題を示す簡単なイメージ）:
```c
void do_something_with_phys_mem(struct page *page) {
    /* 'page' が head か tail か不明 */
    struct page *head = compound_head(page);
    ...
}
```

## 実践ポイント
- 確認：まずカーネルバージョンを確認（uname -r）。folio関連の恩恵はLinux 5.16以降、ページキャッシュ改善は5.18での取り組みが鍵。
- 検証：自分のワークロードでfio（I/O）、memtierやアプリのベンチを使い、カーネルアップデート前後でスループットとレイテンシを比較する。
- ARM環境注意点：Amazon Gravitonや国内ARMサーバでは複数ページサイズの恩恵が大きいので、mTHPやTHP設定を試す価値あり。
- モニタリング：vmstat, /proc/meminfo, perf (TLB miss), iostat を使い、ページキャッシュ/リクレイム周りの挙動変化を観察する。
- 実運用導入は段階的に：ディストリやカーネルパッチの安定性を確認しつつ、カーネルアップをステージング→本番へ移行する。

以上。フォリオは「同じメモリをより賢く扱う」ための基盤改良で、多くの現実的な性能改善をもたらします。
