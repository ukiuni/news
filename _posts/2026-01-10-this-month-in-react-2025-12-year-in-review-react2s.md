---
layout: post
title: "This Month in React 2025-12: Year in review, React2Shell (RCE, DOS, SCE, oh my) - 2025年12月のReact：年次総括、React2Shell（RCE、DOS、SCE…）"
date: 2026-01-10T17:49:29.261Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.reactiflux.com/transcripts/tmir-2025-12"
source_title: "TMiR 2025-12: Year in review, React2Shell (RCE, DOS, SCE, oh my)"
source_id: 467452091
excerpt: "React2Shellで露呈したRCE/DOS/SCE脆弱性と2025年のReact潮流を詳報"
image: "https://reactiflux.com/logo-banner.png"
---

# This Month in React 2025-12: Year in review, React2Shell (RCE, DOS, SCE, oh my) - 2025年12月のReact：年次総括、React2Shell（RCE、DOS、SCE…）
React2Shell事件と2025年のReactエコシステム総まとめ — 日本の開発現場が今すぐ確認すべきポイント

## 要約
Reactコミュニティの2025年総括。特に「React2Shell」と呼ばれる脆弱性（Promiseのデシリアライズ＋new Functionによる評価でRCE/DOS/ソース流出）を中心に、React/React Nativeの主要リリースとエコシステムの出来事を振り返る。

## この記事を読むべき理由
サーバーコンポーネント（RSC）やReactコンパイラの普及で、クライアント・サーバー間の境界が変化している。日本のウェブ/モバイルサービス運用者は、依存関係の供給網やシリアライズ処理、安全なアップデート運用を見直す必要がある。

## 詳細解説
- React2Shell脆弱性（RCE / DOS / SCE）
  - 本質：特別に細工されたPromiseのデシリアライズ処理と、new Function（動的評価）を組み合わせたペイロードにより、リモート実行（RCE）、サービス拒否（DOS）、ソースコード漏洩（SCE）が発生。
  - 影響範囲：サーバーサイドで未検証のデシリアライズや、外部コードを評価する仕組みを使うRSCやツールチェーン。クラウドプロバイダ（Cloudflare）での検出や実際のサービス障害報告もあり、攻撃は実践的だった。
  - 対応：緊急PRでPromiseサイクルやfunction.toString周りのガードが導入。コミュニケーションや脆弱性公開のタイミングについては批判も出た。
  - 技術的示唆：Promiseを含むオブジェクトの信頼できないデシリアライズ、動的関数生成は最小化／禁止する。サーバ側で入力サニタイズと実行コンテキストの制限が必須。

- React / RSC の動向
  - React 19 系の継続的な機能投入（19.2でActivityやuseEffectEvent等）、React Compiler 1.0リリースや「Async React」関連研究が進展。
  - サーバーコンポーネント（RSC）は導入が加速。React Routerや主要ライブラリがRSC対応を進め、Instant-loadingを謳う実装例も登場。
  - 研究トピック：View Transitionsの実験的最適化、Concurrent Stores、そして「throw a promise」パターンの扱い見直し。

- React Native の年次総括
  - リリース群（0.78〜0.83）での重要点：旧アーキテクチャの凍結、新アーキテクチャへの移行、JSCのコミュニティパッケージ化、Android 16対応、Expo/EASのホスティング強化。
  - 0.83は破壊的変更なしでのリリースとなり、開発体験向上を重視。新しい開発者向けツール（DevTools）やパフォーマンス計測機能が充実。

- エコシステム雑感
  - CRA（Create React App）事実上の後退でViteなどの軽量ビルドが推奨に。Styled Componentsのメンテ状況に関する警鐘。
  - 供給網問題：npmトークンの無効化、パッケージ侵害の継続的リスク、GitHub Actionsの価格議論、そしてツール買収（例：Bunの買収報道）などが注目を浴びた。
  - セキュリティ研究：SVGフィルタを悪用したクリックジャッキングのような新手法、AIコーディングエージェントによる依存注入リスクの報告など。

## 日本市場との関連
- 多くの国内サービス（ウェブのフロントエンド、モバイルアプリ、サーバーサイドレンダリングを行うSaaS）がReact/React Nativeを採用しているため、今回のようなシリアライズ・実行系の脆弱性は直接的なリスクとなる。
- 日本の受託開発やレガシーシステム移行案件では、CRA→Vite移行やReact Compiler導入の判断、React Nativeのアーキテクチャ移行計画を早めに検討する価値がある。
- 法規制やエンタープライズ要件（ログ保存、監査、脆弱性対応体制）の観点から、公開脆弱性対応フローと依存管理の強化は重要度が高い。

## 実践ポイント
- デシリアライズの防御
  - 信頼できない入力は絶対にeval/new Functionで評価しない。可能なら安全なシリアライザ（型付け・スキーマ検証）を導入。
- 依存関係とパッケージ供給網
  - 重要ライブラリはバージョン固定と署名検証、脆弱性アラート（Dependabot等）を常時有効化。npmトークンを定期的にローテーション。
- CI/CD と監査
  - ステージング環境での包括的E2Eとファジング、SAST/DAST導入。Cloudflare等CDNのログとWAFルールを監視。
- React / RSC の採用判断
  - RSC導入前にサーバ側の実行境界とシリアライズ戦略を設計。RSCは性能改善の一方で攻撃面が変わるため、セキュリティレビューを必須化。
- React Native アップグレード
  - 破壊的変更がないリリースでも、カナリア環境で動作確認を行い、DevToolsでパフォーマンスを計測。
- 開発者教育
  - チームで「危険なAPI（eval/new Function）」と「安全な非同期デシリアライズ」についてナレッジを共有。

短くまとめると、2025年の大きな教訓は「利便性の高い新機能や高速化の波の裏に、新たな攻撃面が生まれる」という点。ツールは進化しているが、設計と運用の基本（入力検証・依存管理・継続的監視）を手を抜かないことが、結果的に安全で高速なプロダクトにつながる。
