---
layout: post
title: "Media scraper Gallery-dl is moving to Codeberg after receiving a DMCA notice, claiming that its circumvention. - Mediaスクレイパー gallery-dl、DMCA通知を受けてCodebergへ移転を開始（回避行為を主張）"
date: 2026-04-07T11:18:24.095Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mikf/gallery-dl/discussions/9304"
source_title: "DMCA Takedown Notice by FAKKU, LLC · mikf/gallery-dl · Discussion #9304 · GitHub"
source_id: 368868229
excerpt: "gallery-dl、DMCAでGitHub退避→Codeberg移転：スクレイピングの法リスク"
image: "https://opengraph.githubassets.com/cd31bff0cca40766988f0b2eb4fbc3f22aff655215ad6a5bcec4ea348d529f5a/mikf/gallery-dl/discussions/9304"
---

# Media scraper Gallery-dl is moving to Codeberg after receiving a DMCA notice, claiming that its circumvention. - Mediaスクレイパー gallery-dl、DMCA通知を受けてCodebergへ移転を開始（回避行為を主張）

魅力的な日本語タイトル：Gallery-dlがGitHubから“逃げる”理由 — DMCAで問われるスクレイピングとオープンソースの境界

## 要約
人気のメディアダウンローダー「gallery-dl」がFAKKUからのDMCA（§1201／回避行為）通知を受け、GitHub上で該当ファイルの削除や履歴書き換えを要求され、最終的にCodeberg/GitLabへミラー移行を進めた事例。

## この記事を読むべき理由
GitHub依存の日本の開発者・プロジェクト管理者にとって、外部からの著作権・回避主張がリポジトリの存続や運用に直結する現実を示す。スクレイピング系ツールや公開コードのリスク管理を学べる実例だから。

## 詳細解説
- 問題点：FAKKUはgallery-dl内の以下の抽出器を指摘（例：gallery_dl/extractor/nhentai.py、exhentai.py、hitomi.py、hentaifoundry.py）。主張は「大量自動ダウンロードで海賊版インフラを助長／アクセス制御を回避している（§1201の回避）」。  
- 開発者の対応：作者はリポジトリ全履歴をgit-filter-repoで書き換えて該当ファイルを消すよう要求される一方で、履歴改変に抵抗しCodeberg/GitLabへミラーを作成。GitHub側の手続きや7日程度の対応期限が議論された。移行時の技術的課題（Codebergへの移行エラー）や、アーカイブ容量（リリース含まず約250MB、含めると6GB）も報告された。  
- コミュニティの助言：完全削除、対象ファイルのみ削除、反通知（counter-notice／法的リスクあり）、あるいはホスティング移行など複数の選択肢が提示され、どれも一長一短。DMCA §1201は「善意の信念」で成立し得るため、通知が必ずしも法的に正しいとは限らないが、プラットフォームは迅速対応を取る傾向にある。  
- 技術面ポイント：履歴改変には git-filter-repo 等のツールが使われるが、履歴を書き換えると既存ユーザーやPRに影響が出る。ミラーリングや完全アーカイブの作成は運用継続の実用的対策。

## 実践ポイント
- まずバックアップ：issues/PR/discussionsを含む完全アーカイブを定期的に保存する。  
- ミラーを用意：GitLab/Codeberg等、複数のホスティングにミラーを置く（CIやissue運用方針も検討）。  
- 最小限の対応案を検討：法的リスクを理解した上で「問題のファイルだけ隔離する」「該当抽出器を別リポジトリに分離する」など段階的対応を検討。  
- 法的助言を仰ぐ：反通知や対応方針は国・状況で異なるため、必要なら弁護士や対応窓口（例：EFFのような支援団体）に相談する。  
- 開発ポリシー整備：スクレイピングやダウンロード機能の扱い、貢献者への注意喚起、利用規約遵守をREADMEやCONTRIBUTINGに明記する。

短く言うと：オープンソースの「便利さ」と「法的リスク」は隣り合わせ。リポジトリ運用では技術的バックアップと法的な備えの両方が必要だ。
