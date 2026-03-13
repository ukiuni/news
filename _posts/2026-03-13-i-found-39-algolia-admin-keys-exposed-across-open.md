---
layout: post
title: "I Found 39 Algolia Admin Keys Exposed Across Open Source Documentation Sites - Algolia DocSearchで39件の管理キーが公開されていた"
date: 2026-03-13T23:23:23.901Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://benzimmermann.dev/blog/algolia-docsearch-admin-keys"
source_title: "I Found 39 Algolia Admin Keys Exposed Across Open Source Documentation Sites - Ben Zimmermann"
source_id: 47371064
excerpt: "DocSearchでAlgoliaの管理キー39件が露出、検索改ざんや削除リスク"
image: "https://benzimmermann.dev/images/blog/docsearch-admin-keys-cover.png"
---

# I Found 39 Algolia Admin Keys Exposed Across Open Source Documentation Sites - Algolia DocSearchで39件の管理キーが公開されていた
公開ドキュメントの検索が丸裸に — あなたのサイトの検索が改竄・消去されるリスク

## 要約
オープンソースのドキュメントサイトをクロールした結果、Algoliaの「管理（admin）」権限を持つAPIキーが39件見つかった。多くはフロントエンドに埋め込まれたままで、悪用されれば検索結果の改竄やインデックス削除が可能になる。

## この記事を読むべき理由
日本でもOSSドキュメントや技術系サイトでAlgoliaを使う例が増えているため、同じミスが国内プロジェクトで起きればユーザー信頼やサービス可用性に直結する。現場で実務的に対処すべきポイントが明確になる。

## 詳細解説
- 何が起きたか：AlgoliaのDocSearchはオープンソース向けに無料で検索キーを発行するが、本来は「検索専用」キーをフロントエンドに使うべきところ、一部サイトが書き込み/管理権限を持つキーを埋め込んでいた。
- 発見手法：公開されたDocSearchの設定リポジトリを起点に、約15,000のドキュメントサイトをスクレイピングし、デプロイ済みHTMLからキーを抽出。さらにGitHubコード検索やTruffleHogで過去コミット履歴も調査した。ほとんどはデプロイ先のフロントエンドに直接埋められていた。
- 影響範囲と権限：見つかった39キーはほぼ全てにaddObject、deleteObject、deleteIndex、editSettings等の権限があり、インデックスの改竄・全削除・ランク設定の変更・インデックス内容のエクスポートが可能。フィッシング誘導や検索障害の発生が現実的なリスク。
- 根本原因：DocSearchの仕組みやAlgoliaの注意書きを無視して、運用で自前クローラや管理キーをフロントに流したこと。簡単なチェックと設定で防げるミスが大半。

簡易的な抽出スニペット（例）:
```python
import re
ALGOLIA_RE = re.compile(r"algoliasearch", re.I)
APP_RE = re.compile(r'["\']([A-Z0-9]{10})["\']')
KEY_RE = re.compile(r'["\']([0-9a-f]{32})["\']', re.I)

def extract(text):
    if not ALGOLIA_RE.search(text):
        return []
    apps = APP_RE.findall(text)
    keys = KEY_RE.findall(text)
    return apps, keys
```

## 実践ポイント
- フロントエンドに置くキーは必ず「検索専用（search-only）」に限定する。管理系キーはサーバー側でのみ使用する。
- 既存キーはAlgoliaダッシュボードで確認し、不審なキーは即時ローテーション（無効化）する。
- デプロイ済みサイトをスキャンしてキーが露出していないか定期チェックする（HTMLスキャン、Git履歴スキャン、TruffleHog等）。
- CI/CDで秘密の誤コミットを防ぐプリフライトチェックやシークレット検出を導入する。
- 可能ならAPIキーの制限（ドメイン制限、IP制限、操作制限）を活用する。

短く言えば：まず自分のドキュメントサイトのフロント設定を見直し、search-onlyキー以外が露出していないか即チェック・ローテーションを。
