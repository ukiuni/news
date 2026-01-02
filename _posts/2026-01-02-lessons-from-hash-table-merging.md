---
  layout: post
  title: "Lessons from hash table merging - ハッシュテーブルのマージから得られる教訓"
  date: 2026-01-02T05:12:40.451Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://gist.github.com/attractivechaos/d2efc77cc1db56bbd5fc597987e73338"
  source_title: "2026-01-01_hashmap-merge.md · GitHub"
  source_id: 473179318
  excerpt: "ハッシュマップのマージで起きる10倍遅延の原因と即効3解法を実測で示す"
  image: "https://github.githubassets.com/assets/gist-og-image-54fd7dc0713e.png"
---

# Lessons from hash table merging - ハッシュテーブルのマージから得られる教訓
ハッシュマップのマージで「10倍遅くなる」原因と、実用的にすぐ使える3つの対処法

## 要約
ハッシュテーブル同士のマージは一見 $O(N)$ の単純な処理だが、同じハッシュ関数を使うと「原始的なクラスタリング（primary clustering）」で極端に遅くなる。記事は実測と解析を通してその原因を示し、塩（salt）付きハッシュ、事前確保、ストライド走査という3つの現実的解を比較している。

## この記事を読むべき理由
大規模データ処理や分散集約、ログ集計、インメモリ集計などでハッシュマップのマージは頻出。特に日本のプロダクトでも数百万〜数千万キーの統合は珍しくないため、知らないとパフォーマンスの激しい劣化を見落とす。ライブラリ選定や実装上の簡単な対処で劇的に改善できる点は必読。

## 詳細解説
実験概要
- splitmix64 で生成した乱数キーを使い、サイズ N のテーブル h0 に 2N のキーを持つ h1 をマージする測定を実施（N は数百万〜数千万）。
- 比較対象は Swiss Table（Abseil/Boost/Rust等）、Robin Hood（unordered_dense）、単純線形探索（khashl）など。

問題の本質
- 典型的なイテレータはテーブル内をハッシュ順（バケット順）に巡回する。h0 と h1 が同じハッシュ関数を使うと、h1 におけるキーの元のバケット位置と h0 の挿入位置が一致し、マージ時にテーブル前方が偏って埋まる。
- これにより部分的に高負荷な領域が生成され、衝突が増え、線形探索系では探査コストが跳ね上がる（“primary clustering”）。結果、作成（空テーブルへ挿入）と比較して 10〜20x の遅延が観測された実装もある。

提案された解法（3つ）
1) Salted hasher（インスタンスごとのシード）
- 各ハッシュテーブルインスタンスにランダムシードを混ぜてハッシュ値を変える。これにより同じキーでもテーブル間で初期バケット位置がずれるため、偏りを防げる。
- Abseil は既にこの手法を採用しているためマージでの劣化を回避できる。
- 簡易ラッパー例（C++）:

```c++
class RandHasher {
    size_t seed;
public:
    RandHasher() {
        std::random_device rd;
        seed = std::uniform_int_distribution<size_t>{}(rd);
    }
    size_t operator()(uint64_t x) const {
        return hash64(x ^ seed); // 既存の hash 関数にシードを混ぜる
    }
};
```

2) Preallocation（事前確保）
- h0 をマージ前に h0.size + h1.size 相当まで reserve／rehash しておく。バケットが十分に空いていればマージ中の偏りは発生しにくい。
- メモリコストが上がるが、重複（key overlap）が少ない状況では最速の手法。

3) Stride iteration（非線形イテレーション）
- イテレータでバケットを単純に隣接巡回せず、ステップサイズ（stride）を使って全バケットを巡回する。例えばステップ7で素なバケット数と互いに素ならば全バケットを一周できる。
- これによりマージ時の挿入順が実質ランダム化され、クラスタリングを回避できる。ライブラリ内部の実装変更が必要なため適用は難しいが効果は高い。

その他
- 二次探査（quadratic probing）は入力順に対してやや頑健だが、前述3解のいずれほど効果的ではない。
- テーブルをシャーディングして小さいサブテーブルごとに処理する手もあるが根本解決にならない場合が多い。

## 実践ポイント
- まずはライブラリ選び：Abseil のようにインスタンスごとのシードを持つ実装はデフォルトで安全。高パフォーマンスが必要ならベンチを取る。
- すぐできる対応順（低コスト→高効果）:
  1. マージ前に h0.reserve(h0.size() + h1.size()) を行う（最も単純で効果的）。
  2. 独自ハッシュを使う場合はテーブルごとにランダムシードを混ぜる（salted hasher）。
  3. ライブラリを改変できるなら stride/非線形イテレータを検討する。
- キーの重複率が高いワークロードでは事前確保がメモリの無駄になるので注意。必ず実データでプロファイルすること。
- 大規模バッチマージでは、マージ順序（ランダム化）やシャッフルを挟むだけで改善することがある。

## 引用元
- タイトル: Lessons from hash table merging  
- URL: https://gist.github.com/attractivechaos/d2efc77cc1db56bbd5fc597987e73338
