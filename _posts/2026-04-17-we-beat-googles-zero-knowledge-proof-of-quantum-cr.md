---
layout: post
title: "We beat Google’s zero-knowledge proof of quantum cryptanalysis - Googleの量子暗号解析に対するゼロ知識証明を破った"
date: 2026-04-17T16:17:08.390Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.trailofbits.com/2026/04/17/we-beat-googles-zero-knowledge-proof-of-quantum-cryptanalysis/"
source_title: "We beat Google’s zero-knowledge proof of quantum cryptanalysis - The Trail of Bits Blog"
source_id: 1381407045
excerpt: "Trail of BitsがGoogleのzkVM脆弱性を突き、量子コスト報告を改竄した"
image: "https://blog.trailofbits.com/2026/04/17/we-beat-googles-zero-knowledge-proof-of-quantum-cryptanalysis/we-beat-googles-zero-knowledge-proof-of-quantum-cryptanalysis-image-1.png"
---

# We beat Google’s zero-knowledge proof of quantum cryptanalysis - Googleの量子暗号解析に対するゼロ知識証明を破った
ZKの盲点を突くとこうなる：GoogleのzkVM実装を操って「証明」を改変した攻撃の中身

## 要約
Trail of Bitsが、Googleの公開した量子回路コストを報告するゼロ知識証明（zkVMゲスト）の実装上の未検証処理を突き、報告値を大幅に改善（偽造）する手法を示した。Googleはパッチを当て、論文の科学的主張自体は維持されている。

## この記事を読むべき理由
ゼロ知識証明は「検証可能な秘密処理」を実現するが、実装上の小さな安全欠陥が結果の完全性を壊し得る。日本のプロダクトや研究機関でもzkVMや外部バイナリ検証を使う場面が増えており、実運用での落とし穴を知ることは重要です。

## 詳細解説
- 基本概念：GoogleはSuccinct LabsのSP1 zkVM上で、量子回路（kickmixアセンブリ）をプライベート入力として与え、シミュレータが回路の正当性とリソース上限（総演算回数、Toffoli数、量子ビット数）を公表するゼロ知識証明を生成していた。検証は多数（$9,024$）のランダム入力でシミュレーションすることで高確率の正しさを担保する仕組み。
- 攻撃の狙い：zkVMゲストが外部から読み込む回路バイト列の「デシリアライズ時チェック抜き」を利用し、内部状態や列挙値（OperationType）を不正に操って「コストカウントのみ」をすり抜けさせる。具体的にはrkyvのaccess_uncheckedで検証を省略していた点を突く。
- コアの脆弱性：Rustのmatchがコンパイラ最適化で生成する2つのジャンプテーブル（1つはゲートカウンタ更新用、もう1つは実際の操作用）を逆手に取り、範囲外のop.kindで「操作は実行するがカウンタ増分を飛ばす」ようにジャンプさせることで、Toffoliカウント等を意図的に0近くに偽装できた。
- 実験的結果：Trail of Bitsはこの手法でGoogleの検証キーと互換なまま証明を作成し、報告資源を大幅に下げた（例：総演算回数を約 $8.3\times10^{6}$、Toffoliを $0$、量子ビット数を $1,164$ に改善した報告を実現）。Googleはパッチを公開して脆弱性を修正した。
- 周辺の課題：この手法は単なる「暗号の破れ」ではなく、zkVMやプロバー実装が持つ新たな攻撃面を示すもの。さらにレジスタエイリアシングや逆算（uncomputation）に関する論理ミスも攻撃拡張に利用可能だった。

コードの要点（問題箇所のイメージ）：
```rust
let private_circuit_bytes = sp1_zkvm::io::read_vec();
let ops = unsafe { rkyv::access_unchecked::<rkyv::Archived<Vec<Op>>>(&private_circuit_bytes) };
```

## 実践ポイント
- zkVMゲストやプロバーの入力は「未信頼データ」として厳密に検証する。access_unchecked相当は避けるか、外側で必ず検証を挟む。  
- unsafeや最適化依存の挙動がセキュリティ境界にあると危険。ジャンプテーブルやenum範囲外値の扱いを明確にする。  
- ゼロ知識の数学的整合性だけでなく、実装とバイナリレベルの監査（逆アセンブル、fuzz、サニタイズ付きビルド）を必須化する。  
- 日本の組織でzkや量子関係の検証を導入する際は、実装監査・第三者レビュー・パッチ適用の運用プロセスを整備する。

出典：Trail of Bitsブログ記事（元記事）を基に再構成。Googleは既に修正を行っています。
