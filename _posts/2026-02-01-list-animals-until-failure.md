---
layout: post
title: "List animals until failure - 失敗するまで動物を列挙する"
date: 2026-02-01T05:21:00.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://rose.systems/animalist/"
source_title: "list animals until failure"
source_id: 46842603
excerpt: "API検証とUXの工夫が学べる、Wikipedia検証で重複排除し制限時間内に動物を列挙するゲーム"
---

# List animals until failure - 失敗するまで動物を列挙する
制限時間でどれだけ百科知識を引き出せるか？シンプルな「動物列挙ゲーム」で遊びながら学ぶUXと実装の肝

## 要約
英語のミニゲーム「List animals until failure」は、タイマー制でWikipediaに記事がある動物名を次々に入力していくゲーム。各正解で時間が加算され、重複や重なり語は除外されるなど、Wikidata/Wikipediaを使った検証ロジックが特徴です。

## この記事を読むべき理由
- 短時間で遊べるが、APIや検証ロジックの設計、UXの工夫が詰まった良い実例だから。  
- 日本語ローカライズや教育用途、技術演習として再実装・応用しやすい。

## 詳細解説
- ゲームの流れ：初期タイマーがあり、正しい動物名を入力するたびにスコアとタイムが増える。タイマーが0になると終了。設定で初期時間と増分を変更可能。  
- 検証基盤：入力はWikipedia/Wikidataの存在で検証される（元記事は外部API＋手動調整を併用）。LLMは使っていない点に注意。  
- 重複ルール：単純な同一語の重複排除に加えて「重なり語（例：bear と polar bear）」を同一視するロジックがある。これは文字列ベースだけでなく、Wikidataの識別子や手動のホワイト/ブラックリストで調整している可能性が高い。  
- 実装上の考慮点：APIレイテンシ対策（ローカルキャッシュ／バッチ検証）、正規化（大文字小文字、記号、和名／英名のマッピング）、曖昧さ処理（別種なのか亜種か）、不正入力対策が必要。

## 実践ポイント
- 今すぐ試す：ブラウザで元ページを開いて遊んでみる。制限時間と増分を変更して戦略を試すのが面白い。  
- 自分で作るときのチェックリスト：
  - Wikipedia/Wikidata APIで存在確認を行う（キャッシュ必須）。  
  - 入力は正規化して比較（トリム、全角半角、ローマ字変換など）。  
  - 重複判定は単純文字照合＋Wikidata QIDでの一意性確保。  
  - レイテンシ対策に入力を先読み／ローカル辞書を用意。  
  - 日本語化：日本語Wikipediaを使うか和名→英名マッピングを用意すると親和性が高い。  
- 開発の練習題材に最適：フロント（JS）＋API設計＋UX調整を少人数で試せる良いワークショップになる。

参考のミニ検証コード例（非完成、概念示唆）：

```javascript
// javascript
async function isValidWikipediaPage(title){
  const url = `https://en.wikipedia.org/w/api.php?action=query&format=json&titles=${encodeURIComponent(title)}&origin=*`;
  const res = await fetch(url);
  const data = await res.json();
  return !!Object.values(data.query.pages)[0].pageid;
}
```

以上。元記事は単純ながら設計上の工夫が多く、日本語対応や教育用途への応用がしやすい点が魅力です。
