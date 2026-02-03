---
layout: post
title: "GitHub Browser Plugin for AI Contribution Blame in Pull Requests - Pull RequestにおけるAI寄与“ブレーム”を表示するGitHubブラウザプラグイン"
date: 2026-02-03T15:17:53.582Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.rbby.dev/posts/github-ai-contribution-blame-for-pull-requests/"
source_title: "Github Browser Plugin for Ai Contribution Blame in Pull Requests | rbby.dev"
source_id: 46871473
excerpt: "PRの差分上で行単位のAI生成元と割合を可視化し、レビューとコンプライアンスを確認できる新ツール"
image: "https://blog.rbby.dev/og-base_hu_b9eeea61e6fcdc88.png"
---

# GitHub Browser Plugin for AI Contribution Blame in Pull Requests - Pull RequestにおけるAI寄与“ブレーム”を表示するGitHubブラウザプラグイン

PRで誰が（何が）書いたか一目で分かる――AI生成コードを行単位で追跡し、GitHubの差分表示に注釈を出す新しい試み

## 要約
git‑aiは行単位でAI寄与（モデル・プロンプト含む）をgitノートに保存して追跡し、VSCodeやブラウザ拡張（refined-github-ai-pr）でPull Request上にAI寄与注釈や寄与割合を表示できるようにするプロジェクトです。

## この記事を読むべき理由
AIコード生成ツールが一般化する中で、オープンソースや社内リポジトリで「どこまでAIが書いたか」を可視化するニーズが高まっています。日本のプロジェクト運営・コードレビュー品質・コンプライアンス対応に直結するため、開発現場での導入検討価値が高いです。

## 詳細解説
- 背景  
  - Claude Code、Copilot、Cursor等の低摩擦な生成ツールでAI寄与が増加。意図せずAI生成コードが混入するケースが現実問題になっている。  
  - 一部プロジェクトは完全にAI寄与を禁止するが、許容割合や運用ルールでのバランス検討も進むべき課題。

- git‑aiの仕組みと狙い  
  - 行単位で「AIによる生成か」「どのモデル・どのプロンプトか」を記録。  
  - メタデータはgit notesに保存され、コミットに紐づく形で移動するため履歴と一緒に残る。  
  - merge --squash、rebase、cherry-pick等の一般的なgit操作でも注釈が生き残るよう工夫されている。  
  - 実装はgitプラムビング中心で高速（大規模リポジトリでもほぼ影響なしと報告）。

- エディタ／PRでの可視化  
  - VSCode拡張ではガターでハイライトし、行選択やホバーでモデル・プロンプト情報を確認可能。  
  - ブラウザ向けにはrefined-github-ai-pr（Refined GitHubの派生）を作成し、GitHubのPull Requestの差分ビューにAI注釈と「人間 vs AIの寄与割合」メーターを表示する試みがある。  
  - 注意点：ブラウザ拡張はGitHubのHTML構造（クラス）を操作しているため、GitHub側の変更で壊れる可能性がある。

- エコシステムと支援機能  
  - 公式にPRダッシュボード集計（Stat Botの早期アクセス）などの機能も計画されているが、まだ発展途上。

## 実践ポイント
- まずローカルでgit‑aiを試して、既存ワークフローで付与されるメタデータの見え方を確認する。  
- VSCode拡張を導入して日常的なレビューでAI寄与を可視化し、差分の根拠（プロンプト）を確認する習慣を作る。  
- リポジトリのCONTRIBUTINGやレビュー基準に「AI寄与の許容割合」「必須表記」を明記して合意を取る。  
- ブラウザ拡張は便利だが脆弱性（HTML依存）に注意し、運用は検証環境から段階的に。  
- コミュニティ／OSS側にもフィードバックを送り、仕様やツールの成熟に貢献する。

（さらに試したい場合はgit‑aiとrefined-github-ai-prのリポジトリをチェックし、社内のポリシー検討と併せて導入を進めてください。）
