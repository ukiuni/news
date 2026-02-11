---
layout: post
title: "Merge multiple GitHub contribution graphs into one README heatmap - 複数のGitHub貢献グラフを1つのREADMEヒートマップに統合する"
date: 2026-02-11T09:10:59.285Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github-contribution-merger.vercel.app"
source_title: "GitHub Readme Contribution Merger — Combine Multiple GitHub Heatmaps | Apoorv Darshan"
source_id: 444505556
excerpt: "チームの複数GitHub貢献を合成しREADMEに埋め込み、視覚的に活動を一目で示すツール"
image: "https://github-contribution-merger.vercel.app/github-readme-og.png"
---

# Merge multiple GitHub contribution graphs into one README heatmap - 複数のGitHub貢献グラフを1つのREADMEヒートマップに統合する
魅せるチームプロフィールに変える——READMEに複数人分の貢献ヒートマップを合体して埋め込む方法

## 要約
複数のGitHubユーザーの貢献カレンダーを1つの埋め込みSVGヒートマップにまとめ、READMEに貼れるURL／Markdown／HTMLスニペットを生成するウェブツール（Apoorv Darshan 作）。

## この記事を読むべき理由
チームやOSSコミュニティの活動を一目で見せたい日本のエンジニアや採用担当、ポートフォリオ作成者に便利。プロフィールや組織READMEで「誰がどれだけ貢献しているか」を視覚的に表現できます。

## 詳細解説
- 機能
  - 複数のGitHubユーザー名を入力してヒートマップを生成（2人以上）。
  - 2つの表示モード：
    - Sum（合算）: 全ユーザーの貢献数を合算して単一の色スケールで表示。
    - Overlay（重ね表示）: 各ユーザーを別色レイヤーとして重ね、個別の貢献も判別可能。
  - カラー選択、背景（Light/Dark）、プレビュー表示、生成URLと埋め込み用のMarkdown/HTMLスニペット出力。
- 技術的ポイント
  - 出力は埋め込み可能なSVGイメージなのでREADME（Markdown）やHTMLに直接貼れる。
  - データは公開のGitHub貢献カレンダーから取得するため、公開プロフィールであれば誰でも可。ただしプライベート活動は反映されない点に注意。
  - Vercel等でホストされたフロントエンドが生成ロジックとSVGレンダリングを提供。大量リクエストやAPI制限に注意（キャッシュやrate limitの影響を受ける可能性）。
- 日本市場との関連
  - 日本のOSSコミュニティ、社内OSS活動、勉強会メンバー紹介などで視覚的に活動をアピールできる。採用ページや企業GitHub OrganizationのREADMEに使えば活動の見える化に有効。

## 実践ポイント
- 使い方（手順）
  1. ツールにGitHubユーザー名を2つ以上入力。
  2. 表示モード（Sum/Overlay）、色、背景を選択。
  3. 生成されたURLまたはMarkdown/HTMLスニペットをREADMEに貼る。
- README埋め込み例（Markdown）
```markdown
![Contributions](https://github-contribution-merger.vercel.app/api?users=user1,user2&mode=sum&color=00ff00)
```
- 注意点
  - プライベートリポジトリや非公開の貢献は反映されない。
  - 大規模チームでは色分けが見にくくなるため、Sum表示で合算やサブグループごとに分けて表示するのが実用的。
