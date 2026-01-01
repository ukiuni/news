---
  layout: post
  title: "A website to destroy all websites - すべてのウェブサイトを終わらせるウェブサイト"
  date: 2026-01-01T21:55:18.084Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://henry.codes/writing/a-website-to-destroy-all-websites/"
  source_title: "A Website To End All Websites | Henry From Online"
  source_id: 46457784
  excerpt: "静的HTMLとRSS、分散プロトコルで個人のウェブ主権を取り戻す具体策を紹介。"
  image: "https://henry.codes/img/og/og-a-website-to-destroy-all-websites.png"
---

# A website to destroy all websites - すべてのウェブサイトを終わらせるウェブサイト
巨大プラットフォームに抵抗する「小さなWeb」──ネットの主権を個人で取り戻す方法

## 要約
Henryの論考は、インターネットの「工業化」と注意経済が個人の創作・学び・コミュニティを蝕んだとし、HTML/RSSや分散プロトコルなどの「小さなWeb」手法でウェブの主権を取り戻そうと呼びかける。

## この記事を読むべき理由
日本ではLINEや巨大プラットフォームの依存が高く、クリエイターや学習者がプラットフォームの仕様変更で翻弄されやすい。個人で情報の所有権や表現の自由を守る方法を知ることは、仕事や趣味、企業のDX戦略にも直結する。

## 詳細解説
- 問題の構図：著者は自動車の普及に伴う「社会が道具に合わせて変わる」現象を引用し、インターネットが当初の「相互運用性・所有」の理想から広告・アルゴリズムによる注意搾取へと変質した点を批判する。Ivan Illichの「Tools for Conviviality」と「radical monopoly（技術の根本的独占）」の視点が軸。
- 注意経済と中央集権：YouTube/TikTok/大手SNSのアルゴリズムは「露出」と「フック」を最適化するため、コンテンツの質よりもフォーマットやスケールを生む方向に設計される。結果、学びの場やコミュニティが単一のプレイヤーに依存するリスクが高まる。
- 技術的な代替案（主要ポイント）：
  - 所有できるコンテンツ基盤：静的HTMLとRSSで「自分のコンテンツ」を持つ。RSSは長年の実績があり、撤退リスクが低い。
  - 相互運用プロトコル：ActivityPub（Mastodonなど）やATProto（Bluesky）のような分散プロトコルは、プラットフォーム移行のリスクを下げ、異なるネットワーク間の連携を可能にする。
  - POSSE（Publish On Your Own Site, Syndicate Elsewhere）：まず自分のサイトに投稿してから外部に配信する運用で所有権を担保する。
  - マイクロフォーマットとWebmentions：検索や人同士のつながりをHTMLレベルで保持し、外部のサービスと相互作用できる仕組み。
  - ウェブ開発の回復：SPA一辺倒ではなく、HTML/CSSのprogressive enhancementやモダンなブラウザAPIで表現の幅とパフォーマンスを取り戻す。静的サイトジェネレータや軽量なJS採用が推奨される。
- なぜ今なのか（日本向け含意）：日本のクリエイターや中小企業はプラットフォーム依存で収益・顧客接点が不安定になりやすい。個人ドメインや分散プロトコルを早めに採り入れることでリスク分散と長期的なブランド資産化が可能となる。

## 実践ポイント
- 今週できること
  - 自分のドメインを取得し、静的サイトジェネレータ（Hugo / Eleventy / Jekyll）で個人サイトを立ち上げる。
  - RSSフィードを有効化し、既存のSNS投稿をPOSSEで自サイト発信→外部配信に切り替える。
- 中期の改善
  - microformats（h-card, h-entry）をページに組み込み、Webmentionを有効化して外部の反応を自サイトに取り込む。
  - Mastodonやインスタンスを選び、ActivityPub経由で分散SNSと連携する。Bluesky（ATProto）もウォッチする。
- 技術スタックと運用のヒント
  - ホスティングはGitHub Pages/Netlify/Cloudflare Pagesで低コスト運用。CIで自動デプロイ。
  - フロントはまずHTML+CSSで作り、必要最小限のJSを追加する「progressive enhancement」を心がける。VS Codeでソース管理・ローカルプレビューを活用。
  - コンテンツ戦略は「所有→配信→刺さるフォーマット」に。長尺の良質記事は検索・保存されやすく、短期のバズ依存を減らす。
- 組織的な一歩
  - 企業ではブランドサイトのCMS設計に「エクスポート可能」「APIロックイン回避」を要件に加える。クリエイター支援なら収益分配の透明性とコンテンツ所有の確保を優先する。

## 引用元
- タイトル: A website to destroy all websites
- URL: https://henry.codes/writing/a-website-to-destroy-all-websites/
