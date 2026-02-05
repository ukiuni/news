---
layout: post
title: "A small, shared skill library by builders, for builders. (human and agent) - 作り手による、作り手のための小さな共有スキルライブラリ（人間とエージェント）"
date: 2026-02-05T19:15:59.874Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/PsiACE/skills"
source_title: "GitHub - PsiACE/skills: A small, shared skill library by builders, for builders."
source_id: 46902789
excerpt: "短時間で導入できる実務向けPython/RustとLLM用スキル集、社内規約と自動化の即戦力に。"
image: "https://opengraph.githubassets.com/4ff8430194ba9574b371f9f9a6985584619e9d25225f48f863276678ab5fdf50/PsiACE/skills"
---

# A small, shared skill library by builders, for builders. (human and agent) - 作り手による、作り手のための小さな共有スキルライブラリ（人間とエージェント）
実務で使える“スキルの宝箱” — 小さくても強い、PsiACE/skills の活用法

## 要約
PsiACE/skills は、実務に即した小規模な「スキル」コレクションで、PythonやRustの実践的コーディング指針と、エージェント（LLM）向けのスキルを共有します。軽量で変更も速く、チームの作法やエージェント挙動のベースに最適です。

## この記事を読むべき理由
国内の開発チームが短時間で採用できる実践ガイドと、エージェント連携の土台を手に入れられるため。社内コーディング規約や自動化エージェント設計の起点として有効です。

## 詳細解説
- 目的と設計思想：リポジトリは「小さく、実践的」に保つことを重視。筆者らの実務経験と公開ソースから厳選したスキル群を提供し、学習・適用・変更が速いのが特徴。
- 主要コンテンツ：skills ディレクトリに個別スキル（例：friendly-python、piglet、fast-rust）があり、それぞれ「読みやすさ・リファクタ・レビューの実践指針」を中心にまとめられている。AGENTS.md などエージェント関連ドキュメントも含む。
- ドキュメントと開発フロー：mkdocs ベースでサイト化されており、ローカルプレビューやビルド用のコマンドが用意されている（下記参照）。小規模なコレクションであるため、学習コストが低く、チーム単位でカスタマイズしやすい。
- 公開先とライセンス：オンラインドキュメントは https://skills.psiace.me/。コレクションは設計上変化する可能性がある旨が明記されているため、最新版を追う運用が望ましい。

インストールやドキュメント操作に使う主要コマンド例：

```bash
# skills をプロジェクトに追加（ローカル）
pnpx skills add PsiACE/skills --skill='*'

# グローバルに追加
pnpx skills add PsiACE/skills --skill='*' -g

# docs の依存同期・ローカルプレビュー・ビルド
uv sync --group docs
uv run mkdocs serve -f mkdocs.yml
uv run mkdocs build -f mkdocs.yml
```

## 実践ポイント
- まずは friendly-python や fast-rust を読み、現行のコードレビュー規約と照らし合わせる。差分を小さく導入すると定着しやすい。  
- 社内のテンプレや PR チェックリストに該当スキルの要点を組み込む（例：命名、テスト方針、リファクタ基準）。  
- LLM を利用するチームは AGENTS.md を参照し、エージェント向けプロンプトや手順を標準化する。  
- mkdocs を使って社内用にドキュメントをビルドし、Teams/Slack で共有することで採用を加速。  
- 使ってみて改善点があればフォークしてカスタマイズ、または PR で貢献する。

短くても実務で役立つインプットを素早く取り入れたい開発チームにおすすめのリポジトリです。
