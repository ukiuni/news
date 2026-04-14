---
layout: post
title: "The Open Sourcerer of Forem: Beyond the UI - Foremのオープンソーサラー：UIを超えて"
date: 2026-04-14T13:32:57.077Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/francistrdev/the-open-sourcerer-of-forem-beyond-the-ui-4k7p"
source_title: "The Open Sourcerer of Forem: Beyond the UI - DEV Community"
source_id: 3496217
excerpt: "ForemのUIバグ修正で学ぶ、OSS初貢献の具体手順とコツ"
image: "https://media2.dev.to/dynamic/image/width=1200,height=627,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fur7eux8e1dcyjhay62cq.jpg"
---

# The Open Sourcerer of Forem: Beyond the UI - Foremのオープンソーサラー：UIを超えて
はじめてのOSS貢献が一歩ずつ「できる」に変わる — Dev.to（Forem）でUIバグを直して得た実務的な気づき

## 要約
Dev.toを支えるForemリポジトリで報告されたUIの重なり（z-index）問題を、クラス探索→SCSS修正→PR提出の流れで解決した体験記。単純な修正でも学びは大きいという話。

## この記事を読むべき理由
日本でもOSS参加のハードルは高く感じられがちだが、実際は「小さなUI修正」から始められること、作業の進め方とコミュニケーションのコツが分かるため。

## 詳細解説
- 発端：コメントの「いいね」と絵文字リアクションが重なり、表示が崩れるというIssue（z-indexの不備）。
- 再現手順：該当投稿のコメント上でリアクションにマウスを重ねると重なりが確認できる（報告者がスクショ添付）。
- 調査方法：ブラウザの開発者ツールで該当要素のクラス名（crayons-article-actions）を特定し、Visual Studio Codeでリポジトリ内を検索してSCSSファイルを発見。
- 仮修正：問題部分のz-indexを一時的に大きな値（例：9999）に変更して表示を直すPRを作成。これは速攻で効くが最適解ではない。
- 継続改善：メンテナによって「ドロップダウンより上、モーダルより下」といった意図を残すため、最終的にはcalc(var(--z-dropdown) - 1) のような相対指定で整理された。
- コラボの学び：最初のPRがマージされないことは普通。Issueを読み、リポジトリのニーズに合わせて小さく確実に進め、進捗をコメントで共有することが重要。

## 実践ポイント
- 小さなIssue（UIやドキュメント）を狙う：コードベース理解の近道。
- まずはブラウザの開発者ツールで要素のクラス/IDを特定→VS Codeで全体検索。
- ローカル環境で動かして確認：localhostでの再現は信用度を高める。
- 修正は最小限に：一時的な高z-indexは可だが、最終的には設計に合わせた相対指定を提案する。
- PRには再現手順とスクショ、QA手順を明記する（メンテが楽になる）。
- コミュニケーションを忘れずに：Issueで進捗報告、期限（リポジトリのルール）を確認する。
- 継続的に学ぶ：失敗や却下も経験値。日本のエンジニアにも合う、慎重で丁寧な貢献スタイルが歓迎される。

元記事はForem（Dev.to）への寄稿体験で、OSS参加の心理的ハードルの下げ方と実務的な手順を具体的に示しています。まずは「小さく直してPRを出す」ことを試してみてください。
