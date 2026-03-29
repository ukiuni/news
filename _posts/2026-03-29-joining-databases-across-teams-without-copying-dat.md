---
layout: post
title: "Joining databases across teams without copying data or running servers - チーム間でデータをコピーせずサーバーも立てずにデータベースを結合する"
date: 2026-03-29T01:28:18.301Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://datahike.io/notes/collaborate-without-infrastructure/"
source_title: "Joining databases across teams without copying data or running servers"
source_id: 47535863
excerpt: "S3やIndexedDBをコピーせずDatalogで結合し監査再現する手法。"
---

# Joining databases across teams without copying data or running servers - チーム間でデータをコピーせずサーバーも立てずにデータベースを結合する
魅力的なタイトル: サーバーもETLも不要—S3やブラウザのDBをそのまま結合してチーム横断のクエリを実現する方法

## 要約
Datahikeは「データベースを不変値として扱う」設計で、ストレージに置かれたインデックスを直接読み、複数の独立したデータベースを1つのDatalogクエリで結合できる。データのコピーや常駐サーバーを不要にし、監査やオフライン利用にも強い。

## この記事を読むべき理由
日本の開発チームでも、異なる部署やベンダーが別々に管理するデータを素早く安全に突合したい場面が増えています。ETLやAPIの運用コスト、レイテンシ、データ同期ミスを減らせるため実務的価値が高いです。

## 詳細解説
- データベースを「値」として扱う  
  Datahikeでは接続をデリファレンスすると、特定トランザクションで固定された不変のスナップショット（値）が返る。読み手同士のロックや協調は不要で、同じスナップショットは常に同じ結果を返す。

- ストレージが権威（authoritative）  
  書き手は各トランザクションでノードを永続化し、ストレージが最新状態を保持する。トランザクタのような専用プロセスに依存しないため、ストレージを読めるプロセスは誰でも完全なDBを復元できる。

- 構造的共有と永続Bツリー  
  インデックスは不変ノードを持つBツリー系で保存される。更新は影響を受けるパス上のノードだけを書き換え、新旧スナップショットは大部分を共有する。各ノードは一度書かれれば変更されないためキャッシュや複製が容易。

- 分散インデックス空間（distributed index space）  
  ブランチヘッド（root pointers＋メタ）だけを読み取りハンドルを得る。ノードは問い合わせ時にオンデマンドでストレージから取得され、ローカルLRUにキャッシュされる。これにより、サーバー間プロトコルやポートは不要。

- 複数DBの結合と過去スナップショットの混在  
  Datalogが複数ソースを受け付けるため、異なるチームのS3バケットやローカルファイル、IndexedDBにあるDBを同一クエリで結合できる。さらに as-of による過去スナップショットを混ぜて監査や再現検証が可能。

- ブラウザ対応と差分同期  
  konserveのIndexedDBバックエンドやWebSocket同期を使えば、ブラウザにローカルレプリカを作りクエリはネット往復ゼロ。差分は変更ノードのみ転送されるため帯域効率も高い。

## 実践ポイント
- 小さく試す: memory backendでローカルに2つ作り、Datalogで結合するワークフローを試す。  
- ストレージ権限を設計: S3やファイルに直にアクセスするため、バケット/ファイルのアクセス制御が重要。  
- 監査・再現: as-ofスナップショットを利用して報告や検証用の再現性を確保する。  
- ブラウザでの活用: オフライン対応のクライアントや差分同期を検討する場合、有力な選択肢。  
- 性能とGC設計: ノード共有は効率的だが、ノード増加とガベージコレクション戦略は検討する。

ミニ例（Clojure, メモリbackendでのクロスDBクエリ）:
```clojure
(require '[datahike.api :as d])
(def cfg {:store {:backend :memory :id (java.util.UUID/randomUUID)} :schema-flexibility :read})
(d/create-database cfg) (def cat (d/connect cfg))
(d/create-database cfg) (def inv (d/connect cfg))
(d/transact cat [{:product/sku "W001" :product/name "Widget" :product/price 9.99}])
(d/transact inv [{:stock/sku "W001" :stock/count 140}])
(d/q '[:find ?name ?price ?stock :in $cat $inv :where [$cat ?p :product/sku ?sku] [$cat ?p :product/name ?name]
       [$cat ?p :product/price ?price] [$inv ?i :stock/sku ?sku] [$inv ?i :stock/count ?stock] [(> ?stock 0)]]
     @cat @inv)
```

興味があれば、日本の具体事例（ECカタログ×倉庫在庫、監査ログの再現など）に即した検証プランを短く作ります。どれを試したいですか？
