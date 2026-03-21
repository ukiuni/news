---
layout: post
title: "jsongrep is faster than {jq, jmespath, jsonpath-rust, jql} - jsongrepは{jq, jmespath, jsonpath-rust, jql}より高速"
date: 2026-03-21T21:40:37.571Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://micahkepe.com/blog/jsongrep/"
source_title: "jsongrep is faster than {jq, jmespath, jsonpath-rust, jql}"
source_id: 376884852
excerpt: "DFAでJSONを一度だけ走査しjqより高速に検索するjsongrepを試す理由"
---

# jsongrep is faster than {jq, jmespath, jsonpath-rust, jql} - jsongrepは{jq, jmespath, jsonpath-rust, jql}より高速
DFAでJSONを一回だけたどる――超高速JSON検索ツール「jsongrep」を試すべき理由

## 要約
jsongrepはクエリを事前に有限オートマトン（DFA）にコンパイルし、JSONツリーを一度だけ走査してパス一致を行う検索ツール。解釈実行型のjq等より高速になることをベンチマークで示している。

## この記事を読むべき理由
大量ログや大きなJSONレスポンスを日常的に扱う日本の開発者にとって、検索コストを下げる方法は即効の生産性改善につながる。特にクラウド監視・コンテナログ・APIバッチ処理の現場で有益。

## 詳細解説
- 基本概念：JSONはツリー（オブジェクト／配列が分岐、スカラが葉）で、クエリは「ルートから葉へのパス」を記述する言語と見る。jsongrepはこの言語を正則言語として扱う。
- パイプライン（要点）
  1. JSONをツリーとしてパース（zero-copy）。
  2. クエリ文字列をASTに解析。
  3. Glushkovの構成で$\epsilon$を持たないNFAを生成（ε遷移が無いのが利点）。
  4. 部分集合構成でNFAをDFAに決定化。
  5. DFSでツリーを一度だけたどり、各辺でDFAの遷移を1回（$O(1)$）実行してマッチを収集。
- なぜ速いか：DFAは各入力シンボルに対して固定時間の遷移しか行わないため、クエリの評価コストは探索前に一度だけ（コンパイル）払い、検索は単一パスで済む。対してjqやjmespath系はクエリを走査時に逐次解釈・再帰処理するため、再訪問やワークリストの維持が発生しがち。
- 技術的コア：Glushkovの構成によりNFAはεフリー、これが部分集合構成で効率的に決定化できる要因。また実装上はクエリに現れないキー用の“Other”記号を導入して不要探索を早期に切る工夫がある。
- 制約（アンチピッチ）：jqほど表現力は高くない（変換・フィルタや演算は不可）。jsongrepは検索特化で、変換を行いたい場面ではjq等が適切。

## 実践ポイント
- 典型的用途：巨大ログ(JSONL)、Kubernetesイベント、APIバルクレスポンスから特定のキー/値を高速に抽出する場面に最適。
- クエリ例（イメージ）："roommates[*].name" のようなドット区切り、ワイルドカード、繰り返し、選択が使える。
- パフォーマンス確認：著者は複数ツールと大規模データセットで比較し、jsongrepがエンドツーエンドで有利と報告。
- 導入：Rust製でクロスプラットフォーム。試すなら `cargo install jsongrep`（環境による）。まずは読み取り専用の検索用途で検証し、既存ワークフロー（jq等の変換処理）と使い分けるのが現実的。

この記事は「検索を高速化したいが、変換までは不要」というケースに強く刺さる。まずは手元の大きなJSONに対して簡単なクエリで性能差を確かめてみるとよい。
