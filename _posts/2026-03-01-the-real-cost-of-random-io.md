---
layout: post
title: "The real cost of random I/O - ランダムI/Oの真のコスト"
date: 2026-03-01T13:16:43.170Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vondra.me/posts/the-real-cost-of-random-io/"
source_title: "The real cost of random I/O - Tomas Vondra"
source_id: 47165230
excerpt: "Postgresのrandom_page_costはSSDでも約25前後、誤設定で性能が激減する。"
---

# The real cost of random I/O - ランダムI/Oの真のコスト
SSD時代でも要注意：Postgresの「random_page_cost」は本当に4でいいのか？

## 要約
Postgresのデフォルト設定 random_page_cost = 4.0 は古い前提に基づいており、実測ではローカルSSDで約25〜35、クラウドやリモートストレージではさらに大きくなることがある。コスト設定を誤るとプラン選択が大幅にズレ、パフォーマンス被害が出る。

## この記事を読むべき理由
日本のSaaS/クラウド運用やオンプレDB運用では、SSD導入やクラウド移行で「SSDならindex scanで良い」と安易に設定変更しがち。実測に基づいた判断と監視の重要性を理解することで、意図せぬ性能劣化を防げます。

## 詳細解説
著者は直接I/Oを有効にし、shared_buffers（128MB）より十倍大のテーブルを作り、シーケンシャルスキャンとインデックススキャンで実行時間とバッファアクセスを計測しました。単純化すると次のように1ページ当たりの時間を算出できます：

$$
\text{seq\_page\_time}=\frac{\text{seq\_scan\_time}}{\text{seq\_pages}}
\quad,\quad
\text{random\_page\_time}=\frac{\text{index\_scan\_time}}{\text{random\_pages}}
$$

そしてコスト比は

$$
\text{random\_page\_cost}=\frac{\text{random\_page\_time}}{\text{seq\_page\_time}}
$$

実験では $\,\text{random\_page\_cost}\approx 25.2\,$ と算出され、デフォルト4.0より遥かに高い値になりました。複数マシンの試験でローカルSSDは概ね25–35、クラウドはさらに高い傾向です。

さらに重要な点：
- ビットマップスキャンはI/Oをより順次化しプリフェッチを活用するため、index scanより現実的に有利になる領域が広い。
- prefetch（effective_io_concurrency）を切ると実行時間は悪化するが、オプティマイザのコスト値は変わらないためコストと実時間のギャップが生じる。
- コストモデルはプリフェッチやパラレル化の恩恵を十分に反映していないため、GUCの値を変えるとプランの「反転」が起きやすい。

また、random_page_costを下げたほうが良いケースもあります：
- 実ワークロードが「ホットセット（アクティブデータ）」をほぼRAMに収めている場合
- プランは個別クエリでは良くても他クエリのキャッシュ競合を招く場合（計画は単体で最適化される）
- 統計や見積りが悪く、コスト調整で実運用上の最適を擬似的に得る場合

## 実践ポイント
- random_page_costを変える前に必ず代表的ワークロードでA/B検証する（パフォーマンス監視／pg_stat_statementsを活用）。
- effective_cache_size を現実に合わせ正しく設定し、キャッシュ前提を明示する。
- effective_io_concurrency を調整してプリフェッチ効果を検証する（クラウドとローカルで差が出る）。
- 小手先のGUC変更でなく、「どのクエリで何がボトルネックか」をログ・プロファイルで把握する。
- 設定変更は段階的に運用し、クエリ実行時間の分布を監視してプラン反転（遅いクエリ増加）を検出する。

短く言うと：SSDだからといってrandom_page_costを盲目的に下げるのは危険。まず測る、比較する、監視する。これが安全なチューニングの王道です。
