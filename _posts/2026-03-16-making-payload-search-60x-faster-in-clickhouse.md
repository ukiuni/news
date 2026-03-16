---
layout: post
title: "Making Payload Search 60x Faster in ClickHouse - ClickHouseでペイロード検索を60倍高速化した方法"
date: 2026-03-16T13:41:39.431Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://hookdeck.com/blog/how-we-made-payload-search-60x-faster-in-clickhouse"
source_title: "How We Made Payload Search 60x Faster in ClickHouse"
source_id: 382492591
excerpt: "ClickHouseでペイロード検索を約60倍高速化、値ハッシュ＋可変ウィンドウで平均400msに改善"
image: "https://hookdeck.com/og.png?title=How%20We%20Made%20Payload%20Search%2060x%20Faster%20in%20ClickHouse"
---

# Making Payload Search 60x Faster in ClickHouse - ClickHouseでペイロード検索を60倍高速化した方法
ダッシュボードが延々と回り続ける悪夢を終わらせる：ClickHouseでペイロード検索を約60倍高速化した実践テクニック

## 要約
HookdeckがClickHouse上のペイロード検索を、平均約400ms・p99<1.4sまで改善した手法を解説。キーは「タイムスタンプ整合」と「値ハッシュによるバケット化＋可変ウィンドウ検索」。

## この記事を読むべき理由
Webhookやイベント大量処理・ログ検索を扱う日本のプロダクトやSREに直結するノウハウ。ClickHouseで半構造化JSONを高速検索したい現場ですぐ使える設計と実装の要点が得られる。

## 詳細解説
背景問題（要点）
- Webhookは半構造化（スキーマがバラバラ）で、1件あたり巨大なMapカラムを持つと検索で無駄に大量のデータを読み込む。  
- 全てを結合したterms列＋大きなBloomフィルタはスケールで誤検出が増える。  
- 状態遷移で同イベントが複数行になるため、ClickHouseでのクエリ時にGROUP BY＋LIMITが短絡できず、全件を読み・集約してから返す必要があり遅い。

前提整理：created_atの統一
- request, event, payload 各テーブルで同一のcreated_atを厳密に合わせることで、主キー (team_id, created_at, id) のソート／インデックス整合が取れる。  
- これにより、検索で得たタプルを tuple IN で直接参照し、全域スキャンを避けられる。

Technique 1 — 値ハッシュでのバケット化（bucketed storage）
- アイデア：値をハッシュしてN個のMapカラムに分散することで、検索時は対象の1列だけ読む。列スキャン量は概ね$1/N$になる（$N$=50が実運用で良いトレードオフ）。  
- 実装の要点：文字列50、数値50、真偽2 の合計102バケットを用意。インサート時にJSONをフラット化し、値をXXHash3でハッシュして該当バケットに格納。  
- 検索例：キー指定の厳密一致はハッシュで得たバケットのみを対象に mapContains + 値比較 を行う。キー未指定の全文検索はその値がハッシュするバケットの mapValues を走査。  
- 注意点：mapContainsでキー存在確認してから値アクセスする（ClickHouseのデフォルト値による誤検出防止）。配列要素はワイルドカード経路を正規表現に変換して arrayExists で検査する。

SQL（検索イメージ）
```sql
-- 値 "12345" が string_bucket_17 にハッシュされた場合の例
SELECT event_pks
FROM search_payloads_bucketed
WHERE team_id = 'tm_abc'
  AND created_at BETWEEN '2026-03-01' AND '2026-03-13'
  AND mapContains(string_bucket_17, 'body.order_id')
  AND string_bucket_17['body.order_id'] = '12345'
```

配列用パターン変換（概念）
```javascript
// key に % を使うパターンを正規表現に変換
function patternKeyToRegex(key) {
  // escape と % -> [^.]+ 置換 を行う
}
```

Technique 2 — 可変ウィンドウの反復スキャン（variable-window iterative scanning）
- 課題：たとえ列スキャンが減っても、GROUP BYによる重複排除対象行数が多いと遅い。  
- 解決：最近のデータを小さい時間窓から順に検索し、十分な結果が得られたら停止する。短時間窓だとGROUP BYの対象が激減するため応答が速い。必要ならウィンドウを段階的に拡大していく（例：直近30分→数時間→数日）。  
- これにより「最初のページ」が高速に返る確率が大幅に上がる。さらにcreated_atの一貫性があることで、得たタプルを高速に突ける。

その他の実務的ポイント
- ハッシュ関数は高速なXXHash3を採用（インジェスト経路でのオーバーヘッドを低減）。  
- バケット数は payload サイズとクエリ特性で調整（50は経験則）。  
- Bloomフィルタは巨大化すると意味が薄れるため、単一巨大terms列は避ける。

## 実践ポイント
- created_at を関連テーブルで厳密に統一する（インデックスの活用が劇的な差を生む）。  
- 値をハッシュして複数Mapカラムに分散し、検索時は該当バケットのみ読む（$N$バケットで列読みは概ね$1/N$に）。  
- インサート時にJSONをフラット化して型を保存、XXHash3でバケット決定。  
- クエリでは mapContains を必ず使い、配列はパスを正規表現化して arrayExists で探索。  
- レイテンシ重視なら可変ウィンドウ反復スキャンを実装して「まず最初のページを速く返す」戦略を採る。  
- メトリクス（avg/p50/p99、スキャン行数）を計測してバケット数やウィンドウ戦略を調整する。

以上を踏まえれば、ClickHouseでの半構造化ペイロード検索を実用的に高速化できる。実装の詳細（ConcurrencyControllerや微秒同期など）は原著の次回解説が参考になる。
