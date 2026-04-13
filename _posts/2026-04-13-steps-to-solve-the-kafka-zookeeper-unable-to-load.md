---
layout: post
title: "Steps to solve the Kafka Zookeeper \"Unable to load data base on disk\" problem - Kafka ZooKeeperの「Unable to load database on disk」問題を解く手順"
date: 2026-04-13T14:45:30.030Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.pixelstech.net/article/1776059359-steps-to-solve-the-kafka-zookeeper-%26apos-unable-to-load-data-base-on-disk%26apos-%e2%80%8b-problem"
source_title: "Steps to solve the Kafka Zookeeper &amp;apos;Unable to load data base on disk&amp;apos;​ problem | PixelsTech"
source_id: 362733467
excerpt: "破損スナップショット削除とjute.maxbuffer増加でZooKeeperを短時間復旧"
image: "https://www.pixelstech.net/images/uploads/article/img.png"
---

# Steps to solve the Kafka Zookeeper "Unable to load data base on disk" problem - Kafka ZooKeeperの「Unable to load database on disk」問題を解く手順
Zookeeperが起動しない時に慌てず復旧できる、Druid+Kafka環境向けの実践ハンドブック

## 要約
ZooKeeperで "Unable to load database on disk" エラーは、破損または過大なスナップショット/トランザクションログが原因で発生する。解決は（1）破損ファイルの削除、（2）Djute.maxbufferの増加、（3）再デプロイの順で行えば復旧できる。

## この記事を読むべき理由
Druid＋Kafkaを使ったリアルタイム分析基盤は日本の多くの企業でも採用されており、この障害はサービス停止やデータ取り込み停止につながる。手順を知っておけばダウンタイムを短縮できる。

## 詳細解説
- 背景：Apache Druidは大量の時系列データ可視化で使われ、Kafkaが取り込みパイプラインになることが多い。ZooKeeperはメタデータを保持するため重要。
- 症状：起動時に以下のようなログが出る。
  - java.io.IOException: Unreasonable length = <巨大値>
  - ERROR ... Unable to load database on disk
- 原因：
  1. 大量のストリーミング取り込み中にノード障害が発生し、スナップショット/txログが破損または不完全に書き込まれる。
  2. 破損ファイルが他のZooKeeperポッドに伝播して起動不能になる。
  3. デフォルトの jute.maxbuffer（通常10MB）が不足していると大きなtx/snapshotを読み込めずエラーとなる。
- 危険性：単に再インストールすると、破損データが再導入されて再発する。

## 実践ポイント
1) まずバックアップを取りつつ、破損ファイルを削除する（安全のため対象ノードのローカルコピーを保存しておく）。
- ZooKeeperコンテナに入る（例）:
```bash
# bash
kubectl exec -it druid-cluster-zk-zookeeper-0 -- zkCli.sh
```
- データディレクトリ内のversion-2や大きなスナップショットを削除:
```bash
# bash
kubectl exec -it druid-cluster-zk-zookeeper-0 -- bash -c "ls -lh /bitnami/zookeeper/data/version-2"
kubectl exec -it druid-cluster-zk-zookeeper-0 -- bash -c "rm -rf /bitnami/zookeeper/data/version-2/*"
# 大きな snapshot.* を個別に確認して削除
kubectl exec -it druid-cluster-zk-zookeeper-0 -- bash -c "find /bitnami/zookeeper/data/version-2 -type f -name 'snapshot.*' -size +80M -exec rm -v {} \;"
```
※削除前に必ずファイルを別場所へ退避（scpやkubectl cp）して復旧手段を確保すること。

2) ZooKeeperのバッファ上限を引き上げる（zk-values.yaml等でDjute.maxbufferを増やす）
```yaml
# yaml
zookeeper:
  extraEnvVars:
    - name: JVMFLAGS
      value: "-Djute.maxbuffer=104857600"  # 100MB
```
デフォルト約10MB → 100MB等に設定。破損サイズより少し大きめに。

3) Helmで再デプロイ
```bash
# bash
helm uninstall -n druid druid-cluster-zk
helm install -n druid druid-cluster-zk bitnami/zookeeper -f zk-values.yaml
```

4) 動作確認
- 全ZooKeeperポッドがReadyになること、Quorumが確保されていることを確認。
```bash
# bash
kubectl -n druid get pods -l app.kubernetes.io/name=zookeeper
kubectl -n druid logs druid-cluster-zk-zookeeper-0
```
- Druid側のダッシュボード/メタデータが復帰しているかを確認。

5) 運用上の注意（日本市場向け短めチェックリスト）
- メンテ時にスナップショットの自動取得と外部バックアップを設定。
- jute.maxbufferは過剰に大きくせず、取り込みバーストの最大サイズを想定して調整。
- Kafka→Druid流量制御と監視（Podの負荷異常時にアラートを出す）を整備。

以上の手順で多くの "Unable to load database on disk" 事象は解消される。必要ならログ抜粋や環境（K8sバージョン、ZooKeeperのイメージ）を提示して詳細助言を依頼してください。
