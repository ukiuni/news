---
layout: post
title: "Building a Self-Hosted Google Trends Alternative with DuckDB - DuckDBで作るセルフホスト版Google Trends代替ツール"
date: 2026-02-16T01:28:38.468Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://medium.com/python-in-plain-english/i-built-a-self-hosted-google-trends-alternative-with-duckdb-624a19bcab65"
source_title: "Building a Self-Hosted Google Trends Alternative with DuckDB"
source_id: 440723247
excerpt: "DuckDBとPythonでセルフホストのSERP変動を可視化し、急上昇を検出する方法"
---

# Building a Self-Hosted Google Trends Alternative with DuckDB - DuckDBで作るセルフホスト版Google Trends代替ツール
独立系開発者が週末で作った「検索結果の揺らぎ」を可視化するローカル分析ツール（Python + DuckDB + CLI）

## 要約
Google Trendsが教えてくれない「SERPの入れ替わり」「競合のタイトル変更」「順位の劇的な動き」を、毎日のスナップショットからDuckDBで集計して0–100の“Interest Score”に変換する自己ホスト型ツールの作り方。

## この記事を読むべき理由
日本語のプロダクト/技術記事やSEOに取り組む開発者は、キーワードの「検索ボリューム」だけでなく「誰が上がってきたか」「見出しを変えてCTRを試しているか」を知る必要がある。月額高額ツールに頼らずローカルで履歴を貯めて分析できる実践的な手法を学べる。

## 詳細解説
- 全体構成  
  - CLI（argparse）起点でコマンドを実行：fetch / volatility / scores / calculate-scores 等。結果はファイル内の DuckDB（単一ファイル）に蓄積。cronで定期取得、jqやスクリプトと組み合わせ可能。
  - 外部SERPはBright Data等のAPI経由で取得（serp_client.py）。他APIへの拡張はクライアント実装を追加するだけ。

- なぜDuckDBか  
  - カラム指向で時系列集計が高速、LAG() や PARTITION BY といったウィンドウ関数が使える。サーバ不要でDBが単一ファイルのため運用が簡単。

- Interest Score の設計（要点）  
  1. 新規ドメイン数（Top10に新しく入ったドメイン数）: 0–40点  
     $$
     new\_domains\_score = \min(\text{len(new\_domains)} \times 4, 40)
     $$
  2. 平均ランク改善（共通ドメインの前日比）: 0–30点  
     - 各ドメインで $rank\_improvement = previous\_rank - current\_rank$ を取り平均し、正規化してスコア化。概念的には平均を -10..+10 にマップし点数化。  
  3. ドメイン重複率（今日のTop10のうち前日から残っている割合）: 0–30点  
     $$
     reshuffle\_score = reshuffle\_frequency \times 30
     $$
  合計で
  $$
  interest\_score = new\_domains\_score + rank\_improvement\_score + reshuffle\_score
  $$
  高スコアは「急上昇／大規模なSERP変動」、低スコアは「安定した領域」を示す。

- 実装の流れ（簡潔）  
  - fetch: 当日のSERPを取得して `serp_snapshots` テーブルへ追記  
  - スナップショットの差分から新規参入、タイトル変更、順位差を算出  
  - スナップショット挿入時に前日と比較してInterest Scoreを計算して `interest_scores` に格納  
  - scores コマンドで過去N日分を取得しPNGチャートを出力（matplotlib）

- CLI例
```python
# 実行例
python main.py fetch --keywords "python"
python main.py volatility --query "python" --days 30
python main.py scores --query "nextjs" --days 7
```

## 実践ポイント
- 小さく始める：まずは毎日1キーワードをfetchして7〜30日分の履歴を貯めるだけで実用的な変化が見える。  
- 運用コストを抑える：DuckDBは単一ファイル、バックアップはそのファイルをコピーするだけ。  
- 拡張しやすさ：Bright Data以外のSERP APIを追加するには `serp_client` を実装するだけ。  
- 自動化：cronで定期fetch、生成JSONをjqで加工して通知やSlackに流すワークフローが簡単。  
- 日本語キーワード注意点：日本語SERPは地域・言語で結果が変わるため、Bright Data等のAPIで地域設定を適切に行うこと（または日本向けプロキシを用意）。

元記事のリポジトリを読んでクローンすれば週末プロジェクトとして再現可能。ローカルで自由に履歴を解析したい人に強くおすすめ。
