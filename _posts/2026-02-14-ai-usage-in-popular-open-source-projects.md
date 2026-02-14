---
layout: post
title: "AI usage in popular open source projects - 人気オープンソースでのAI利用状況"
date: 2026-02-14T09:47:13.506Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tirkarthi.github.io/programming/2026/02/13/genai-oss.html"
source_title: "AI usage in popular open source projects"
source_id: 442060735
excerpt: "主要OSSで急増するAI活用の実態と開示・検証・運用の具体的対策をデータで示す"
---

# AI usage in popular open source projects - 人気オープンソースでのAI利用状況
魅力的な日本語タイトル: 「大手OSSは今、AIをどう使っているか？Spark解析から見る“利用実態と注意点”」

## 要約
主要OSS（Apache Spark, Airflow, CPython, .NET, curl など）でのAI利用は増加傾向だが、全体比はまだ小さく、プロジェクトごとに開示ルールや対応が分かれている。

## この記事を読むべき理由
日本企業やOSS貢献者は、AIコード生成の扱い（開示・ライセンス・セキュリティ）を実務で突き当たる問題として直面している。実データと方針例を知ることで、自社ルール作りやOSS貢献時のリスク管理に役立つ。

## 詳細解説
- 分析手法：著者はGitコミットメッセージ中の「Was this patch authored…」等の開示行をパースしてAI利用を集計。簡易スクリプトで「yes/no」とメタ情報（どのモデルか）を抽出している。  
  ```python
  # python
  import re
  from git import Repo
  repo = Repo("/path/to/repo")
  key = "Was this patch authored or co-authored using generative AI tooling"
  for c in repo.iter_commits():
      if key in c.message.lower():
          # 簡易パース例
          print(c.committed_datetime, c.message)
  ```
- Apache Spark：PRテンプレートでAI利用開示を必須化。2023/08以降の解析ではAI利用と明示されたコミットは約130件、非AIは約8411件（全体では1〜2%程度）。ただし2024→2026で利用は増加（2026年初頭に急増）。頻出ツールはAnthropic系（claude/sonnet/opus）、GitHub Copilot、Cursor。
- Apache Airflow：UIの多言語化などでAI支援を利用。生成されたPR説明文など低品質な自動PRが増え、Contributingドキュメントで開示の義務化を議論・適用。
- CPython：公式ポリシーは明確でないが、co-authored や generated-by 表記のコミットが散発的に存在。
- .NET：開発者コミュニティでCopilotの利用が広く事例として確認されている。
- cURL：AIを使った不正・誤報の報告増加が原因でバグバウンティ一時停止など運営負担が顕在化。
- ポリシー動向：Linux Foundation、Apache、PyPI、Fedora、Debian 等で議論・ガイドラインが整備中。NetBSDやGentooのように「LLM生成コードは原則禁止」と明示するプロジェクトもある。

## 実践ポイント
- PRテンプレートでAI利用の有無と「どのツール・どの程度」を必須開示にする。  
- AI生成コードは必ず人間がレビューし、テスト／ベンチマーク／セキュリティチェックを追加する。  
- ドキュメントやテストデータ生成、i18nなど「低リスクで生産性の高い用途」から導入する。  
- オープンソースに貢献する際は各プロジェクトのAIポリシーを確認し、企業内ルールも整備する（ライセンス・著作権・脆弱性）。  
- メンテナ負担（誤報や低品質PR）を考慮し、自動生成されたIssue/PRをそのまま投げない運用を徹底する。

結論：AIは実務で有用だが「開示・検証・ガバナンス」が鍵。日本の現場でもOSSへの貢献と社内開発で両方意識したルール作りが急務。
