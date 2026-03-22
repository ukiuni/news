---
layout: post
title: "Linking Smaller Haskell Binaries - 小さな Haskell バイナリのリンク"
date: 2026-03-22T09:07:31.120Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://brandon.si/code/linking-smaller-haskell-binaries/"
source_title: "Linking Smaller Haskell Binaries | Brandon Simmons&#39; website"
source_id: 47432789
excerpt: "リンク時オプションでHaskell実行ファイルを100MB級から64MBへ削減する具体的手法を解説"
---

# Linking Smaller Haskell Binaries - 小さな Haskell バイナリのリンク
Haskellの巨大バイナリを一気に小さくするリンク時テクニック（100MB級→64MBの実例付き）

## 要約
GHCで生成される大きな実行ファイルを、リンク時のオプションで大幅に削減する手法を紹介。主にセクション分割＋GCで未使用コードを削る方法と、実験的な同一コード折り畳み（ICF）を組み合わせた例を示す。

## この記事を読むべき理由
Haskellプロジェクト（特に依存関係が多いもの）ではバイナリ肥大が悩みの種。ビルド配布やコンテナ化、CI実行時間、デバッグ体験に直結するため、簡単に試せる最適化手法は日本の開発者にも実務的価値が高い。

## 詳細解説
- 問題点：多くのトランジティブ依存でセクションごとのコードが重複し、strippedでも100MB級になることがある。
- 基本対策（安全で効果大）：
  - GHCに小さなコード単位で出力させる：-split-sections
  - リンカで未使用セクションを削除：--gc-sections
  - Cコード側も節分割（効果は限定的）：-fdata-sections -ffunction-sections
  - 高速でICFが得意なリンカとしてlldを指定：-fuse-ld=lld
  - 実例：stripped前後で113MB→83MB（約-27%）
- 実験的手法（更に削るが注意）：
  - Identical Code Folding（ICF）で機能的に同一なセクションを結合：--icf=all 等
  - 注意点：Cのポインタ等で「等価性」に依存するコードやデバッグ情報が折り畳まれると問題になる可能性がある。実例で83MB→64MB（さらに-23%）。
- デバッグ／プロファイリングとの相互作用：
  - -fdistinct-constructor-tables などの情報テーブルが折り畳まれるとプロファイル／デバッグに支障が出る。情報テーブルをGCルート扱いにする制御が必要になる場合がある。
- ツール互換性：bloatyやkcovはHaskellバイナリで問題が出ることがあるため検証に制約あり。
- 将来の示唆：コンパイル中に早期に重複を検出してキャッシュすることでコンパイル時間と最終バイナリ両方を改善できる可能性がある。

## 実践ポイント
- cabal.project等に最低限これを追加して試す（lldを使う前提）:
```ini
package *
  ghc-options: -split-sections
  gcc-options: -fdata-sections -ffunction-sections

package pandoc
  ghc-options: -split-sections
  ld-options: -fuse-ld=lld -Wl,--gc-sections,--build-id
```
- さらに試す（実験的、注意してテストを回す）:
```ini
ld-options: -Wl,--icf=all,--ignore-data-address-equality,--ignore-function-address-equality,--print-icf-sections
```
- 実行前に必ずテストスイートを通すこと（ICFは安全とは限らない）。
- デバッグやプロファイリングが必要なビルドではICFやgc-sectionsを外すか、情報テーブルの扱いを確認する。
- コンテナや配布サイズを抑えたい場合はまず-gc-sections＋lldを推奨、その後ICFを慎重に評価する。

以上。
