---
layout: post
title: "Vinyl Cache has left github - Vinyl CacheがGitHubを離れました"
date: 2026-02-17T17:48:30.040Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://vinyl-cache.org/organization/moving.html"
source_title: "Vinyl Cache has left github &#8212; Varnish HTTP Cache"
source_id: 865144491
excerpt: "Vinyl CacheがGitHubを離脱、移行で必要なSSH・URL更新と注意点"
---

# Vinyl Cache has left github - Vinyl CacheがGitHubを離れました
魅力的なタイトル: GitHubから独立したVinyl Cache──移行で押さえるべき3つの手順

## 要約
Vinyl CacheはGitHub上のリポジトリ群を自前のForgejoインスタンス（https://code.vinyl-cache.org/）に移行しました。利用者はリポジトリURL・SSH設定・ブランチ名の変更に対応する必要があります。

## この記事を読むべき理由
日本の運用者や開発者も、オープンソースプロジェクトのホスティング移行に直面する可能性があります。移行手順やトラブルの実例は、自分のプロジェクトで同様の作業を行う際の参考になります。

## 詳細解説
- 移行先は自前ホスティングのForgejo: https://code.vinyl-cache.org/vinyl-cache/  
  参加・コラボレーションを続けたい場合は、同サイトでアカウント登録が必要（記事公開時点で登録期限あり：2026-02-18T19:51:32+01:00）。
- URL/名前規則（変換ルール）:
  - Webプレフィックス: https://github.com/varnishcache/ → https://code.vinyl-cache.org/vinyl-cache/
  - プロジェクト名内の "varnish" → "vinyl"
  - main/trunk ブランチは main に統一
  - sed で表すと概ね:
```bash
sed -e 's:github.com/varnish:code.vinyl-cache.org/vinyl-:; s:varnish:vinyl:'
```
- git クローン／SSH の変更:
  - HTTPS 例: https://github.com/varnishcache/varnish-cache → https://code.vinyl-cache.org/vinyl-cache/vinyl-cache
  - SSH 例: git@github.com:varnishcache/varnish-cache.git → git@code.vinyl-cache.org:vinyl-cache/vinyl-cache.git
- ブランチ名とPR影響:
  - master→main の切り替えで、PRのベースが変わり自動で閉じられる等の副作用が出た。ForgejoではDB直接修正で復旧できたが、同様のリスクを認識すること。
- 運用面:
  - 重要リポジトリには最終タグとREADME追記、GitHubは archived に設定して移行完了を周知。
  - CI（vtest等）や自動サイト更新の復旧が移行後の優先作業。将来的に読み取り専用ミラーを追加予定。

- 移行を自分の環境で自動化するサンプルスクリプト（リポジトリ内で実行）:
```bash
#!/bin/bash
## call this from a varnish-cache git directory
set -eux
top=$(git rev-parse --show-toplevel)
cd "${top}"
origin=origin
newurl=$(git remote get-url "${origin}" | sed -e 's:github.com\([\:/]\)varnishcache:code.vinyl-cache.org\1vinyl-cache:;s:varnish:vinyl:')
git remote set-url "${origin}" "${newurl}"
git fetch
# rename master to main (create main from master)
git checkout -b main master
git branch -u origin/main main
git branch -d master
if [[ "${top}" == *varnish* ]] ; then
  new="${top/varnish/vinyl}"
  mv "${top}" "${new}"
  echo NOW CALL: cd "${new}"
fi
```

## 実践ポイント
- まず新Forgeでアカウント登録（期限に注意）。確認メールが届かない場合はSPAMフォルダを確認。
- 自分のクローン済みリポジトリで上記スクリプトを実行し、remote とブランチ名を一括更新する。
- CI・デプロイ設定（リモートURLやブランチ指定）を見直す。PRのベース変更で閉じられたPRがないか確認する。
- READMEやドキュメントに移行先URLを明示し、依存するチームへ通知する。
- 自前ホスティング移行の教訓として、タグ/READMEの追記、アーカイブ手順、DBレベルの影響を想定したロールバック手順を用意する。
