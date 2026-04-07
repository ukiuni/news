---
layout: post
title: "Running Out of Disk Space in Production - 本番でディスク容量が枯渇した話"
date: 2026-04-07T13:19:45.293Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://alt-romes.github.io/posts/2026-04-01-running-out-of-disk-space-on-launch.html"
source_title: "Running out of Disk Space in Production"
source_id: 47627217
excerpt: "同時ダウンロードで本番ディスクが枯渇、nginx設定と/nix分離で即復旧した事例"
---

# Running Out of Disk Space in Production - 本番でディスク容量が枯渇した話
公開直後にディスクが満杯に—nginxの設定が招いた実戦的トラブルと即効対処法

## 要約
公開直後の同時アクセスでディスクが100%になりサービス停止。原因は（1）/nix を含むストレージ割当と（2）nginxのプロキシ設定による一時ファイル肥大。ボトルネックの特定と設定修正で復旧した事例。

## この記事を読むべき理由
同時ダウンロードや大容量ファイル配信は日本の小規模クラウド環境でも起きやすい。短時間で復旧するための調査手順とnginx周りの落とし穴を知っておけば、本番事故を素早く収束できる。

## 詳細解説
- 環境と症状：Hetznerの小容量VM (NixOS, 4GB RAM, 40GB disk)。配布ファイルが2.2GBで、公開直後の同時アクセスでメール送信やダウンロードが失敗。dfでルートが100%。
- 初動調査：du -shで大きいディレクトリを確認。/var/lib（ClickHouse）約8.5GB、/nix/store 約15GBを発見。nix-collect-garbage が「No space left」で失敗し、journalctl --vacuum-time=1s でログを掃除して一時的に空きを確保。
- ストレージ対策：/nix を別ボリュームに移動（ext4でラベル付け→fstab相当の宣言的設定に登録）してルートの空きを確保。再起動で効果あり。
- 大容量ファイルが落ちる原因：nginxがプロキシのレスポンスを一時ファイルにバッファリングしており（デフォルト proxy_max_temp_file_size 1024m）、2.2GBの配信中に大量の一時ファイルが生成され、さらに削除済みだがプロセスが保持しているファイルがディスクを圧迫（lsof +L1 で約14.5GiB検出）。
- 根本修正：nginxのproxy_bufferingを無効化、または proxy_max_temp_file_size を適切に設定すると一時ファイル生成を防げる。記事では proxy_buffering off と proxy_max_temp_file_size 0 を適用して解決。

重要なコマンド（調査・復旧例）:
```bash
# ディスク使用量確認
df -h
du -sh /* | sort -h

# 古いjournalを削除（急場）
journalctl --vacuum-time=1s

# 開かれたが削除されたファイルを検出
lsof +L1 | grep nginx
lsof +L1 | awk '/nginx/ {sum += $7} END {print sum/1024/1024/1024 " GiB"}'
```

nginx設定例（NixOSのextraConfig風）:
```nix
# /etc/nixos/configuration.nix の relevant 部分
"/" = {
  proxyPass = "http://127.0.0.1:8000/";
  extraConfig = ''
    proxy_buffering off;
    proxy_max_temp_file_size 0;
  '';
};
```

## 実践ポイント
- 大きなファイルを配るなら、事前にプロキシのバッファ設定（proxy_buffering / proxy_max_temp_file_size）を確認・試験する。
- 重要なストア（/nix やデータベースの格納先）は別ボリュームに分離して容量不足の影響範囲を限定する。
- 緊急時は journalctl の掃除で短時間の空きを作り、余裕ができたら安全にガベージコレクションを実行する。
- 削除済みだがプロセスが保持するファイルは lsof +L1 で確認してプロセス再起動で解放する。
- 本番リリース前に「大容量ファイル同時ダウンロード」の負荷試験を行う（nginx/アプリ挙動の確認）。

― 以上、nginxのプロキシ設定とストレージ分離で本番ディスク枯渇から復旧した実例。迅速な原因特定と小さな設定変更で被害を抑えられる点が学べる。
