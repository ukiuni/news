---
layout: post
title: "Manyana: A Coherent Vision For The Future Of Version Control - Manyana：バージョン管理の未来像"
date: 2026-03-22T15:44:21.409Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://bramcohen.com/p/manyana"
source_title: "Manyana - by Bram Cohen - Bram’s Thoughts"
source_id: 1514869235
excerpt: "ManyanaはCRDTでマージ失敗を無くし、近接編集をわかりやすく衝突提示するVCS案"
image: "https://substackcdn.com/image/fetch/$s_!93xj!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fbramcohen.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D-1733548744%26version%3D9"
---

# Manyana: A Coherent Vision For The Future Of Version Control - Manyana：バージョン管理の未来像
驚くほど実用的な“衝突しない”バージョン管理の提案 — Manyanaで見るCRDTの現実解

## 要約
Bram Cohenが公開したManyanaは、CRDT（Conflict-Free Replicated Data Types）を用いて「マージは常に成功するが、編集が近接すると分かりやすく衝突を提示する」UXを実現したプロトタイプで、従来のVCSが抱える再現性・マージ地獄を別の角度から解くものです。

## この記事を読むべき理由
日本でも分散開発、モノレポ、大規模レビューや頻繁なリベースでマージ疲れが問題化しています。Manyanaは「マージ失敗をなくしつつ、分かりやすい衝突表示」で日常の開発負荷を下げる可能性を示しています。今後のVCSやエディタ連携の方向性を先取りできます。

## 詳細解説
- 基本アイデア：CRDTをファイル単位（行単位の「織り込み＝weave」）で使い、状態は「ファイルに存在したすべての行」とその追加・削除メタデータとして保持。従来の3-wayマージのように共通祖先を探す必要がない。
- マージの性質：CRDTは順序に一貫性を持たせるため、複数ブランチが同じ位置に挿入しても一度決まった行順は変わらない（恒久的順序）。その結果、複雑なマージトポロジでも結果が決定的。
- 衝突UXの工夫：CRDT自体は「失敗しない」ため従来の「競合＝マージ失敗」は起きない。Manyanaは「編集が近接した箇所」を衝突としてフラグし、誰が何を追加／削除したかを示す構造化された衝突表示を行う（例：削除された範囲／追加された範囲を明示）。これにより、単純な左右差分よりも意味のある解決が可能になる。
- リベース問題の解消：従来のrebaseは履歴を書き換えるために「履歴の破壊」を招くが、CRDTでは「プライマリ祖先」注釈を付けることで、コミットを再適用しつつ完全な履歴を保持できる。DAGだけで履歴を再構築する必要が薄れる。
- Manyanaの現状：470行ほどのPythonデモで、個別ファイル上の概念実証。チェリーピックやローカルundoは未実装だが設計思想とREADMEで拡張案を提示。コードはパブリックドメイン。

## 実践ポイント
- デモを触る：Manyanaのリポジトリ（README含む）を読んで、実際にファイルでどう衝突が見えるか確認する。概念が直感的に理解できる。
- 小さな実験を組織で：モノレポや頻繁なリベースで問題が出ているチームは、ファイル単位のCRDTワークフローをプロトタイプ導入して運用コストを比較してみる。
- エディタ／レビュー連携を考える：衝突が「誰が何をしたか」を示す形式なら、コードレビューUIやIDEの自動案内がやりやすくなる。VSCode拡張や差分ビューの改善案を検討する価値あり。
- 長期設計に反映：VCSの将来設計や社内ツール選定で「マージは失敗しないが有益に衝突を提示する」アプローチを候補に入れる。

--- 
原著はBram Cohen氏のManyana（READMEと実装は公開）に基づく要約・解説です。
