---
layout: post
title: "Garment Notation Language: Formal descriptive language for clothing construction - 衣服構築のための形式記述言語"
date: 2026-02-18T16:58:44.620Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/khalildh/garment-notation"
source_title: "GitHub - khalildh/garment-notation"
source_id: 47062329
excerpt: "GNLで服をコード設計し、サイズ多様化や設計→製造の高速化を実現する記述言語"
image: "https://opengraph.githubassets.com/be4ac3f38561e70ef73ef96ddfb8f7189a7c7101402ed0612e31815d1d3dca37/khalildh/garment-notation"
---

# Garment Notation Language: Formal descriptive language for clothing construction - 衣服構築のための形式記述言語
服を「コードで」設計する――GNLがもたらすパターン革命

## 要約
GNL（Garment Notation Language）は、人体基準の座標系・トポロジー・構築手順を持つ衣服記述言語で、記述だけであいまいさなく縫製可能な形に落とせることを目指しているプロジェクトです。

## この記事を読むべき理由
日本のアパレル産業やファッション×テックに関心がある人は、パターン設計のデジタル化・自動化、サイズ多様化対応、デザイン→製造の高速化に直結する技術としてGNLを知っておく価値があります。

## 詳細解説
- コア概念
  - Body-anchored：人体の解剖学的ランドマーク（例：@shoulder.L）や領域（%torso.front）を座標系に使い、パターンを体に対して定義する。
  - Topological：衣服を「境界と開口を持つ面」として扱い、パターンの連続性や端の扱いを明示できる。
  - Constructive：最終形だけでなく「組み立て順（BUILD）」を記述する。縫い合わせ順や仕上げ指示が言語で表現される。
  - Composable：複雑な衣服は単純要素の合成で表現できる（再利用性が高い）。
- 記法の一例（要旨）
  - FABRIC定義（例：M(160gsm, fluid, biaxial:15%, …)）
  - パーツ定義：front = P(%torso.front, contour, 1.15) のように領域・形状・係数でパネルを生成
  - BUILD命令：S(...), F(...) などで縫い・仕上げの順序を列記（例：S(front.shoulder, back.shoulder, serged) >> ...）
- 実装面
  - 文法はPEG（Peggy）で定義され、生成されるパーサが豊富に型付けされたASTを吐く。ランタイムでレンダラ用フォーマットに変換される。
  - リポジトリにはライブビューアがあり、左にGNLを入力すると右で組み上がり図とフラットパターンを同時に確認できる（縫い目、寸法、グレインライン等表示）。
  - Korostelevaデータセット用コンバータを同梱し、2DパネルJSONからGNLへ自動変換する機能がある（初回実行でテンプレートを自動取得）。
- 現状と注意点
  - 仕様は v0.2（ドラフト）で、グレイン、方向性イーズ、プリンセスシーム、裏地やコンポーネント合成の記述が導入済み。今後の現場フィードバックで精錬される段階。
  - ライセンス欄は "All rights reserved" とされているため、商用利用や転載時は注意が必要。

## 実践ポイント
- まずはライブビューアを触る：手を動かして記述→即レンダリングで理解が早い。
- ローカルで試す手順（短縮）
  - npm install
  - npm run generate（grammarからパーサ生成）
  - npm test（サンプルをパースして動作確認）
- 日本の導入シナリオ案
  - 既存のCAD／パターンDBとGNLを橋渡しする変換レイヤを作れば、工場とのデータ連携が進む。
  - オンデマンド縫製やパーソナライズ服のサイズ生成ループに組み込むと差別化要素になる。
- コントリビュートの勧め：仕様がドラフトのため、パターン設計者や縫製現場の知見をフィードバックすることで実用性を高められる。
