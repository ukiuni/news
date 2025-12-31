---
layout: post
title: "Distributed MultiThreaded Web Crawler (beginner) - 分散マルチスレッドWebクローラ（入門）"
date: 2025-12-31T23:38:55.252Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/DhairyaVardhanChauhan/WebCrawler"
source_title: "Distributed MultiThreaded Web Crawler (beginner)"
source_id: 474116219
excerpt: "RedisとJsoupで作る、robots対応の分散ECクローラ実践ガイド"
---

# Distributed MultiThreaded Web Crawler (beginner) - 分散マルチスレッドWebクローラ（入門）
魅せる見出し: Redis×Jsoupで作る、実用的かつ礼儀正しい分散クローラ設計 — 日本のECデータ収集現場がすぐ使える

## 要約
このリポジトリは、Redisを状態管理に使い、JsoupでHTMLを解析する分散マルチスレッドWebクローラのサンプル実装。robots.txt尊重、ドメイン単位ロック、重複検知、リトライ/デッドキューなど、実用性の高い仕組みが揃っています。

## この記事を読むべき理由
日本のECや価格モニタリング、データチームにとって「スケールしつつ礼儀正しく」スクレイピングする設計例は貴重です。OSS実装を読み解くことで、即戦力になるアーキテクチャや運用上の注意点が掴めます。

## 詳細解説
- アーキテクチャ概要  
  - 中核は Crawler クラス：RedisでURLキュー（queue, queue:retry, queue:dead 等）を管理し、JsoupでHTMLを取得・解析、製品情報を抽出してRedisへ公開します。複数スレッドで動作し、ステートはRedisで共有するため分散実行に向きます。
  - CrawlerRunnable：各ワーカースレッドが無限ループで Crawler.crawl() を呼び続ける実装。例外はランタイム例外として扱います。

  サンプル（実装イメージ）:
  ```java
  public void run() {
      while (true) {
          try {
              Crawler.crawl();
          } catch (IOException | URISyntaxException e) {
              throw new RuntimeException(e);
          }
      }
  }
  ```

- robots.txtの扱い（RobotsHelper / RobotsRules / RobotsGroup）  
  - robots.txtをダウンロードしてパースし、Redisにキャッシュ（例: robots:<domain>）。ユーザーエージェントごとのallow/disallowとcrawl-delayを解決して適用します。
  - isAllowedByRobots はパスのprefixで許可/不許可を判定。デフォルトのcrawl-delayは1秒（1000ms）を基本に設計されています。

- ポリテネスとドメインロック  
  - acquireDomainLock(domain, delay) によりドメインごとのアクセス頻度を制御。ドメイン単位でロックとアクティブカウントを持つことで過負荷を防ぎます。

- 重複対策とキュー運用  
  - BloomFilter やコンテンツハッシュ（content:hashes）で重複コンテンツを弾く。失敗URLは再試行カウント（url:retries）を持ち、閾値超過で queue:dead に移動。
  - queue:processing で現在処理中のURLを管理し、障害時の復旧を容易に。

- データ抽出（Product Extraction）  
  - HTMLのセレクタ（例: "li.product", ".product-name", ".product-price"）を使って製品名・価格・画像URLを抽出し publishProduct でRedisへ流す設計。eコマース特化だが抽出ロジックは汎用化可能。

- 実装周辺  
  - 技術スタック：Java, Jsoup, Jedis (Redis client), Gson, ExecutorService。Dockerfile / docker-compose.yml / pom.xml が含まれ、コンテナ化や依存管理の例もあり。

## 実践ポイント
- 分散状態はRedisで一元化：キュー・ロック・キャッシュをRedisで管理するとワーカ追加が容易。
- robots.txtは必ず尊重：キャッシュして使う（例: 24時間TTL）ことでリクエストを減らす。
- ドメイン単位の遅延制御：ドメインロック+crawl-delayを必須にしてサイト負荷を下げる。
- 重複排除は多層に：URL正規化 + BloomFilter + コンテンツハッシュで漏れを減らす。
- 運用監視を設計に含める：queue長、retryカウント、deadキューの増加をアラート化する。
- 法律・利用規約の確認：日本国内でもスクレイピングは景表法・利用規約や著作権に関する配慮が必要。robots.txtは技術的ガイドラインだが、法的リスク回避のため運用ルールを整備すること。

## 引用元
- タイトル: Distributed MultiThreaded Web Crawler (beginner)
- URL: https://github.com/DhairyaVardhanChauhan/WebCrawler
