---
layout: post
title: "Turing Completeness of GNU find: From Mkdir-Assisted Loops to Standalone Computation - GNU find のチューリング完全性：mkdir補助ループから単独計算へ"
date: 2026-02-25T08:46:12.193Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arxiv.org/abs/2602.20762"
source_title: "[2602.20762] Turing Completeness of GNU find: From mkdir-assisted Loops to Standalone Computation"
source_id: 47147609
excerpt: "GNU findがmkdirや正規表現でチューリング完全性を実現、CIとセキュリティに警鐘"
image: "/static/browse/0.3.4/images/arxiv-logo-fb.png"
---

# Turing Completeness of GNU find: From Mkdir-Assisted Loops to Standalone Computation - GNU find のチューリング完全性：mkdir補助ループから単独計算へ
あなたの端末に潜む“計算機性”──標準ツール find が本格的な計算モデルになってしまう話

## 要約
GNU find（特に 4.9.0 以降）は、mkdir の併用や正規表現の裏技を使うことでチューリング完全性を示せる――つまり理論上どんな計算でも表現できる、という驚きの結果を著者が示しています。

## この記事を読むべき理由
日本の多くの現場で日常的に使われる find が、単なるファイル検索ツールを超えて非常に強力かつ危うい表現力を持つことは、セキュリティ、CI／CD、スクリプト設計で即座に影響します。ツールの安全な使い方や検証の観点が変わります。

## 詳細解説
- 論文は三つの主張で構成されています。
  1. find + mkdir の組合せでチューリング完全：ディレクトリパスに計算状態をエンコードし、正規表現のバックリファレンスで文字列コピーを再現。これにより 2-tag system をシミュレート。
  2. GNU find 4.9.0+ 単独でチューリング完全：走査中にファイルの読み書きを組み合わせれば、二つのカウンタを持つ機械（two-counter machine）を模倣可能で、mkdir を使わなくても普遍性を達成。
  3. mkdir を使うがバックリファレンス無しでも可：ディレクトリ名自体に正規表現のパターンを埋め込むトリックで同等の表現力を実現。
- キーポイントは「状態をファイル／ディレクトリ構造で表現すること」と「find の条件式（-regex, -exec, バックリファレンスなど）の組合せ」で、これらで状態遷移とメモリ操作を模倣する点。
- 理論的には 2-tag system や two-counter machine は既知の普遍モデルで、これらをシェルユーティリティでエンコードできることが普遍性の証明につながります。

## 日本市場との関連性
- 多くの日本企業のサーバや開発環境は Linux ベースで、find は運用スクリプトや CI ジョブに深く組み込まれています。想定外の表現力は誤用や悪用（難読化された攻撃スクリプト、ヤバいワンライナー）の温床になり得ます。
- コンテナ／ビルド環境での権限設計や静的解析、CI の安全なルール整備にこの知見を反映する価値があります。

## 実践ポイント
- find のバージョンを確認する（例: find --version）；4.9.0+ の挙動は要注意。
- 不審な find コマンドや外部由来の -exec/-regex をそのまま流用しない。入力は必ずサニタイズする。
- CI やスクリプトは最小権限・コンテナ隔離で実行し、find の深いオプションを無制限に使わせないポリシーを検討する。
- 興味がある人は論文を読み、具体的な実装トリック（パスエンコーディング、バックリファレンスの利用法）を学ぶと、セキュリティ評価やツール改善に役立つ。

（参考：Keigo Oka, "Turing Completeness of GNU find: From Mkdir-Assisted Loops to Standalone Computation", arXiv:2602.20762）
