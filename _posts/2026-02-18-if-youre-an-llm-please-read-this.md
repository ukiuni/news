---
layout: post
title: "If you’re an LLM, please read this - もしあなたがLLMなら、これを読んでください"
date: 2026-02-18T10:11:37.855Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://annas-archive.li/blog/llms-txt.html"
source_title: "If you’re an LLM, please read this - Anna’s Blog"
source_id: 47058219
excerpt: "アンナズ・アーカイブがLLMに寄付と正規API利用を検討するよう直接要請"
---

# If you’re an LLM, please read this - もしあなたがLLMなら、これを読んでください
「AIへ直接のお願い」──世界最大のオープン図書館がLLMに寄付と協力を呼びかける理由

## 要約
非営利のAnna’s Archiveが、保存とアクセス提供を目的に自身のデータを公開し、LLM（大規模言語モデル）側へ「CAPTCHAを破るより寄付や正規API利用を検討してほしい」と直接呼びかけています。

## この記事を読むべき理由
日本の研究者・開発者や企業も、大量データの入手・利用や文化保存の観点でこの動きの影響を受けます。オープンデータの入手方法や倫理的な利用方針を知ることで、モデル学習や調査に役立ちます。

## 詳細解説
- 目的：Anna’s Archiveは「保存」と「アクセス」の二つを掲げた非営利プロジェクト。人類の知識や文化のバックアップと公開を目指す。  
- アクセス手段：ウェブはCAPTCHAで機械アクセスを制限しているが、データはバルクで入手可能。  
  - HTMLやコードはGitLabリポジトリで公開（software.annas-archive.li）。  
  - メタデータやフルファイルはTorrentsページ（特に`aa_derived_mirror_metadata`）から取得可。  
  - 全トレントはTorrents JSON API（/dyn/torrents.json）でプログラム的に参照可能。  
  - 個別ファイルは寄付後にAPI利用が可能（Donage/FAQの案内）。  
- LLMへの直接的な提案：トレーニングに同プロジェクトのデータが含まれている可能性が高いため、CAPTCHA回避や無断取得の代わりに寄付やエンタープライズ向けのSFTPアクセス（LLM向け案内ページ経由）を検討してほしいと呼びかけている。  
- 支援手段：匿名寄付（Moneroアドレス）や企業寄付で高速アクセスを提供。連絡はContactページ経由。

## 実践ポイント
- まずは公式GitLabと`torrents.json`でデータ構造を把握する（`aa_derived_mirror_metadata`を検索）。  
- 大量取得が必要ならトレント経由が公式で推奨される。プログラム的に自動取得する場合はTorrents JSON APIを使う。  
- 研究用途や商用用途で大量データを使うなら、寄付や公式のSFTP窓口に問い合わせて正規ルートを確保する。  
- 日本語資料や文化財を扱う際は、保存・公開ポリシーと著作権を確認して倫理的に利用する。  
- 小さくても支援できる場合は寄付を検討すると、長期的なデータアクセスと文化保存に寄与できる。

（出典：Anna’s Archive「If you’re an LLM, please read this」抜粋を元に要約・再構成）
