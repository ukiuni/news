---
layout: post
title: "Block the \"Upgrade to Tahoe\" Alerts - 「Tahoeへのアップグレード」通知をブロックする方法"
date: 2026-02-28T22:22:10.064Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://robservatory.com/block-the-upgrade-to-tahoe-alerts-and-system-settings-indicator/"
source_title: "Block the &#8220;Upgrade to Tahoe&#8221; alerts and System Settings indicator &#8211; The Robservatory"
source_id: 47198977
excerpt: "構成プロファイルでTahoeへの通知を90日間抑え、手動再適用で旧UIを維持する方法を解説"
---

# Block the "Upgrade to Tahoe" Alerts - 「Tahoeへのアップグレード」通知をブロックする方法
Tahoeの押し売り通知を90日ずつ封じる—面倒なアップデートバッジと通知を一時的に消す現実的トリック

## 要約
macOSの「Tahoe（macOS 26）」への大型アップデート通知を、構成プロファイルで最大90日間ブロックする手順を紹介する記事の翻訳＆解説です。

## この記事を読むべき理由
TahoeのUI（Liquid Glass等）や機能変更が嫌で旧バージョン（例：Sequoia）を使い続けたい人、あるいは企業で段階的に展開したい管理者にとって、毎回出る赤い通知や自動促進を抑えられる実践的な手段だからです。ただし重要なセキュリティ更新の扱いには注意が必要です。

## 詳細解説
要点は「構成プロファイル（device management profile）」を使い、メジャーアップデート関連のアクティビティを90日間延期（defer）する設定を適用すること。Stop Tahoe UpdateというGitHubプロジェクトにあるdeferral-90days.mobileconfigがそれを提供します。手順の概要：

1. リポジトリをクローンしてディレクトリへ移動
```bash
git clone https://github.com/travisvn/stop-tahoe-update.git
cd stop-tahoe-update
```

2. スクリプトに実行権を付与（READMEにない重要手順）
```bash
chmod 755 ./scripts/*.sh
```

3. deferral-90days.mobileconfig を編集して2つのPayloadUUIDを生成・差替え（uuidgenを2回実行）
```bash
uuidgen
uuidgen
# 出力されたUUIDをprofiles/deferral-90days.mobileconfig内のREPLACE-WITH-UUIDにそれぞれ貼る
```
4. オプション：副作用を減らすために小さな更新は受け取りたいなら
profilesファイル内の
```xml
<key>forceDelayedSoftwareUpdates</key><true/>
```
を
```xml
<key>forceDelayedSoftwareUpdates</key><false/>
```
に変える（minorアップデートは通常通り受け取る）。

5. プロファイルをインストール：
```bash
./scripts/install-profile.sh profiles/deferral-90days.mobileconfig
```
Sequoia系ではprofilesコマンドが使えないためスクリプトは「Profilesを使ってSystem Settingsで承認してね」という指示を表示します。System Settings（環境によっては「Profile Downloaded」や「Privacy & Security → Profiles」）を開き、ダウンロードされたプロファイルを選んで「Install」をクリックして有効化します。

6. 再適用の簡略化（任意）：90日ごとに手動で繰り返す場合、.zshrc等にエイリアスを作ると便利です。
```bash
# bash/zsh例
alias notahoe='open "/path/to/deferral-90days.mobileconfig"; sleep 2; open "x-apple.systempreferences:com.apple.preferences.configurationprofiles"'
```

注意点：
- この手法は構成プロファイル仕様で許される最大の90日間の延期に依拠します。永続的に遮断するものではありません。90日ごとに再インストールが必要です。
- macOSのバージョンやAppleの挙動（例：15.7.3のバグ）によって動作が異なる可能性があります。SOFAなどのリリース・ディフerral表も参照すると良いです。
- セキュリティアップデートを無視するのは危険なので、重要なセキュリティパッチは別途適用することを推奨します。

## 実践ポイント
- まずはローカルで一台だけ試して挙動を確認する（企業導入前の必須手順）。
- 小さなアップデートは受け取りたい場合は forceDelayedSoftwareUpdates を false に設定する。
- 90日ごとの再適用が面倒なら、.zshrcのエイリアスでワンクリック再インストールとProfilesパネル表示を用意する。
- 管理者（MDM）環境なら同等の構成プロファイルをMDMから配布すれば中央管理できる。
- 常にセキュリティ通知とAppleのパッチ情報を確認して、重要な修正を見逃さないようにする。
