---
layout: post
title: "A Unique Performance Optimization for a 3D Geometry Language - 3Dジオメトリ言語における独自の実行高速化"
date: 2026-01-11T09:07:39.283Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://cprimozic.net/notes/posts/persistent-expr-memo-optimization-for-geoscript/"
source_title: "A Unique Performance Optimization for a 3D Geometry Language :: Casey Primozic&#39;s Notes"
source_id: 1138494168
excerpt: "Geoscriptが式評価を永続キャッシュ化し、900ms級処理もライブ再実行で即時化"
image: "https://cprimozic.net/notes/img/favicon/green.png"
---

# A Unique Performance Optimization for a 3D Geometry Language - 3Dジオメトリ言語における独自の実行高速化
Geotoy開発者が見つけた「実行結果を丸ごと次回に持ち越す」超実用的最適化

## 要約
Geoscript（Geotoy向けの3Dジオメトリ言語）は、実行中に評価した「定数表現」の結果をハッシュでメモ化し、それを複数回の実行で永続化することで、ライブコーディング時の再実行コストを劇的に削減する最適化を導入した。

## この記事を読むべき理由
ライブで形を試行錯誤するWebベースの3Dツールや、プロトタイプを頻繁に再実行するワークフローは日本でも多い（ゲーム、CG、点群処理、プロダクトデザイン等）。小さなコード変更で重い処理を毎回走らせる非効率を解消する実践的テクニックで、類似ツールや自作のスクリプト言語にも応用可能だから。

## 詳細解説
背景
- Geoscriptは外部入力がほぼ無く、乱数はシード固定という性質上、プログラムは「引数ゼロの純粋関数」に近い。これが最適化の余地を大きくしている。

既存の最適化
- 定数畳み込み（constant folding）: AST上で定数計算を畳み込み、可能な限りリテラルに置き換える。
- CSE（共通部分式消去）を狙った構想: ASTノードを構造的にハッシュ化して同型ノードを検出する。著者はノードを決定的に u128 にハッシュする実装を行った。

重要なアイデア — 実行時メモ化の永続化
- 実行時に評価した「完全に定数な式」の値をメモ化（expr cache）し、ブラウザやローカルストレージなどに永続化して次回実行時に再利用する。
- ライブコーディングでは大部分のコードが同じまま少しずつ変わるため、変更されていない式は前回の評価結果をそのまま利用できる。
- 例: 高コストな alpha_wrap（CGAL由来の複雑なメッシュ生成）が毎回900msかかるケースでも、簡単なパラメータ調整だけならこの呼び出しはキャッシュヒットして再実行不要になる。

PRNGへの対応
- RNG呼び出しは状態を変えるため通常は非定数扱いだが、Geoscriptでは「RNG初期状態」をキャッシュキーに含めることで、乱数を含む式も再利用可能にしている。
- 本質的に、乱数呼び出しを $$f: (\mathrm{rng\_state}) \mapsto (T, \mathrm{new\_rng\_state})$$ と扱うことで決定性を保つ。

仕組み（概念）
- 各ASTノードに対して構造ハッシュ H(node) を計算。
- 実行時に key = combine(H(node), snapshot_of_relevant_env, rng_state_if_used) を作り、ディスク/DB上のキャッシュを参照。
- ヒットすれば値をcloneして返し、ミスなら評価して結果を挿入。

簡易的な式（説明用）
$$
\text{key} = H(\text{node}) \oplus H(\text{captured\_consts}) \oplus H(\text{rng\_state})
$$

類似性
- ビルドキャッシュ（Nix/Bazel）と同じ発想で、中間生成物ではなく「式の評価結果」を保存している点がユニーク。

## 実践ポイント
- ASTの安定ハッシュを作る: ノードの種類、順序、引数、リテラル値を含めて決定的なハッシュを生成する。
- キャッシュキーに「環境スナップショット」を含める: クロージャが捕捉する定数やモジュールバージョンなど。
- RNGを使う場合は初期シード／内部状態をキーに含め、順序依存性を厳密に保つ。
- 永続化方法: ローカルファイル、IndexedDB、ユーザ毎のキャッシュディレクトリ等を検討。大きなバイナリ（メッシュ）は参照カウントや差分保存が有効。
- 無効化戦略: ソースの依存関係解析で「変更が影響するノード」を特定して部分的に無効化するのが望ましい（全消しは非効率）。
- 注意点: 副作用のある関数、外部I/O、非決定的APIはキャッシュしない／別扱いにする。

参考にする価値
- ライブコーディングや反復的なデザイン作業をするプロダクトにとって、今回の手法は非常に実用的。既存のインタプリタ／パイプラインにも比較的低コストで導入できる技術であり、日本のツール開発者や研究者にも有用なアイデアとなるはずだ。
