---
layout: post
title: "A one-line Kubernetes fix that saved 600 hours a year - 1行のKubernetes修正で年間600時間を取り戻した"
date: 2026-03-27T18:01:07.351Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.cloudflare.com/one-line-kubernetes-fix-saved-600-hours-a-year/"
source_title: "A one-line Kubernetes fix that saved 600 hours a year"
source_id: 1145980919
excerpt: "fsGroupChangePolicyを一行変更しPV再起動を30分→30秒に短縮、600時間節約"
image: "https://cf-assets.www.cloudflare.com/zkvhlag99gkb/wl0SJ0AVuinUobub2XxJr/aee61d15c87b32063fdee8205106350d/OG_Share_2024-2025-2026__25_.png"
---

# A one-line Kubernetes fix that saved 600 hours a year - 1行のKubernetes修正で年間600時間を取り戻した
ワンライナーで復旧が30分→30秒に。大量ファイルのPVで再起動が止まる原因と超簡単な直し方

## 要約
Cloudflareが、Atlantis（Terraform運用ツール）の再起動が30分かかっていた原因を突き止め、podのセキュリティ設定を1行変えるだけで再起動時間を30秒に短縮し、年間約600時間を取り戻した話です。

## この記事を読むべき理由
大量ファイルを持つPersistentVolume（PV）を使う日本のSRE／プラットフォームチームやTerraform運用者は、Kubernetesの「安全なデフォルト」がスケール時に致命的なボトルネックになることを見落としがちです。簡単に適用できる対策で大幅な工数削減が期待できます。

## 詳細解説
- 症状：Atlantisを再起動するとPodはすぐスケジュールされるが、Init段階で30分以上「Init:0/1」のまま停止。月100回近い再起動で毎月50時間以上の待ちが発生。
- 原因探索：Podイベントだけでは原因不明。ノード上のkubeletログ（Kibana経由）を掘ると、PVのマウント直後に次のログが出力されていた。
  - 「Setting volume ownership ... and fsGroup set. If the volume has a lot of files then setting volume ownership could be slow」
- 原理：Podのspec.securityContextでfsGroupを設定すると、kubeletがPVをマウントする際にfsGroupに合わせてファイル所有権を再帰的に変更（chgrp -R 相当）する。PVに数百万ファイルがあるとこの再帰処理が非常に遅くなり、kubeletのタイムアウトや「No sandbox」ループを引き起こす。
- プラットフォーム事情：Cephのストレージでmkfsのinode設定が渡せず、inode枯渇→PVサイズ変更で再起動が発生しやすいケースが発覚。単にアラート延長では根本対処にならない。
- 解決策：Kubernetes v1.20以降で使えるpod.spec.securityContext.fsGroupChangePolicyをデフォルトのAlwaysからOnRootMismatchに変更。これによりrootディレクトリの権限が正しければ再帰的な所有権変更をスキップでき、再起動が劇的に速くなる。
- 効果：再起動時間が約30分→約30秒に短縮。月50時間、年間約600時間の工数回収に相当。

## 実践ポイント
- まずPod定義を確認：fsGroupを使っているか、fsGroupChangePolicyが未設定（＝Always）かをチェック。
- すぐ使える1行（YAML例）：

```yaml
apiVersion: apps/v1
kind: StatefulSet
spec:
  template:
    spec:
      securityContext:
        fsGroupChangePolicy: OnRootMismatch
```

- 運用上の注意：
  - OnRootMismatchを使う前に、PV上のルートディレクトリの所有権・グループが期待通りか検証すること。
  - 既存のファイル作成プロセス（init jobやコンテナのUID/GID）で権限がおかしくならないか確認すること。
  - 大容量PVを使う環境では、kubeletログ（ノード側）やCSI/volumeログも合わせて監視すると原因特定が早い。
- 日本市場への示唆：GitLab＋AtlantisやTerraformを使うチーム、オンプレCephや大規模EBS/NFSを使うSREは特に要チェック。小さな「安全設定」がスケールで大きなコストになることがあります。

以上。シンプルな設定見直しで実働時間を大幅に取り戻せます。
