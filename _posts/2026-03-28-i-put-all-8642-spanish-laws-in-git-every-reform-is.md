---
layout: post
title: "I put all 8,642 Spanish laws in Git – every reform is a commit - スペインの8,642本の法令をGitに――改正はすべてコミットに"
date: 2026-03-28T13:00:48.045Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/EnriqueLop/legalize-es"
source_title: "GitHub - EnriqueLop/legalize-es: Spanish legislation as a Git repo — every law is a Markdown file, every reform a commit. 8,600+ laws. · GitHub"
source_id: 47553798
excerpt: "法改正履歴をそのままコミット化、スペイン8,642法令をGitで公開"
image: "https://opengraph.githubassets.com/109c5bdde38b270d87ce8ac79f4ba241fa53e40ee6414ebea32ebe5a37f4b85a/EnriqueLop/legalize-es"
---

# I put all 8,642 Spanish laws in Git – every reform is a commit - スペインの8,642本の法令をGitに――改正はすべてコミットに

法改正の履歴がそのままGitのコミットになる――法律を“ソースコード”のように扱うオープンな試み。

## 要約
スペインの公的法令（8,600+）をMarkdownファイル化し、各改正を別コミットとして履歴管理したリポジトリ。公式APIのデータを使い、1960年代以降の改正をそのままGitで追えるようにしている。

## この記事を読むべき理由
法令の差分追跡・監査・自動検知は法務・コンプライアンス・行政向けの強力な基盤。日本でも同様のデータ活用が進めば、法改正対応の自動化や透明性向上に直結するため、エンジニア／法務の両方に示唆がある。

## 詳細解説
- 何をしているか：BOE（スペイン官報）の「Consolidated Legislation API」から法令テキストを取得し、各法をMarkdownファイル（frontmatterにメタデータ）として格納。各「改正」は公式公開日をコミットの作成年としてコミットし、メッセージに改正IDとソースURLを明記。
- 規模と履歴：8,600超の法令ファイルと約27kのコミットで、1960年代以降の改正履歴を完全に辿れる構成。
- リポジトリ構造：spain/BOE-A-1978-31229.md（例：憲法）といったファイル群。YAML frontmatterにtitulo、identificador、fecha_publicacion、estado、fuenteなどを保持。
- 技術的利点：git log / git diff / grep 等で特定条文の改正差分を簡単に抽出できる。CIで差分検出→通知、自動マージルール、法令全文検索API構築などが実装しやすい。
- ライセンス／出所：法文本体は公的資料でパブリックドメイン。リポジトリは構造やツールをMITで公開。
- 日本との関連：日本にも「法令データ提供システム」や官報APIがあり、同様の手法で法令のバージョン管理・差分配信・監査ログ化を進められる。自治体や事業会社のコンプライアンス自動化、リーガルテック製品のデータ基盤として応用可能。

簡単な利用例：
```bash
# リポジトリをクローンして特定条文を追う
git clone https://github.com/EnriqueLop/legalize-es.git
cd legalize-es
grep -A 10 "Artículo 135" spain/BOE-A-1978-31229.md
git log --oneline -- spain/BOE-A-1978-31229.md
git diff 6660bcf^..6660bcf -- spain/BOE-A-1978-31229.md
```

## 実践ポイント
- まずはクローンして気になる条文をgit log / git diffで追ってみる。差分運用の利便性がすぐに分かる。  
- CIで定期pull→diff検出→Slack/メール通知を組めば改正監視が自動化できる。  
- 日本の官報APIや法令データを同様にパイプライン化し、改正履歴をGitで管理するプロトタイプを作る価値あり。  
- 法務チームと共同で差分ルール（重要条文のタグ付け、影響範囲判定）を設計すると運用効果が高まる。
