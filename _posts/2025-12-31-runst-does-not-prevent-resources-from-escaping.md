---
layout: post
title: "runST does not prevent resources from escaping - runSTはリソースの漏出を防がない"
date: 2025-12-31T07:38:36.347Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://welltypedwit.ch/posts/runst-does-not-prevent-resources-from-escaping.html"
source_title: "runST does not prevent resources from escaping"
source_id: 1547729347
excerpt: "runSTでsを隠してもポインタは漏れ、use-after-freeを招く危険性と対策を解説"
---

# runST does not prevent resources from escaping - runSTはリソースの漏出を防がない
思っているほど「安全」じゃない？runSTトリックの落とし穴と実務への示唆

## 要約
Haskellの有名な「runSTトリック」は、参照やポインタが「外へ出る」ことそのものを型で禁止するわけではない。高階ランク型で作られる型タグは「同じrunST呼び出し内でのみアクセス可能」という保証を与えるが、実際にはリソース自体を外に漏らすことは可能で、存在型（あるいは同等のランク化パターン）を使えばuse-after-freeが発生する。

## この記事を読むべき理由
HaskellやFFIを使う日本のエンジニアにとって、runSTや地域（region）風の設計を安全だと過信すると致命的なバグ（メモリ破壊・use-after-free）を招く可能性がある。ライブラリ設計や安全なFFIラッパー作成の際に役立つ実践的な知見が得られる。

## 詳細解説
- runSTの仕組み
  - runST :: (forall s. ST s a) -> a の形で、sという型パラメータを高階で普遍的にしている。
  - これにより、STRef s のような内部参照は型レベルで「どのrunST呼び出しか」をタグ付けされ、異なるs間で混同されないため、純粋性の保証が保たれる。
- でも「漏出」は可能
  - 型システムは確かに「別のsでアクセスする」ことを防ぐが、値（例えばポインタ）を外側に返す（漏らす）こと自体は不可能にしていない。重要なのは「返した後にそれを安全に操作できるか」。
  - 存在型（existential）や、それと等価な高ランク型のトリックを使えば、内部で生成したs付きのリソースを外に包んで持ち出せる。たとえば SafePtr s a を existential に包むと、sが隠蔽されて外へ出せる。
- 実際の問題の再現
  - alloca系の安全ラッパを作り、SafePtrでsを添付して高ランクで限定しようとする。しかし MkNotSoSafePtr のように s を隠すと、alloca のスコープを抜けた後に poke すると use-after-free を起こす（ValgrindでInvalid write / free'd block の証拠が出る）。
- runSTが保証している「本当のこと」
  - runSTが保証するのは「そのsタグに紐づくSTRefは、生成された同一のrunST実行内でしか操作できない」こと。生成された値自体が外へ出ることを防いでいるわけではない。型タグは一意性を与えるが、値の流れを封じる万能の盾ではない。

## 実践ポイント
- API設計で「sを隠せば安全」は誤り
  - region風APIやランタイムリソースを型でラベル付けしても、存在型的に包むことが可能なら安全は破れる。外部に渡す値は必ずライフタイム管理（bracket/with系）で厳密に制御する。
- FFIでのポインタ管理は特に慎重に
  - alloca / malloc / free のラッパーは、外へ持ち出される可能性を想定して設計する。ForeignPtr + finalizer、withForeignPtr/with* パターンを優先する。
- 型レベルの対策
  - 単純な高ランク型ではなく、より強力な手段（線形型、region型ライブラリ、依存型的な証明）を検討する。GHCのLinear Typesやregionライブラリを使うと誤用を減らせる。
- コードレビューと動的検査
  - ランタイムでValgrindやASANを使った検査をCIに組み込む。型だけに依存せず、実行時の検証を行う習慣をつける。
- 小さなルール
  - 「S付き型を隠蔽して外に返すラッパーはレビュー必須」とルール化する。
  - alloca系の戻り値は純粋に使い切る（callback内完結）か、持ち出すならコピーを作る。

