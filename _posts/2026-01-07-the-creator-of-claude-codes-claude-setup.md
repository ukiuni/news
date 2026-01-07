---
  layout: post
  title: "The creator of Claude Code's Claude setup - Claude Codeの作者によるClaudeのセットアップ"
  date: 2026-01-07T04:48:27.688Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://twitter.com/bcherny/status/2007179832300581177"
  source_title: "The creator of Claude Code's Claude setup"
  source_id: 46470017
  excerpt: "たった一枚の「JavaScript無効」画面が暴く、Web設計の落とし穴と即効対策"
  ---

# The creator of Claude Code's Claude setup - Claude Codeの作者によるClaudeのセットアップ
JavaScriptが無効でも"止まらない"作りを考える — たった一枚のエラーメッセージが突きつける設計の本質

## 要約
あるツイートのスクリーンショットに表示された「JavaScriptが無効です／プライバシー拡張が原因かも」というメッセージは、モダンWebアプリがJS依存で破綻する実例を示している。開発者はこの問題をテスト設計・フォールバック設計の観点で見直すべきだ。

## この記事を読むべき理由
日本のサービスでも、企業のセキュリティ設定や広告ブロッカー、古いブラウザ環境、端末の設定によりJavaScriptや一部の外部スクリプトが無効化される事例は少なくない。ユーザーを失わないための実装指針が得られる。

## 詳細解説
ツイートに表示されている文面は典型的なブラウザ側の警告とヘルプ案内（"JavaScript is not available"、"Some privacy related extensions may cause issues"）。技術的に注目すべきポイントは次の通りです。

- JS必須設計の落とし穴:
  - SPAやクライアント側で完全レンダリング・ルーティングを行う設計は、JSが無効だと空白ページやエラー表示になる。
  - ハイドレーションの失敗や依存ライブラリのブロック（CDN経由のスクリプトがブロックされる）も同様の障害を招く。

- 対策パターン:
  - Progressive Enhancement / Graceful Degradation: 基本コンテンツはサーバサイドで提供し、JSは機能拡張に留める。
  - SSR（サーバサイドレンダリング）＋クライアントハイドレーション：初回描画をSSRで行い、JS有効時にインタラクティブ化することでUXと耐障害性を両立。
  - <noscript>や静的HTMLの用意：JS無効時に意味のある案内や最小限の操作を提供する。
  - Feature detection とフォールバック：APIや機能がなければ代替ルートを用意する。

- 運用・テスト面:
  - 自動テストで「JS無効」ケースを含める。ヘッドレスブラウザでJSを切って挙動を確認する。
  - プライバシー拡張やセキュリティプロキシ下での振る舞いをモニタリングし、適切なエラーガイドを表示する（拡張の無効化を促すなど）。
  - 監視ログにブラウザのコンソールエラーやリソースのブロック情報を収集し、問題の根本原因を特定する。

## 実践ポイント
- テスト：PuppeteerでJSを無効化してレンダリング確認
```javascript
// JavaScript
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setJavaScriptEnabled(false);
  await page.goto('https://example.com', { waitUntil: 'networkidle2' });
  console.log(await page.content());
  await browser.close();
})();
```

- 実装の優先順位（短期→中期）:
  1. 重要ページに <noscript> を入れて、利用方法や代替リンクを表示する。
  2. 主要な公開ページをSSR化／静的プレレンダリングする（SEO向上にも寄与）。
  3. 自動テストに「JS無効」「広告ブロッカーあり」のケースを追加する。
  4. エラーメッセージは具体的に：何を無効にしたら直るかをユーザーに示す（例：「ブラウザの広告ブロック拡張を一時的に無効化してください」）。

- 日本市場への注意点:
  - 企業ネットワークや携帯キャリアのプロキシでスクリプトが差し替えられるケースがあり、特にB2Bや組織内ユーザーを想定するサービスでは耐障害性が重要。
  - プライバシー志向の高まりで、最小限のトラッキング設計と「機能しないときの案内」を用意することが信頼につながる。

短いエラーメッセージ一つでも、設計の甘さや運用上の抜け道が露わになる。現代のWeb開発では「JSがある前提」だけでなく「JSがない状況でも成り立つこと」を検証する習慣を持とう。
