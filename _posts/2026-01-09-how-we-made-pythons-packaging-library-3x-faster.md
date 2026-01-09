---
layout: post
title: "How we made Python's packaging library 3x faster - Python の packaging ライブラリを 3x 高速化した話"
date: 2026-01-09T22:08:08.040Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://iscinumpy.dev/post/packaging-faster/"
source_title: "How we made Python&#39;s packaging library 3x faster -"
source_id: 715087577
excerpt: "packagingの内部最適化でpipの依存解決が最大3倍高速化した手法"
image: "https://iscinumpy.dev/images/avatar.jpg"
---

# How we made Python's packaging library 3x faster - Python の packaging ライブラリを 3x 高速化した話
魅力的なタイトル: 「pip を速くする地味だけど劇的な改善 — packaging の内部最適化で体感速度が変わる理由」

## 要約
Python の packaging ライブラリ（pip が内部で使うライブラリ）をプロファイリングと小さな実装改善で大幅に高速化し、Version の読み込みが最大2倍、SpecifierSet の判定が最大3倍、filter はさらに速くなったという話。

## この記事を読むべき理由
packaging はほぼ全ての Python 環境に届くライブラリで、依存解決やバージョン判定のホットスポットです。CI や大規模プロジェクト、社内パッケージレジストリを使う現場では、ここが速くなるだけでインストール時間や解決時間が目に見えて短くなります。日本の開発現場でもパッケージ数が増えるほど恩恵は大きいです。

## 詳細解説
- 背景と重要性  
  packaging は PEP 440 準拠の Version、SpecifierSet、Marker、Requirement などを扱う基盤ライブラリ。pip に組み込まれて配布されるため、全世界の Python 利用者に影響します。依存解決中に何千回も Version を作ったり比較したりするので、ここが遅いと全体に波及します。

- 測定手法とデータ  
  開発者はまずプロファイリング（CPython 3.15 の統計サンプリングプロファイラを利用）し、PyPI の全メタデータ（数 GB の実データ）を使ったマイクロベンチで現実的な入力を再現しました。単純なベンチだけでなく、asv による履歴比較も実施しています。

- 主要な改善点（要点）  
  1. 正規表現の改善  
     - PEP 440 のパターンは巨大な正規表現で表現される。atomic/possessive 修飾を活用してバックトラックを減らすことで 10〜17% 程度の改善を得た（3.11+ の機能）。互換性のために後方対応も組み込んでいます。  
  2. 不要なデータ構築を削減  
     - 末尾ゼロを取り除く処理などでリスト・タプル生成を多用していた箇所をループベースに書き換え、実行速度を劇的に改善。pip の解決器では 40% 程度の改善例も。  
     - Version の比較用タプルをコンストラクタで毎回作るのではなく、初回比較時に遅延生成することで総コストを低減。  
  3. パーサと依存の整理  
     - pyparsing を止めて手書きパーサに置き換え（外部依存を減らす効果もあり）、パフォーマンスと安定性が向上。  
  4. キャッシュとアルゴリズムの調整  
     - SpecifierSet.filter で Version の再構築を避けるキャッシュを導入して約5x の高速化。  
     - canonicalize_name で正規表現置換をやめて str.translate を使い 2x 改善。  
  5. API レベルの微最適化  
     - functools.singledispatch の過剰使用を避け、ホットパスではシンプルな if/else に戻すことで数パーセント単位の改善を得た。

- 結果  
  packaging 26.0rc1 でこれらの改善が取り込まれ、Version の読み込みで最大 2x、SpecifierSet の判定で最大 3x の改善。実使用（pip の依存解決など）で体感できる速度向上が報告されています。

## 実践ポイント
- まずは自分の環境で計測する  
  - 単に「遅い」と感じたらプロファイラを当てる。CPython 3.15 の統計プロファイラは低セットアップで有用（リリース前なら類似ツールで代替）。asv で履歴比較を取ると変化が見やすい。  
- 使えるなら packaging / pip をアップデートする  
  - packaging 26 系や新しい pip を使うだけで恩恵が受けられる。CI イメージやビルド環境を最新化しておくと効果的。  
- 自分のコードでの応用例  
  - 頻繁に作るオブジェクト（例: Version 相当）は再利用・キャッシュする。  
  - 正規表現でバックトラックが疑われる場合は possessive/atomic 的な考え方で見直す（Python の機能や実装制約に注意）。  
  - 小さな文字列変換は re.sub より str.translate の方が高速なことが多い。  
  - シンプルな if/else はホットパスで侮れない（高抽象のコストを測る）。  
- すぐ試せるコード例（末尾ゼロ削除の速い実装）
```python
python
def _strip_trailing_zeros(release: tuple[int, ...]) -> tuple[int, ...]:
    for i in range(len(release) - 1, -1, -1):
        if release[i] != 0:
            return release[: i + 1]
    return ()
```

まとめ：大きなリファクタや言語アップグレードなしに、小さな実証的最適化（プロファイリング→問題の局所化→低レイヤの修正）で、エコシステム全体に効く改善が得られる好例です。日本のプロジェクトでも依存解決やインストール待ち時間を減らすために今すぐ取り入れられる知見が含まれています。
