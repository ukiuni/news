---
layout: post
title: "A bug in Bun may have been the root cause of the Claude Code source code leak."
date: 2026-04-01T00:51:46.790Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/oven-sh/bun/issues/28001"
source_title: "Bun&#39;s frontend development server - Source map incorrectly served when in production · Issue #28001 · oven-sh/bun · GitHub"
source_id: 409377438
excerpt: "Bunのバグで本番にソースマップ公開、クロードコード流出の疑い"
image: "https://opengraph.githubassets.com/4beefbbf9e8914bf5baabb0cd1943733ee6cdccbb8e7b6a661429eaa198ee4ad/oven-sh/bun/issues/28001"
---

A bug in Bun may have been the root cause of the Claude Code source code leak - BunのバグがClaude Codeのソースコード流出の根本原因だった可能性

本番で勝手にソースマップを公開？Bunの誤挙動が招く“見えない”情報漏えいリスク

## 要約
Bun のフロントエンド開発サーバーが、本番モード設定でもソースマップを返してしまうバグが報告されており、これが機密ソースの流出につながった可能性が指摘されています。

## この記事を読むべき理由
Bun は高速な JavaScript/TypeScript ランタイムとして注目されており、日本でも採用が増えています。本番で不要なソースマップが公開されると、難読化されたはずのコードや内部実装、場合によっては機密情報が第三者に露出するリスクがあります。AIモデルや商用サービスを扱う開発者は必読です。

## 詳細解説
- 問題の概要  
  GitHub Issue #28001 によれば、次のような構成で Bun サーバーを本番モード（development: false）で起動しても、ソースマップ（*.js.map）が返されてしまう現象が再現されています。

- 再現例（簡略）
```javascript
// server.js
import homepage from './index.html'
Bun.serve({ routes: { '/': homepage }, development: false })
```
```html
<!-- index.html -->
<script type="module" src="script.js"></script>
```
```javascript
// script.js
function blah() { let something = 'yes'; console.log(something) }
```
サーバーにアクセスすると、minified な出力の末尾に `//# sourceMappingURL=/chunk-xxxx.js.map` が付与され、実際に .map ファイルが取得できるため、元の可読なソースが復元可能になります。

- なぜ危険か  
  ソースマップは元のソースコード（変数名やコメント含む）へのマッピングを提供するため、公開されると難読化やバンドルで隠したはずの実装やロジックが明らかになります。APIキーや内部専用のロジックがソース内に残っていれば、侵害につながる可能性があります。

- 影響と文脈  
  報告では「Claude Code のソースコード流出」に関連する可能性が示唆されています（確定的な因果は要調査）。いずれにせよ、ソースマップ公開は重大な情報漏洩経路になり得ます。

## 実践ポイント
- まずは Bun のバージョンを確認し、該当バグが修正された最新バージョンにアップデートする。  
- 本番ビルドでソースマップを生成しない設定を明示する（ビルドツール／バンドラの設定を確認）。  
- 出力ディレクトリに .map ファイルが含まれていないこと、HTTP でアクセスできないことを curl 等で検証する。例:
```bash
curl -I https://your-site.example.com/chunk-xxxx.js.map
```
- ビルド後に自動で sourceMappingURL コメントを削除するステップを導入する（CI/CD で検査）。  
- 万一公開してしまった場合は、該当ファイルを即座に削除してアクセスを遮断し、必要に応じて鍵やシークレットのローテーションを行う。  
- 日本の企業・チームは、依存ランタイムのセキュリティアップデートや公開アセットの定期監査を運用ルールに組み込むこと。

短く結論：Bun のような新興ランタイムは魅力的だが、本番環境での「出力確認」と「公開アセットの検査」は必須。ソースマップの扱いは軽視しないでください。
