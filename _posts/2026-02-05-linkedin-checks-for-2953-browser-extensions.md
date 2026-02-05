---
layout: post
title: "LinkedIn checks for 2953 browser extensions - LinkedInが2953のブラウザ拡張機能をチェックしている件"
date: 2026-02-05T20:28:25.608Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mdp/linkedin-extension-fingerprinting"
source_title: "GitHub - mdp/linkedin-extension-fingerprinting"
source_id: 46904361
excerpt: "LinkedInが2953の拡張を識別、プライバシーと採用でリスク"
image: "https://opengraph.githubassets.com/abfe76a947e011b3dc26872639e1e0dc746adab175917a97ddb365381cc4b0e7/mdp/linkedin-extension-fingerprinting"
---

# LinkedIn checks for 2953 browser extensions - LinkedInが2953のブラウザ拡張機能をチェックしている件
クリックせずにはいられないタイトル: LinkedInはあなたの拡張機能を“名簿”で照合している — 何がわかる？どう守る？

## 要約
GitHub上の調査で、LinkedInがページ読み込みごとに2,953個のChrome拡張機能を密かにチェックしていることが確認された。拡張機能IDリストと検出ツールが公開されている。

## この記事を読むべき理由
LinkedInはプロ向け情報を扱うため日本のビジネスパーソンや採用担当者にも広く使われており、拡張機能の検出はプライバシーやターゲティング、企業のセキュリティ方針に直結します。初心者でも影響と対策が分かります。

## 詳細解説
- 発見内容：調査リポジトリ（mdp/linkedin-extension-fingerprinting）は、LinkedInのページスクリプト（fingerprint.js）から抽出した拡張機能ID一覧（chrome_extension_ids.txt）を公開。合計2,953件をリスト化している。
- データの内訳：リポジトリ内のcsv（chrome_extensions_with_names_all.csv）には拡張機能ID、名前、Chrome Web Storeリンクが対応づけられており、約78%はChrome Web Storeで確認、約22%はExtpose（削除済みなどのフォールバック）で確認されている。
- ツール：fetch_extension_names.js が拡張機能IDからストア名を取得する仕組みを提供（Node.jsで実行）。テスト用スクリプトやサブセット取得オプションもある。
  - 実行例：
```bash
# 全件取得（Rate limitに注意）
node fetch_extension_names.js

# 一部取得（オフセット／リミット指定）
node fetch_extension_names.js --offset 0 --limit 500
```
- 技術的意味：LinkedInはページ内でインジェクト可能なオブジェクトや既知の拡張機能が注入する特有のグローバル変数などを検出し、ブラウザにどの拡張が入っているか「指紋」を取れる。拡張機能の有無はユーザーのブラウザ状態や行動パターンのプロファイリングに使える。
- リスク：拡張名の組み合わせから個人を特定（追跡）したり、広告や採用のターゲティング、あるいは企業内ポリシー違反の検出に利用され得る。

## 実践ポイント
- 自分の拡張を把握する：Chromeで chrome://extensions を開き、不要な拡張は無効化または削除する。
- スクリプトを確認する：devtoolsのNetwork/Sourceでfingerprint.jsや外部スクリプトを確認し、不審な挙動を監査する。
- 実行して一覧を確認する（Node.jsが必要）：
```bash
git clone https://github.com/mdp/linkedin-extension-fingerprinting.git
cd linkedin-extension-fingerprinting
node fetch_extension_names.js --limit 100
```
- プライバシー対策：広告ブロッカーやスクリプトブロッカー（例：uBlock Origin, uMatrix相当）を導入する、ブラウザプロファイルを分離する、企業ならグループポリシーで拡張管理を行う。
- 組織向け：社内のエンドポイントで拡張管理・監査ポリシーを整備し、業務端末での余計な拡張インストールを制限する。

短く言えば、LinkedInは“拡張機能名簿”でブラウザ状態を照合しているため、個人と企業の両方で拡張機能の管理とスクリプト監査が重要です。
