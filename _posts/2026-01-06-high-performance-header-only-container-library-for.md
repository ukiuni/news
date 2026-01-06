---
  layout: post
  title: "High-performance header-only container library for C++23 on x86-64 - x86-64向けC++23 高性能ヘッダオンリーコンテナライブラリ"
  date: 2026-01-06T16:46:47.513Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/kressler/fast-containers"
  source_title: "GitHub - kressler/fast-containers: Performance focused header-only container library. Currently primarily contains a fast B+Tree implementation."
  source_id: 46512842
  excerpt: "AVX2とHugePageで10M要素を2–5×高速化するC++23ヘッダオンリーB+木"
  image: "https://opengraph.githubassets.com/aa62e87bca58489154798273920d8cc6705b6ee6b2527a5a1bb87fcb0e26c589/kressler/fast-containers"
---

# High-performance header-only container library for C++23 on x86-64 - x86-64向けC++23 高性能ヘッダオンリーコンテナライブラリ
魅力タイトル: 「10M要素で差が出る — AVX2＋HugePageで加速するC++向け高速B+木ライブラリ」

## 要約
kressler/fast-containers は、x86-64（AVX2）向けにチューニングされたヘッダオンリーのコンテナ群で、特に高速な B+Tree 実装と巨大ページ(hugepage)対応のプーリングアロケータを特徴とする。大規模データでの挿入/検索/削除が既存実装（Abseil の btree や std::map）より数倍高速になることが報告されている。

## この記事を読むべき理由
日本のサーバ／クラウド環境（大規模キャッシュ、インメモリDB、検索インデックスなど）ではTLBやキャッシュ効率が性能のボトルネックになりやすい。本ライブラリはSIMD検索と巨大ページプールでこれらの問題に直接アプローチしており、実運用でのレイテンシ改善やスループット向上の候補として注目に値する。

## 詳細解説
- コア構成要素
  - B+Tree (kressler::fast_containers::btree): キャッシュフレンドリー設計、SIMD（AVX2）検索、巨大ページ対応。
  - Dense Map: ノード内部で使う固定長ソート配列。
  - Hugepage Allocators: 単一サイズ / マルチサイズ / ポリシーベースのプール式アロケータを提供し、TLBミスと割付オーバーヘッドを削減。

- 性能面の要点
  - ベンチマークでは大きな木（例: 1,000万要素）で Abseil の btree や std::map に対して 2–5× のスピードアップを報告。ただし条件（キー/値サイズ、CPU、Linux+AVX2）に依存。
  - 速度源は主に (1) Hugepage による TLB ミス削減、(2) AVX2 を使ったノード内検索、(3) ノードサイズのチューニング。

- 設計上のポイント
  - デフォルトのノードサイズはキー/値サイズに基づくヒューリスティックで自動算出される。例えばリーフノードは概ね 2KB 相当を目指す:
    $$\text{LeafNodeSize} = \operatorname{clamp}\left(8,\,64,\,\text{round8}\left(\frac{2048}{\mathrm{sizeof(Key)}+\mathrm{sizeof(Value)}}\right)\right)$$
    内部ノードは約1KB:
    $$\text{InternalNodeSize} = \operatorname{clamp}\left(16,\,64,\,\text{round8}\left(\frac{1024}{\mathrm{sizeof(Key)}+\mathrm{sizeof(void*)}}\right)\right)$$
  - SearchMode によってノード内検索を線形・SIMD・二分探索で切替可能。SIMD はキー型が SIMD 互換（int32/64, uint32/64, float, double）で効果あり。
  - 現時点で Linux/x86-64（AVX2）でのビルド・テストが主。rdtscp 等で計測しているためベンチは x86-64 固有。

- 注意点
  - 効果は大規模データ（TLB ミスや割付コストが支配的なケース）で顕著。小規模データでは差が出ない可能性あり。
  - コンパイラ要件: C++23（GCC 14+/Clang 19+）、CMake 3.30+。AVX2 必須でない設定もあるが SIMD 効能は AVX2 に依存。

- API と互換性
  - インターフェイスは std::map に類似。insert/find/erase/iterate といった基本操作をサポート。
  - アロケータを差し替え可能で、複数ツリーで共有するポリシーベースのプールも使用可能。

## 実践ポイント
- まず動かす（最短手順）
  - 必要環境を確認（GCC14+/Clang19+, CMake 3.30+, AVX2 CPU）
  - サブモジュールとして追加し CMake に add_subdirectory で組み込む。
  - ヘッダをインクルードしてビルド（例: -mavx2 を有効にするビルド設定を確認）。
  - 参考コード（簡易）:
```cpp
// cpp
#include <fast_containers/btree.hpp>
#include <cstdint>
#include <iostream>

int main() {
    using Tree = kressler::fast_containers::btree<int64_t, int32_t>;
    Tree tree;
    tree.insert(42, 100);
    auto it = tree.find(42);
    if (it != tree.end()) std::cout << it->second << "\n";
}
```
- 性能検証の進め方
  - 実運用ワークロード（キー分布、値サイズ、同時スレッド数）で必ずベンチする。リーフ/内部ノードサイズはヒューリスティックだが、ワークロードに合わせて手動チューニングする余地あり。
  - HugePageAllocator を試す。HugePage を有効化できる環境（Linux カーネル設定、巨大ページの割当）で 3–5× の効果が期待できる。
  - TLB ミス、キャッシュミス、割付回数を perf / VTune 等で計測して効果を裏付ける。

- どんなケースで導入検討すべきか
  - メモリ上で数百万〜数千万のエントリを扱い、検索/挿入が頻繁でレイテンシやスループット改善が求められるシステム。
  - サーバ環境で HugePages が使える、かつ x86-64（AVX2）が利用可能なケース。

要点は「大規模データでのTLB／キャッシュを意識した実装」と「ヘッダオンリーで導入が容易」なこと。まずはローカルの代表的データセットで比較ベンチを取り、HugePage とノードサイズの効果を評価すると実践的な判断ができる。
