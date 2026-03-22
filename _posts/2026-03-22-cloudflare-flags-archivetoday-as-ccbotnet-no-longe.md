---
layout: post
title: "Cloudflare flags archive.today as \"C&C/Botnet\"; no longer resolves via 1.1.1.2 - Cloudflareがarchive.todayを「C&C/ボットネット」と判定；1.1.1.2で解決されなくなる"
date: 2026-03-22T05:58:11.923Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://radar.cloudflare.com/domains/domain/archive.today"
source_title: "Cloudflare flags archive.today as \"C&C/Botnet\"; no longer resolves via 1.1.1.2"
source_id: 47474255
excerpt: "archive.todayがC&C/ボットネット判定、1.1.1.2で遮断—原因と対処"
---

# Cloudflare flags archive.today as "C&C/Botnet"; no longer resolves via 1.1.1.2 - Cloudflareがarchive.todayを「C&C/ボットネット」と判定；1.1.1.2で解決されなくなる
アーカイブサイトarchive.todayが「危険サイト」扱いに――閲覧できない・共有できない事態の原因と対処

## 要約
Cloudflareのドメイン情報でarchive.todayが「C&C/Botnet」と分類され、Cloudflareのマルウェア遮断用リゾルバ（1.1.1.2）では名前解決されなくなっている。だが証明書は頻繁に更新されており、サイト自体は稼働が確認できる状況。

## この記事を読むべき理由
archive.todayは研究・報道・検証で広く使われるアーカイブサービスで、日本のエンジニアやジャーナリストにも影響が出る可能性がある。DNSベースのブロックは見えにくく、業務や調査に混乱を招くため、原因把握と対処法を知っておくべきだ。

## 詳細解説
- 分類の仕組み：Cloudflare Radarはトラフィック・スキャン・外部フィードを元にドメインをカテゴリ分けする。C&C/Botnetはマルウェアのコマンド＆コントロールやボットネット関連と見なされた場合のラベル。
- 1.1.1.2の挙動：1.1.1.1のマルウェアフィルタ付きバリアントで、危険と判定されたドメインはNXDOMAINやブロック応答になるため「解決されない」ように見える。
- 証明書状況：Cloudflare Radarの記録ではarchive.todayはLet's Encryptで短い有効期間の証明書を継続的に発行しており、運営側は通常通り証明書を更新している（サービスが完全に停止しているとは限らない）。
- 考えられる原因：実際のマルウェア運用、サブドメインの悪用、URLスキャンでの検出誤判定、あるいは外部フィードの誤情報。技術的にはDNSフィルタのシグネチャやURLスキャン結果がフラグのトリガーになりやすい。
- 影響範囲：企業やISPがCloudflareのマルウェアブロックを利用している場合、ユーザーがarchive.todayにアクセスできなくなる。研究データや引用リンクが閲覧不能になるリスクあり。

## 実践ポイント
- ブロック確認：手元で名前解決を比較する。
```bash
# 1.1.1.2（マルウェアブロック）で解決されるか
dig @1.1.1.2 archive.today +short

# 1.1.1.1（通常）や他のリゾルバでの差分確認
dig @1.1.1.1 archive.today +short
dig @8.8.8.8 archive.today +short
```
- 一時対応：業務で必須なら、信頼できるネットワークでは1.1.1.1や別のリゾルバを使う／VPNやプロキシで回避。ただしポリシーや法令順守を確認。
- 調査手順：Cloudflare Radarの該当ページ、公開URLスキャン、CTログ（証明書履歴）を確認して挙動とタイムラインを把握する。
- 恒久対策（組織向け）：必要なら許可リストを設定するか、セキュリティチームがCloudflareへ再評価を依頼する。ユーザー向けには影響範囲と回避方法を通知。
- 注意点：誤判定の可能性もあるので、即時のブロック解除要求には慎重に。根本原因（悪用か誤検出か）を特定して対応すること。

--- 
参考：Cloudflare Radarのドメインページは証明書履歴やURLスキャン結果、トラフィック指標を公開しており、原因調査に有用。
