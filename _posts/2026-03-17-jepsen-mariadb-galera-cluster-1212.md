---
layout: post
title: "Jepsen: MariaDB Galera Cluster 12.1.2 - Jepsen：MariaDB Galera Cluster 12.1.2"
date: 2026-03-17T06:55:42.259Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jepsen.io/analyses/mariadb-galera-cluster-12.1.2"
source_title: "Jepsen: MariaDB Galera Cluster 12.1.2"
source_id: 1680443550
excerpt: "Jepsen検証がGalera 12.1.2でコミット喪失やLost Updateなど整合性欠陥を暴露し、運用設計に重大な警鐘"
---

# Jepsen: MariaDB Galera Cluster 12.1.2 - Jepsen：MariaDB Galera Cluster 12.1.2
本番クラスタで「トランザクションは失われない」は本当か？Jepsenが暴いたGaleraの整合性ギャップ

## 要約
Jepsenの独立検証により、MariaDB Galera Cluster 12.1.2はドキュメントの主張に反して、コミット済みトランザクションの喪失（特に協調的なクラッシュ時）やLost Update（P4）・Stale Readなどの整合性異常を示すことが確認された。

## この記事を読むべき理由
日本でもGaleraを使ったアクティブ－アクティブ構成や高可用クラスタは現場導入例が多く、ドキュメントの「no lost transactions」「瞬時同期」といった保証を盲信するとデータ損失やアプリ不整合を招く可能性があるため、設計・運用で知っておくべき重要な知見が含まれている。

## 詳細解説
- アーキテクチャと主張  
  Galeraは各ノードで読み書き可能な同期レプリケーション（gcommベース）を謳い、「全ノードにコミットされて初めて成功」といった説明が繰り返されるが、実際はクォーラム（過半数）で進行する設計。つまり単一障害を許容するために「全ノード必須」ではない。

- テスト設計（Jepsenの手法）  
  Jepsenは3ノードクラスタでMariaDB 12.1.2系＋Galeraを構築し、Elleによるリスト追加ワークロード（主キー単位のappendのみ）でトランザクション依存を解析。ネットワーク分断、プロセス停止・クラッシュなどの故障注入を行った。

- 観測された問題点
  1. コミット済み書き込みの喪失（MDEV-38974 / MDEV-38976）  
     - 推奨設定（innodb_flush_log_at_trx_commit=0）では、複数ノードが短時間で落ちる協調クラッシュ時にACK済みのトランザクションが失われる事例を頻繁に観測。0→1に変更すると発生頻度は劇的に減るが完全解消はされない。  
  2. Lost Update（P4, MDEV-38977）  
     - 正常動作時でも、あるトランザクションの読み取り→書き込みの間に別トランザクションの更新が入り、先の更新が事実上上書きされる（Lost Update）が確認され、Snapshot IsolationやRepeatable Read相当の保証がないことを示す。  
  3. Stale Read（MDEV-38999）  
     - あるトランザクションがコミットしてクライアントにACKされた後の新しいトランザクションが、そのコミット済みの変更を見ない（遅延や可視化されない）事象を定期的に観測。  
  4. ドキュメントと実挙動の乖離  
     - MariaDBの説明は強い一貫性を匂わせるが、Jepsenの結果はより弱い一貫性モデル（G-singleやG1c等の異常）を示している。

- なぜ起きるか（要点）
  - Galeraは楽観的にローカルで実行→コミット時に認証（certify）するモデルで、ログのフラッシュ設定やクラッシュのタイミングによってはディスクに確実に残らない操作があり得る。
  - 同期が「全ノード必須」ではなくクォーラムベースなので、可視性・原子性がドキュメントほど強くない箇所がある。

## 実践ポイント
- 設定変更：innodb_flush_log_at_trx_commit を 1 にすることで、協調クラッシュ時の書き込み喪失は大幅に低減する（ただし完全防止ではない）。  
- 設計上の注意：ORM等のread-modify-writeパターン（楽観的インクリメント等）はLost Updateのリスクが高い。SELECT ... FOR UPDATEや明示的ロック／外部調停を検討する。  
- 運用の備え：Galeraに「絶対喪失しない」という期待を置かない。障害注入テストや復旧手順を定期的に実行し、バックアップ・レプリカ戦略を明確化する。  
- ドキュメント確認：MariaDBの公式記述は誤解を招きやすいため、実運用前にJepsen等独立検証結果やMDEVチケットを参照する。  
- 代替検討：強い整合性（厳密なシリアライズ）を要する用途は、単一リーダー構成や別の分散DB（要件に応じて）を検討する。

以上の点を踏まえ、Galeraを使う場合は設定・アプリ設計・テストを慎重に行ってください。
