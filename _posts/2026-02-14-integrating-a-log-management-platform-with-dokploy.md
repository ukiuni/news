---
layout: post
title: "Integrating a log management platform with Dokploy - Dokployにログ管理プラットフォームを統合する方法"
date: 2026-02-14T18:14:36.559Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tanin.nanakorn.com/integrating-a-log-management-platform-with-dokploy/"
source_title: "Integrating a log management platform with Dokploy"
source_id: 441744102
excerpt: "DokployでCompose不要、fluent-bitをホストで動かしNewRelicへログ送信"
image: "https://tanin.nanakorn.com/content/images/size/w1200/2024/11/banner-1.png"
---

# Integrating a log management platform with Dokploy - Dokployにログ管理プラットフォームを統合する方法
Docker環境で動くDokployに対して、軽量なfluent-bit＋New Relicプラグインでログを素早く流し込む実践ガイド

## 要約
Dokployは`--log-driver`を直接サポートせず、Docker Composeを使わずに外部ログ基盤へ送るには工夫が必要。解決策として、ホスト上でfluent-bit＋New Relic出力プラグインを動かし、/var/lib/docker/containers/*/*.log を読ませる方法が手早く確実。

## この記事を読むべき理由
- Dokployを使う日本の開発チームで、Docker Composeを避けたい／軽量なログ収集をしたい人向け。  
- New Relicなど商用ログ基盤へ素早く接続する実務的な設定が学べる。

## 詳細解説
背景
- 著者はNew Relic、OpenObserve、Papertrailを検討。最終的にUXと導入のしやすさでNew Relicを採用。OpenObserveはANSI色に非対応、Papertrailはサインアップで失敗したため断念。
- 理想はDockerの`--log-driver=fluentd`でnrLicenseKeyタグを渡す方法だが、Dokployは`--log-driver`の良いサポートがなく、Docker Composeに頼る必要があるため回避したいという制約。

採用したアプローチ
- ホスト上でfluent-bit（軽量で高性能）を動かし、Dockerが出力するJSONログファイルを直接tailしてNew Relicへ送信する構成を採用。
- fluent-bitはfluentdと互換性があり、プラグイン経由でNew Relicへ送れる。

主要設定例（抜粋）
- /etc/fluent-bit/fluent-bit.conf（入力はDockerログのパース、出力はnewrelicプラグイン）

```ini
[INPUT]
    Name        tail
    Path        /var/lib/docker/containers/*/*.log
    Path_Key    filepath
    Tag         docker_tail.*
    Parser      docker
    DB          /var/log/flb_docker.db
    Mem_Buf_Limit 5MB
    Skip_Empty_Lines On
    Docker_Mode On

[SERVICE]
    Parsers_File parsers.conf
    Plugins_File plugins.conf

[FILTER]
    Name record_modifier
    Match *
    Record hostname ${HOSTNAME}

[OUTPUT]
    Name newrelic
    Match *
    licenseKey <YOUR_LICENSE_KEY>
```

- /etc/fluent-bit/plugins.conf（New Relic出力プラグインのパス指定）

```ini
[PLUGINS]
    Path /home/ubuntu/out_newrelic-linux-amd64-3.4.0.so
```

- /etc/fluent-bit/parsers.conf（DockerのJSONログをパース）

```ini
[PARSER]
    Name   docker
    Format json
    Time_Key time
    Time_Format %Y-%m-%dT%H:%M:%S.%L
    Decode_Field_As escaped log
```

プラグインは公式リリースからダウンロードする（例）
- https://github.com/newrelic/newrelic-fluent-bit-output/releases

注意点（ギャップ）
- 設定で付与している `Path_Key` が filepath 属性を追加するが、これにはコンテナIDハッシュを含むフルパスが入り、サービス名が分かりにくい。サービス名を流すには別途対策（コンテナラベルを取り込む、正規表現でfilepathを解析、fluent-bitのLua/modifyフィルタで抽出など）が必要。

## 実践ポイント
- まずはホストにfluent-bitをインストールし、上記のconfを配置してテスト送信する。  
- New RelicプラグインはGitHubリリースからバイナリをダウンロードしてplugins.confで指定する。  
- サービス名を付与したい場合は（短期的） filepath を正規表現で切り出すか、（中長期）コンテナ起動側でラベルを付け、fluent-bitでラベルを読み込むフィルタを追加する。  
- Dokployの`--log-driver`サポート改善（Issue #3132）を追うと、将来的にもっとスマートな連携が可能になる。

以上を試せば、Docker Composeを使わずにDokploy環境からNew Relicへ効率的にログを流すことができます。
