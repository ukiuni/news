---
layout: post
title: "Show HN: wxpath – Declarative web crawling in XPath - Show HN: wxpath — XPathで宣言的に書くウェブクローリング"
date: 2026-01-20T19:03:30.237Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/rodricios/wxpath"
source_title: "GitHub - rodricios/wxpath: wxpath - declarative web crawling with XPath"
source_id: 46618472
excerpt: "XPathだけで非同期幅優先クローリングを実現、短時間でスクレイピングを宣言的に構築できるツール"
image: "https://opengraph.githubassets.com/e2db19866491d8ea04bccbf3ec4ed622346c77de70c3d597f133e2a60a48e910/rodricios/wxpath"
---

# Show HN: wxpath – Declarative web crawling in XPath - Show HN: wxpath — XPathで宣言的に書くウェブクローリング
XPathで「書くだけ」クローラーが作れる――wxpathでスクレイピングがぐっとシンプルに

## 要約
wxpathは「何をたどって何を抽出するか」をXPath式だけで宣言し、非同期に幅優先で巡回して結果をストリームするPythonライブラリです。url(...)演算子と///構文で深掘り（ページネーションやリンク追跡）を1式で表現します。

## この記事を読むべき理由
- スクレイピングやデータ収集の実装量を減らしたい初級〜中級エンジニアに有効。  
- 日本のドキュメント、EC、ニュースの定期収集やPOCで短時間に結果を出せる。  
- 非同期（asyncio/aiohttp）対応で並列取得が簡単、かつrobots.txtとUser-Agent設定で「礼儀ある」スクレイピングがしやすい点も実務向け。

## 詳細解説
- コア思想：従来の「ループでURLを取り出してfetchしてparseして…」という命令型ではなく、XPath式で「ここから開始して、こういうリンクを辿り、ここを抽出する」と宣言する。エンジンが並列で実行し、見つかった結果を逐次返す。  
- url(...)：指定したURL（あるいはXPathで動的に生成されたURL）をフェッチして、lxml.html.HtmlElementとしてXPath処理に渡すカスタム演算子。  
- ///url(...)：単一式で「深掘り」を指示する専用構文。max_depth等で深さ制限を掛け、幅優先っぽく（breadth-first-ish）探索を行う。無制限だと爆発するので注意。  
- 非同期：内部はasyncio + aiohttpベース。wxpath_asyncやwxpath_async_blocking_iter（同期コードから並列取得を扱えるラッパー）を提供。  
- XPath 3.1：elementpathライブラリを使い、map/arrayなどXPath 3.1の高機能を使えるため、抽出結果をその場で構造化できる。  
- 出力型：lxml要素、XPathの値、独自のWxStrや辞書/配列など。CLIはJSONフラット化して表示。  
- マナーと設定：robots.txtは既定で尊重可能。User-Agentや同一ホスト並列数、キャッシュ/永続化の設定も用意。進捗表示はtqdmで追える。  
- 注意点：URLの重複はベストエフォートで抑制されるが完全ではない点、深掘りの制約を必ず設けること、サイトの利用規約やrobots.txtを順守すること。

## 実践ポイント
- まずはREADMEのサンプルを試す（例：Wikipediaのリンク抽出）。以下は同期＋並列ラッパーの例。

```python
python
from wxpath import wxpath_async_blocking_iter

path_expr = """
url('https://en.wikipedia.org/wiki/Expression_language')
///url(//main//a/@href[starts-with(., '/wiki/') and not(contains(., ':'))])
/map{
  'title': (//span[contains(@class, "mw-page-title-main")]/text())[1] ! string(.),
  'url': string(base-uri(.))
}
"""

for item in wxpath_async_blocking_iter(path_expr, max_depth=1, progress=True):
    print(item)
```

- すぐ使えるチェックリスト：
  1. max_depthやXPathのフィルタで探索範囲を絞る（traversal explosion回避）。  
  2. robots.txtと対象サイトの利用規約を確認する。wx:respect-robotsを有効に。  
  3. User-Agentヘッダを設定する（例: "my-app/0.1 (contact: you@example.com)"）。  
  4. CLIでまず少量の深さ・並列数で試し、結果と負荷を観察する。  
  5. 日本語サイトではUTF-8やHTML構造の違いを意識し、XPathはページ構造に合わせて調整する。  

- 導入メモ：まずはリポジトリのREADMEでインストール方法とAPIを確認（pipインストールや依存関係、バージョン注意）。実運用ではキャッシュや永続化オプションを検討する。

短時間でプロトタイプを作りたい人や、XPathに慣れている人には特に刺さるツール。深掘りは強力だが慎重に設定して使おう。
