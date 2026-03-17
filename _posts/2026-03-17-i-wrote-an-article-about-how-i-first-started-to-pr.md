---
layout: post
title: "I wrote an article about how I first started to program - 私がプログラミングを始めた経緯"
date: 2026-03-17T12:12:41.061Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://artificesoftware.com/articles/how_i_started_programming.html"
source_title: "Artifice Software | How I Started Programming"
source_id: 381687071
excerpt: "考古学現場の大量FASTQをPythonで自動化し論文へ導いた実践ストーリー。"
---

# I wrote an article about how I first started to program - 私がプログラミングを始めた経緯
考古学の「土」とPythonがつないだキャリア — ボランティア作業から論文につながった自動化の物語

## 要約
大学のボランティア作業で遭遇した膨大なDNAデータの手作業処理を、Pythonで自動化した経験がキャリアの転機になった話。単純なファイル操作とウェブ自動化が、やがて論文や本格的な解析パイプラインにつながる過程を描く。

## この記事を読むべき理由
- 現場で生じる「単調な手作業」をプログラムで解決する具体例は、日本の研究機関やスタートアップにそのまま応用できる。
- 初心者が何を学べば実用的な自動化を作れるか、実践的な指針が得られる。

## 詳細解説
著者は考古学プロジェクトで得られたFASTQ形式の大量DNA配列を、人手でNCBIデータベースに照合していた作業を見て、これを自動化することに着手しました。ポイントは以下です。

- FASTQの構造：1配列につき4行（ヘッダ／配列／区切り／品質スコア）。これを正しくパースすることが前提。  
- 手作業の流れ：配列をコピー→NCBIで検索→アクセッション番号取得→別データベースで生物情報取得→結果を表にまとめる、を繰り返す。  
- 自動化手法：ファイル入出力（Pythonのopen/読み取り）、文字列処理、ウェブアクセス（requestsやSelenium等）でフォーム操作や取得を自動化。サーバー側のレート制限やIPブロックへの対処（遅延挿入、API利用）が必要。  
- 精度管理：データは必ずしも完全一致しない（断片化やダメージであいまい照合が起きる）。最頻度ヒットだけで片付けず、スコアや複数候補を保持する設計が望まれる。  
- 発展：その後、配列トリミング・低品質配列除去・年代判定などのQC工程を加え、"Bailey Pipeline"のような一連の解析パイプラインに発展。再現性と自動化が研究成果に直結した例です。  
- 実務向けの技術選択：ウェブスクレイピングよりも、可能ならNCBIのEntrez APIやBiopython（SeqIO, Entrez）を使うのが安定的で礼儀正しい（rate-limitを守れる）方法です。

## 実践ポイント
- まずはPythonでファイル操作と文字列処理を身につける。  
- FASTQはBiopythonのSeqIOで簡単に扱える（例：```python
from Bio import SeqIO
for rec in SeqIO.parse("sample.fastq","fastq"): ...
```）。  
- ウェブ自動化はrequests＋APIが第一選択、GUI操作が必要ならSeleniumを検討。  
- サーバー負荷・API制限に配慮し、遅延・リトライ・APIキーを使う。  
- 小さいデータセットでまず試し、ログとテストを整備してからスケールする。  
- 日本の大学・博物館・ベンチャーでは「人手不足×定型作業」の場面が多く、同様の自動化で即戦力を発揮できる。再現性のためにSnakemake/Nextflow等でパイプライン化するのも有効。

短い結論：言語は何でも始められるが、Pythonは手元のデータを触って自動化し結果を出すまでの学習コストが低く、実務でのインパクトが大きい。まず小さな反復作業を自動化してみてください。
