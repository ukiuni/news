---
layout: post
title: "I added a Bluesky comment section to my blog - ブログにBlueskyのコメント欄を追加した"
date: 2026-01-24T21:45:58.980Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://micahcantor.com/blog/bluesky-comment-section.html"
source_title: "I added a Bluesky comment section to my blog"
source_id: 46747366
excerpt: "静的ブログにBlueskyの返信を埋め込み、認証不要で会話を表示する簡単実装ガイド"
---

# I added a Bluesky comment section to my blog - ブログにBlueskyのコメント欄を追加した
静的サイトに“本物のコメント欄”を手間なく組み込む――Blueskyで実現したシンプル実装ガイド

## 要約
CDNで配信する静的ブログに、Bluesky上の返信を埋め込むことで「読み書きはBluesky側、表示は自サイトで」のコメント欄を実装した話。OAuthでの投稿は省き、読み取り専用で簡潔にまとめている。

## この記事を読むべき理由
静的サイトやJamstackで運用する日本の個人ブロガー／小規模メディアにとって、コメント運用のコスト（ホスティング・スパム対策・モデレーション）をほぼゼロにしつつ、サイト上で会話を見せられる現実的な手法だから。

## 詳細解説
- アプローチの要点  
  - コメントの「保存・認証・モデレーション」はBlueskyに任せ、サイト側はBlueskyの公開APIから返信を取得して表示するだけにする方式。これにより自分で常時稼働する動的サービスを運用する必要がなくなる。
- 技術スタックと実装の流れ  
  - ブログはReact Server Components + Parcel、記事はMDXで記述。各記事にmetadataオブジェクトをエクスポートし、そこにBlueskyのpost ID（bskyPostId）を紐付ける。  
  - TypeScriptで @bluesky/api を利用し、AT Protocolの getPostThread エンドポイントに与えられたURIから投稿とその返信を取得する。  
  - フロント側では fetch/useEffect でも実装できるが、読み込みやエラー処理を楽にするため TanStack の react-query を使ってAPIの状態管理（キャッシュ・再試行・ローディング/エラー）を委譲している。  
- 表示の工夫と制限  
  - Blueskyの投稿はリッチな構造を持つが、まずは本文テキストのみを抽出して表示するシンプル実装に留める（添付や複雑なマークアップは無視）。  
  - スレッド表示は返信をインデント＋左ボーダーで視覚的に追いやすくし、プロフィール画像や投稿日などはBlueskyのデザインを参考に配置した。  
  - 投稿機能（書き込み）は一度OAuthで実装しかけたが、独自UIを整えるコストやユーザーのサインインの手間を考え、当面は読み取り専用にしている（「返信したければBlueskyで」への誘導を併記）。
- なぜBlueskyを選ぶか  
  - AT Protocolというオープンな基盤で動くためプラットフォームの独占リスクが低く、会話（ソーシャル）のホスティングにはGitHub Discussions系より適している、という判断。

## 実践ポイント
- 記事メタデータにBlueskyの投稿IDを追加する（例）  
```typescript
export const metadata = {
  title: "記事タイトル",
  description: "説明文",
  date: "2026-01-24",
  bskyPostId: "<post-id>",
  tags: ["web-dev"],
};
```
- @bluesky/api の getPostThread を使って返信を取得する。  
- react-query で取得・キャッシュ・エラー処理を管理する（useQuery を活用）。  
- Blueskyのリッチ構造はまずテキストだけ抜き出す。スレッドはインデント＋左ボーダーで見やすく。  
- 投稿は当面オフにして、親ポストへのリンクを明示してユーザーをBlueskyへ誘導する。  
- 実装は小規模（約200 LOC）なので、自サイトに合わせたスタイル調整や将来的な機能追加（いいね表示やユーザーリンク等）は容易。

興味があれば、実装例やReactコンポーネントの抜粋を提示できます。どのレベルのサンプルが欲しいですか？
