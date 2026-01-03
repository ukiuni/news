---
  layout: post
  title: "X-Clacks-Overhead - X-Clacks-Overhead（X-クラックス・オーバーヘッド）"
  date: 2026-01-03T14:34:49.842Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://hleb.dev/post/x-clacks-overhead/"
  source_title: "X-Clacks-Overhead | hleb.dev"
  source_id: 46475437
  excerpt: "X-Clacks-OverheadでサイトにGNU Terry Pratchettを静かに流す方法"
  image: "https://hleb.dev/images/x-clacks-overhead/cover.jpg"
---

# X-Clacks-Overhead - X-Clacks-Overhead（X-クラックス・オーバーヘッド）
HTTPヘッダで追悼をささやく：サイトに「GNU Terry Pratchett」を流す小さな仕掛け

## 要約
Sir Terry Pratchettへの敬意を込め、HTTPレスポンスヘッダ「X-Clacks-Overhead: \"GNU Terry Pratchett\"」を静的サイトに追加する手法を紹介します。Cloudflare Pagesの_headersファイルを使えば簡単に実装できます。

## この記事を読むべき理由
技術的には無意味でも、ウェブに文化的なメッセージを忍ばせる実践はコミュニティやブランドの個性づくりに有効です。日本の開発者も同様の「小さな文化的ジェスチャー」をサービスに取り入れることで、ユーザーとの距離感やチームの文化を豊かにできます。

## 詳細解説
X-Clacks-Overheadヘッダは、Terry Pratchettの小説『Going Postal』に登場するClacks（通信網）を模したファンによる追悼の習慣です。ヘッダ値に "GNU Terry Pratchett" を入れておくことで、ネットワーク上のリクエスト/レスポンスを通じて名前を「流し続ける」象徴的な仕組みになります。機能的な効果やパフォーマンス改善は一切なく、完全にエモーショナルなメッセージです。

Cloudflare Pagesではルートに_plain_な _headers ファイルを置くことで任意のカスタムレスポンスヘッダを注入できます。シンプルな例は次の通りです。

```text
/*
  X-Clacks-Overhead: "GNU Terry Pratchett"
```

この指定はサイトのすべての静的アセットとHTMLレスポンスに対してヘッダを付与します。挙動を確認するにはブラウザのデベロッパーツールのNetworkタブでレスポンスヘッダを見たり、curlでヘッダだけ取得します。

```bash
curl -I https://hleb.dev
```

注意点としては、CDNや中間プロキシが独自のヘッダポリシーを持っている場合があること、未知のカスタムヘッダがセキュリティ監査で質問される可能性があること、そしてヘッダ名は衝突しないよう配慮することです。

## 実践ポイント
- Cloudflare Pagesを使っている場合、プロジェクトルートに_headersを置き、上記のように記述すれば即時適用される（デプロイ後に確認）。
- ブラウザのNetworkタブや `curl -I` でレスポンスヘッダを確認して正しく配信されているか検証する。
- 社内外での文化的トリビュートとして活用する場合は、ブランドや法務ポリシーと整合性をチェックする（公序良俗や商標などのリスク回避）。
- 同様の手法でチームメッセージや小さなイースターエッグを忍ばせることで、プロダクトに「人」を感じさせることができる。
