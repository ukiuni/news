---
layout: post
title: "Losing 1½ Million Lines of Go - Goで失いかけた150万行"
date: 2026-01-24T03:01:30.406Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tbray.org/ongoing/When/202x/2026/01/14/Unicode-Properties"
source_title: "ongoing by Tim Bray &#xb7; Losing 1½ Million Lines of Go"
source_id: 46679802
excerpt: "巨大生成コードを捨て、オンデマンド生成とキャッシュでUnicode対応を大幅高速化した実践記"
image: "/ongoing/misc/podcast-default.jpg"
---

# Losing 1½ Million Lines of Go - Goで失いかけた150万行
Unicodeの地雷を避けて、Goで高速な文字プロパティ正規表現を実装する方法

## 要約
Tim BrayがQuaminaでUnicode文字プロパティ（例: \p{L}）対応を実装し、巨大全生成コードを捨てて「初回生成＋キャッシュ」戦略で性能と作業性を両立させた話。

## この記事を読むべき理由
Go標準のUnicode対応は古い（2026年1月時点でUnicode 15.0.0）。日本語・漢字・絵文字を多用する実務では最新版Unicode対応が重要で、現場での実装選択と運用コストに直結するため。

## 詳細解説
- 問題点：Quaminaは正規表現でUnicodeプロパティ（例: [\p{L}\p{Zs}\p{Nd}]）を扱いたく、Go標準のunicodeパッケージが最新Unicodeに追随していないため、UnicodeData.txtを直接取得・解析してコード点レンジを作成した。  
- データ処理：UnicodeData.txtからカテゴリごとのコード点ペアを抽出（37カテゴリ、合計14,811ペア、例：Lが1,945ペア）。これを元にオートマトンを作る設計。  
- 初期アプローチの失敗：全自動体を事前生成してGoソースに埋め込むと、途中で775K行（計画ではさらに増える見込み）になり、生成ファイルでIDEが落ちたり起動時メモリ/時間コストが激増。単体テストや開発体験が劣化。  
- 解決策：オートマトン生成処理自体は簡潔に保ちつつ、最初の利用時にオンデマンドで生成してインスタンス内でキャッシュする方式に変更。結果、Unicodeプロパティの追加速度が135/sec→4,330/secに改善（約30倍）。ランタイムでのマッチング速度自体は高く、数十万〜数百万件/秒で動作可能。  
- 補足：定型作業（ファイル取得・解析・コード生成・テスト）はGenAI（例：Claude）に向くが、導入コストや過信への注意も述べられている。

## 実践ポイント
- Goで最新Unicodeを扱う必要があるなら、標準パッケージ頼みは危険。UnicodeData.txtを直接使う選択肢を検討する。  
- 全生成ソースを埋め込むのではなく、オンデマンド生成＋インメモリキャッシュで起動負荷とIDE問題を回避する。  
- 生成データは「レンジ表現＋効率的なシリアライズ」でコンパクト化を図る（巨大なソースファイルは編集回避と起動負荷の原因）。  
- 単純作業の自動化にはGenAIが有効だが、検証とテストを必ず行う。  
- 日本語環境では漢字や絵文字の追加・変更がサービス品質に直結するため、Unicodeバージョン管理の運用ルールを整備する。
