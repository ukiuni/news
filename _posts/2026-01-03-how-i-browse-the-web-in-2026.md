---
  layout: post
  title: "How I browse the web in 2026 - 2026年の私のウェブの巡り方"
  date: 2026-01-03T21:05:53.879Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://bastiangruber.ca/posts/how-i-browse-the-web-in-2026/"
  source_title: "How I browse the web in 2026"
  source_id: 1404368876
  excerpt: "端末分離とFirefox拡張、セルフホストRSSで個人情報を守る実践ブラウジング術"
  image: "https://bastiangruber.ca/images/default-social-image.png"
---

# How I browse the web in 2026 - 2026年の私のウェブの巡り方
クリックせずにはいられないタイトル案: 「Apple依存から脱出した開発者の2026年ブラウジング術 — プライバシー重視で作業効率を保つ実践セットアップ」

## 要約
著者は仕事と私生活を完全に分離し、Firefox中心・拡張でプライバシーを強化、RSSや自己ホスティングで情報摂取を最適化している。2026年の“現場で使える”ブラウジング習慣を短くまとめるとこれだけで十分だ。

## この記事を読むべき理由
日本ではApple中心のワークフローが根強く、個人データや仕事用アプリの境界管理が課題になりがち。この記事は、実務者が実際に採用している「デバイス分離」「履歴無効化」「拡張＋自己ホスティング」を具体例とともに示しており、すぐ試せるヒントが多い。

## 詳細解説
- ハードウェアとOS:
  - 仕事用にMacBook Pro（M3 Pro）、私用にFramework（AMD 13" + Arch + COSMIC）を採用。モバイルは仕事用アプリを完全に削除し、将来的にGrapheneOS系のネイティブAndroidを検討。
  - ポイント: デバイス単位でログインやアプリを分離することで、個人データと会社資産の混在を防ぐ。

- ブラウザとクライアント:
  - 全端末でFirefoxをメインにし、ラップトップではThunderbird、職場端末ではブラウザ経由でGmail、iPhoneはデフォルトのメール。Firefox Syncで設定・拡張を同期。
  - ポイント: クロスプラットフォームで一貫したプライバシー構成を持てる。

- 拡張機能（抜粋）:
  - uBlock Origin, Privacy Badger, SponsorBlock, AdBlocker for YouTube, Bypass Paywalls, ClearURLs 等を活用。YouTube履歴を無効化して推薦アルゴリズムの影響を回避。
  - ポイント: 広告・追跡・推薦バイアスを削ぎ落とすことで「意図的な情報摂取」が可能に。

- サービスとワークフロー:
  - TickTick（ToDo）、YNAB（家計）、Excalidraw（図）、Miniflux（セルフホストRSS）、WakingUp（瞑想）、GitHub（コード）。記事はAre.naへ保存し、RSSで定期チェック。読書習慣はTickTickでリマインド。
  - ポイント: 情報の取り込み→保存→後で読むを明確に分け、ブラウザを「探索」用に使いすぎない運用。

- 情報源の使い分け:
  - Hacker NewsやLobstersは業界俯瞰用、YouTubeはチュートリアルや音楽用で履歴オフ、PinboardやAre.naで保存。RSSは「クリーンな直接接触」を提供。
  - ポイント: 推薦フィードに頼らず、自分でハブを作る。

## 実践ポイント
- 今すぐ試せる5つ:
  1. 仕事と私用のログインを端末レベルで分離する（最初はブラウザのプロファイルだけでも効果あり）。
  2. ブラウザ履歴をオフにしてYouTubeの自動推薦を切る。SponsorBlock等で広告やスポンサーを自動スキップ。
  3. uBlock Origin + Privacy Badger を入れてトラッキングと広告を減らす。
  4. RSSを一つセルフホスト（Minifluxなど）か専用リーダーで集約し、毎日短時間だけチェックする習慣を作る。
  5. 記事保存→TickTickで「毎日2記事読む」などの小さなリマインドを入れて「保存したまま積読」化を防ぐ。

短く言うと：ツールよりルールを先に決め、プライバシー拡張＋軽い自己ホスティングで情報摂取を意図的にコントロールすると、日本の多忙な開発者にも効果が高い。
