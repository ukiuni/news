---
layout: post
title: "CVEs Affecting the Svelte Ecosystem - Svelteエコシステムに影響するCVE"
date: 2026-01-15T19:14:53.527Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://svelte.dev/blog/cves-affecting-the-svelte-ecosystem"
source_title: "CVEs affecting the Svelte ecosystem"
source_id: 46636387
excerpt: "Svelteエコシステムの5つの重大脆弱性と即時更新・設定対策を紹介"
image: "https://svelte.dev/blog/cves-affecting-the-svelte-ecosystem/card.png"
---

# CVEs Affecting the Svelte Ecosystem - Svelteエコシステムに影響するCVE
魅力的なタイトル: Svelteユーザー必読：今すぐアップデートすべき脆弱性5件と現場での対処ポイント

## 要約
Svelte関連パッケージで5件の重大な脆弱性（DoS、メモリ増幅、XSS、SSRFなど）が報告され、既に修正版が公開されています。該当バージョンを使っている場合は速やかなアップグレードと設定確認が必要です。

## この記事を読むべき理由
- Svelte/SvelteKitは日本でも採用が増えており、知らずに脆弱版を動かすとサービス停止や情報漏えいのリスクがあります。
- 脆弱性は「リモート関数」「プリレンダリング」「hydratableのキー」など機能依存で影響範囲が変わるため、単にライブラリを更新するだけでなく導入方法の見直しが重要です。

## 詳細解説
以下は主要ポイントの分かりやすい解説です。

- 修正版と対象パッケージ
  - devalue → 5.6.2
  - svelte → 5.46.4
  - @sveltejs/kit → 2.49.5
  - @sveltejs/adapter-node → 5.5.1
  - 依存関係（devalue）を使うsvelte / @sveltejs/kitは、patched版に依存更新が含まれています。

- CVEの概要（影響と条件）
  - CVE-2026-22775 / CVE-2026-22774（devalue）
    - 問題: devalue.parseでユーザー制御の入力をパースすると、大量メモリ割当て／CPU消費を引き起こす可能性（DoS）。
    - 影響条件: devalue 5.1.0〜5.6.1 や 5.3.0〜5.6.1 を使用し、ユーザー入力をparseする場合。SvelteKitの「リモート関数」を使うと影響。
  - CVE-2026-22803（@sveltejs/kit）
    - 問題: Remote Functionsのバイナリ形式デシリアライズでメモリ増幅DoS。
    - 影響条件: SvelteKit 2.49.0〜2.49.4 で experimental.remoteFunctions を有効にし、formを使用している場合。
  - CVE-2025-67647（@sveltejs/kit, @sveltejs/adapter-node）
    - 問題: プリレンダリング関連でDoSおよび設定次第でSSRF。条件が整うとCDNキャッシュを悪用した二次的なXSS（SXSS）も発生し得る。
    - 影響条件: @sveltejs/kit 2.44.0〜2.49.4 でプリレンダードルートがある場合。さらに @sveltejs/adapter-node を使い ORIGIN 環境変数が未設定で、ホストヘッダ検証を行わないリバースプロキシ環境だとSSRFリスクがある。
  - CVE-2025-15265（svelte）
    - 問題: hydratable に渡すキーが未サニタイズのユーザー制御文字列だと XSS を引き起こす可能性。
    - 影響条件: svelte 5.46.0〜5.46.3 で hydratable を使い、外部入力をキーに使用している場合。

- 背景と対応の意義
  - 近時、Web開発ツール群で高プロファイルの脆弱性が続いたため、コミュニティでの責任ある開示と短期のパッチ適用が活発化しています。Svelteチームも改善プロセスを強化する予定です。

## 実践ポイント
すぐに取れる対策を簡潔にまとめます。

- まずはアップデート（最優先）
  - package.json / lockfile を更新して以下へアップデート：
    - devalue → 5.6.2
    - svelte → 5.46.4
    - @sveltejs/kit → 2.49.5
    - @sveltejs/adapter-node → 5.5.1
  - CIで依存解決後のビルド・テストを自動実行すること。

- 設定と機能の見直し
  - SvelteKitのexperimental.remoteFunctionsを使っているプロジェクトは、入力パース経路を点検し、不要なら無効化。
  - プリレンダリングを使っている場合は ORIGIN 環境変数を明示的に設定するか、確実に Host ヘッダ検証を行うリバースプロキシを置く。
  - hydratable に渡すキーは必ずサニタイズまたはエスケープ。ユーザーが制御する文字列をキーにしない。

- 開発／運用上のベストプラクティス
  - 依存性監視ツール（Dependabot、Renovate、npm audit 等）を導入して自動でPRを受け取る。
  - 本番前にメモリ・負荷テストを行い、異常な入力での挙動を確認する。
  - 脆弱性を発見したらリポジトリのSecurityタブ経由で責任ある報告を行う。

- 日本向けの注意点
  - 多くの日本企業ではオンプレやプライベートネットワークに内部ダッシュボードがあるため、SSRF が内部資源に与える影響が大きい点に留意してください。
  - 国内CDN／エッジキャッシュを利用する場合、キャッシュポリシーとヘッダ検証を厳格に設定しましょう。

以上を踏まえ、まずは該当パッケージのバージョン確認とアップデートを実施してください。ログやモニタリングで不審なメモリ増加やエラーを早期に検知する体制も併せて整えることをおすすめします。
