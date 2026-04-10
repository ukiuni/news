---
layout: post
title: "Parsing 11 languages in pure Go without CGO: replacing regex with a tree-sitter runtime - CGO不要で純Goで11言語をパース：正規表現を置き換えたtree-sitterランタイム"
date: 2026-04-10T17:06:23.144Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://glinr.hashnode.dev/parsing-11-languages-in-pure-go-without-cgo-how-i-replaced-regex-with-a-tree-sitter-runtime"
source_title: "Parsing 11 languages in pure Go without CGO: replacing regex with a tree-sitter runtime"
source_id: 365054950
excerpt: "CGO不要の純Goでtree-sitter実装、正規表現を捨て11言語を高速正確にパース"
---

# Parsing 11 languages in pure Go without CGO: replacing regex with a tree-sitter runtime - CGO不要で純Goで11言語をパース：正規表現を置き換えたtree-sitterランタイム
魅力的タイトル：正規表現を捨てて安全に高速化──CGO不要の純Go tree-sitterで11言語をパースした話

## 要約
著者は、従来の正規表現ベースの解析をやめ、tree-sitterの考え方を取り入れた「CGOを使わない純Goランタイム」を作って11言語をパースできるようにした。クロスコンパイル性や堅牢な構文解析が得られ、実運用での利点が大きい。

## この記事を読むべき理由
日本の現場でも、静的解析ツール・コード検索・IDE拡張・CIでのバイナリ配布など、CGOを避けて単一バイナリで動かしたいニーズが増えています。本件は「安全で配布しやすい形で複数言語を解析する実装戦略」を示しており、実装や導入を検討する価値があります。

## 詳細解説
- tree-sitterとは：構文木（AST）を高速に生成し、増分パースやクエリ（tree-sitter query）でノードを抽出できるモダンなパーサー基盤。もともとはCでランタイムが提供される。
- 問題点：公式の多くのバインディングはCランタイムを使うためCGO依存になり、staticビルドやクロスコンパイル、軽量な配布に障害が出る。
- 解決のアイデア：ランタイムAPIを純Goで再実装する、もしくは文法（grammar）を中間表現に変換してGoで解釈することでCGOを排除。これにより以下が可能に：
  - 単一の静的バイナリで多言語解析を配布
  - Goのメモリ安全性とGC管理の恩恵
  - CIやサーバレス環境での容易な実行
- 技術的ポイント：
  - 文法の取り込み方法：既存のtree-sitter文法（JSONや生成済み構造）を読み込み、純Goランタイムが扱える形に変換する手順が必要。
  - 増分パース：変更差分だけ再計算する機構を実装すれば、IDE的なフィードバックや高速な解析が可能。
  - クエリ互換性：tree-sitterのquery言語に対応すると、既存の抽出ルールを流用できるため移行コストが下がる。
  - パフォーマンスとメモリ：手作業の最適化でCランタイムに近づけられるが、ケースによっては微調整が必要。
- 正規表現からの利点：
  - 正規表現は多言語・入れ子構造・コメント混在などに弱い。構文木ベースなら正確にノード単位で抽出可能。
  - 複雑な言語機能（テンプレート、マクロ、埋め込み言語）にも対応しやすい。

## 実践ポイント
- まず既存のツールで試す：sergi/go-tree-sitterなどのGoバインディング（CGO有無を確認）でPoCを作る。
- CGO不要を本気で狙うなら：純Goランタイムを探すか、文法を中間形式に変換して解釈するアプローチを採る。
- 増分パースを採用：IDEや高速CI用途なら差分解析を実装してレスポンスを改善する。
- migration計画：既存の正規表現ルールはtree-sitter queryに置き換えられるかを検証し、段階的に移行する。
- 日本の現場用途：大規模リポジトリのコード検索、言語横断の静的解析、CIでの単一バイナリ運用、VSCode拡張などに適用可能。

短く言えば、CGOを使わない純Goのtree-sitterランタイムは「配布・運用のしやすさ」と「正確な構文解析」を両立する実務的な選択肢です。導入前に既存バインディングとのトレードオフをベンチマークしてみてください。
