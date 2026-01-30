---
layout: post
title: "Beta testing of WebUSBUnpinner - WebUSBUnpinnerのベータテスト：プラットフォームワーカーのプライバシーと権利侵害を調査するツール"
date: 2026-01-30T00:51:45.836Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://reversing.works/posts/2026/01/help-reversing.works-empower-workers-by-testing-our-tool/"
source_title: "Help Reversing.works empower workers by testing our tool :: Reversing.Works"
source_id: 1435197779
excerpt: "スマホで職場監視を暴き出すWebUSB Unpinnerのベータ参加募集中"
image: "https://reversing.works/"
---

# Beta testing of WebUSBUnpinner - WebUSBUnpinnerのベータテスト：プラットフォームワーカーのプライバシーと権利侵害を調査するツール
あなたのスマホで職場監視を暴く — 誰でも参加できるWebUSB Unpinnerベータ募集

## 要約
Reversing.worksが、職場アプリとサーバー間の通信を調査するためのツール「WebUSB Unpinner」の初回ベータ参加者を募集中。技術的にはAndroid端末とCLI知識で、アプリの通信可視化やTLSピンニング対策の検証を支援することが目的。

## この記事を読むべき理由
職場でのアプリ監視や労働者のプライバシー侵害は世界共通の課題で、日本でもフードデリバリーや派遣／プラットフォーム労働の増加で身近になっています。技術的ツールのベータに参加することで、問題の可視化や改善に貢献できます。

## 詳細解説
- 目的：WebUSB Unpinnerは、従業員が使う業務アプリと雇用側サーバー間の通信を観察できるようにして、監視や権利侵害の証拠収集を支援するツールです。  
- 技術的ポイント（高レベル）：
  - Android端末を使い、端末とPC間の通信経路をローカルで中継・解析する仕組みを提供します。
  - 多くのモバイルアプリはTLSピンニング等の保護を行っており、単純なプロキシだけでは通信が見えないことがあります。Unpinnerはそうした保護を回避・検証するための補助を行い、解析を容易にします（注：法的／倫理的な許可がある場合に限定）。
  - 完全自動ではなく、複雑な商用アプリや先進的な防御を使うアプリでは失敗することがあり、その報告がツール改善に重要です。

## 実践ポイント
- 要件：Android端末、コマンドラインの基本知識。
- 参加方法：公式ドキュメントに従ってインストール・実行し、動作ログや失敗事例をリポジトリのIssueに報告する。staff@reversing.works に連絡してワークショップ支援を依頼可能。
- テストの進め方（安全に）：自分が許可を持つアプリ・アカウントでのみ実施し、会社規約や法令に抵触しないよう注意する。結果は具体的な挙動（成功/失敗）とログを添えて共有すると開発側の改善に役立ちます。
- 波及効果：同僚やコミュニティでワークショップを開いて多様な端末・アプリでの挙動を集めると、ツール成熟に貢献できます。
