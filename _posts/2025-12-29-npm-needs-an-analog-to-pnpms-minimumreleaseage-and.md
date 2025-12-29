---
layout: post
title: npm needs an analog to pnpm's minimumReleaseAge and yarn's npmMinimalAgeGate
date: 2025-12-29 01:48:49.689000+00:00
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: https://www.pcloadletter.dev/blog/npm-min-release-age/
source_title: npm needs an analog to pnpm's minimumReleaseAge and yarn's npmMinimalAgeGate
source_id: 436966445
excerpt: npmにも年齢ゲート導入を提案、公開直後の攻撃をCIで防ぐ方法
---
# npmにも欲しい「公開後の猶予」でサプライチェーンを守る — 新着パッケージに年齢ゲートを掛ける意味

## 要約
pnpmのminimumReleaseAgeやyarnのnpmMinimalAgeGateは、新しく公開されたパッケージの即時導入を防ぎ、npmエコシステムに増えるサプライチェーン攻撃への対抗手段を提供する。npm本体には同等の柔軟な仕組みが未だ整っておらず、企業／チーム単位での対策が求められている。

## この記事を読むべき理由
日本の開発現場でもnpmを中心に大量のOSS依存が使われており、急ぎで公開されたマルウェア混入や乗っ取りを防ぐ実践的な手法を知ることは、プロダクト安全性と運用の安定性に直結するため必読。

## 詳細解説
- 「年齢ゲート」とは何か  
  公開されてから一定時間（例：3日）経過していないパッケージをインストール対象から除外する仕組み。攻撃者が短時間で悪意あるバージョンをばらまくケースを想定し、時間差で検知されることに期待する防御策。

- pnpm / yarn の実装例  
  pnpmは minutes 単位で設定、yarnは期間表記をサポートし、どちらもパッケージ別のallowlist（信頼バイパス）を持てる点がポイント。
  
  ```json
  // pnpmの例 (.npmrcやpnpm-workspace.yamlではなく概念)
  {
    "minimumReleaseAge": 1440 // 分（=3日）
  }
  ```
  ```json
  // yarnの例 (設定例)
  {
    "npmMinimalAgeGate": "3d"
  }
  ```

- npmの現状と問題点  
  npmには--beforeフラグ（例: npm install --before=3d／npmrcのbefore=3d）で相対日付を扱う方法があるが、現状は以下の点で不十分：
  - allowlist（信頼済みパッケージの例外化）が標準で用意されていない  
  - ドキュメント上でセキュリティ対策として明確に扱われていない  
  - 組織ごとの内部依存（社内パッケージ）を便利に運用するためのエスケープハッチがない  
  これらは実務での採用障壁となる。

- なぜ「年齢」が効くのか  
  人気パッケージは多くの目に触れるため、攻撃は比較的早く発見される。新着バージョンを即時受け入れないことで「検出される時間」を担保し、被害範囲を小さくできる。

## 実践ポイント
- まず使える環境ならpnpmやyarnで年齢ゲートを有効化する（社内標準ツールの見直しを検討）。
- npmを使い続ける場合の暫定対応：
  - CIでnpm install --before=3d相当を組み込む（またはnpmrcに設定）して「自動化された検査時間」を確保する。
  - 内部パッケージは社内レジストリ（Verdaccio、Artifactory等）で配信し、信頼済みのみ即時許可する。
- 依存管理運用の強化：
  - 重要パッケージはバージョン固定（厳密なpin）＋依存性差分レビューをルール化する。
  - 署名/検証やSCAツール（Snyk等）で公開直後の変化を監視する。
- 組織提案ポイント：npmに相当機能（設定・allowlist・公式ドキュメントのセキュリティ用途明記）を要望として上げることで、より実務に即した改善を促す。

短時間の運用ルール変更とCI組み込みだけで、サプライチェーンリスクを大幅に下げられる。まずはツール選定とCIポリシーの見直しから始めよう。
