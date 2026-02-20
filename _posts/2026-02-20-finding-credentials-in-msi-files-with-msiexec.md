---
layout: post
title: "finding credentials in .msi files with msiexec - .msi内の資格情報をmsiexecで発見"
date: 2026-02-20T20:33:36.129Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ljb.fyi/your-msi-isnt-an-executable/"
source_title: "your .msi isn&#x27;t an executable | nonobvious nonsense"
source_id: 1237345119
excerpt: "msiexecでMSIを展開すると平文ドメイン管理者パスが内部配布で露出"
image: "https://bear-images.sfo2.cdn.digitaloceanspaces.com/herman-1683556668-0.png"
---

# finding credentials in .msi files with msiexec - .msi内の資格情報をmsiexecで発見
内部配布ツールが“誰でも読めるドメイン管理者のパスワード”を隠し持っていた話 — あなたの社内配布物も他人事じゃない

## 要約
msiexecの「管理者インストール」で.msiを展開すると、中に含まれるスクリプトやファイルがそのまま取り出せる。実際にVDスクリプトに平文のドメイン管理者資格情報が埋め込まれていて、社内アクセス権を持つ多くの人が読める状態だった。

## この記事を読むべき理由
国内でもMSIでの社内配布やベンダー配布が多く、知らないうちに「配布パッケージ＝安全ではない」状況が発生し得ます。秘密情報の埋め込みや権限管理の甘さは、インシデントに直結するため今すぐチェックすべきです。

## 詳細解説
- MSIは単なる「実行ファイル」ではなく、インストーラのデータベースと圧縮ファイル群。`msiexec /a`（管理者インストール）で中身を展開できる。
- 事例では、社内で配布されていたドメイン参加用ツールの.msiを展開すると、Visual Basicスクリプト群が現れ、その中にJoinDomain(username, password, domain, OU)の呼び出しがあり平文パスワードが埋め込まれていた。
- その.msiは内部サイトで配布され、アクセス権は限定されているとされたが、実際はグループネストで500人超が含まれており、退職者や外部委託先まで到達するリスクがあった。
- 発見者はチーム→マネージャ→セキュリティへと報告し、対応を進めた（責任の所在と早期通報の重要性も示唆）。

検査・解析の基本ツール例:
- msiexecによる展開
- 7-Zip等のアーカイバで開く
- テキスト検索（PowerShellのSelect-String等）で「password」「admin」「OU」などを探す

## 実践ポイント
- 今すぐ社内で配布中のMSIをチェックする（展開してスクリプト/設定を検索）。
  ```batch
  msiexec /a C:\join.msi /qb TARGETDIR=C:\temp\join_unpack
  ```
  ```powershell
  Select-String -Path C:\temp\join_unpack\* -Pattern 'password','admin','Domain','OU'
  ```
- 平文の資格情報は絶対に埋め込まない。代わりに gMSA や機密管理サービス（Key Vault等）、一時トークンを使う。
- アクセス制御を見直す：配布サイトのグループ構成を再確認し、ネストされたグループで過剰に広がっていないか確認する。
- CI／レビュー段階で秘密検出（secret scanning）を導入し、サードパーティ／請負ベンダーの成果物もチェックするワークフローを作る。
- 発見したら速やかにセキュリティ窓口へ報告し、影響範囲の特定と資格情報のローテーションを行う。

短いまとめ：MSIは中身を覗ける「箱」です。配布パッケージに秘密を置かない、アクセスと検査を厳格にする――これだけで重大な露出を防げます。
