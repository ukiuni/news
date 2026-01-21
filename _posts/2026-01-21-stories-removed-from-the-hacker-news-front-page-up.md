---
layout: post
title: "Stories removed from the Hacker News Front Page, updated in real time - ハッカーニュースのフロントページから削除された投稿（リアルタイム）"
date: 2026-01-21T13:24:08.988Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/vitoplantamura/HackerNewsRemovals"
source_title: "GitHub - vitoplantamura/HackerNewsRemovals: List of stories removed from the Hacker News Front Page, updated in real time."
source_id: 46704555
excerpt: "HNの注目投稿がなぜ消えるかを1分ごとに検出・記録し削除傾向を可視化"
image: "https://opengraph.githubassets.com/4a33707149a97bf490687f4ce308836dbbb0fb11a225dffff413831aaf8e9b06/vitoplantamura/HackerNewsRemovals"
---

# Stories removed from the Hacker News Front Page, updated in real time - ハッカーニュースのフロントページから削除された投稿（リアルタイム）

知られざるHNの裏側：消された注目投稿をリアルタイムで追う小さな監視プロジェクト

## 要約
GitHub上の小規模プロジェクトが、Hacker Newsのフロントページから「突然消えた」投稿を1分ごとに検出・記録する。削除頻度や対象ジャンルを可視化することで、モデレーションの実態を追える。

## この記事を読むべき理由
Hacker Newsはグローバルな技術トレンドやスタートアップの注目度を左右します。日本のOSSやスタートアップが国際的に見られる機会にも関わるため、「なぜ注目投稿が消えるのか」を知ることは情報戦略や透明性の理解に直結します。

## 詳細解説
- 目的と背景：作者はフロントページ上の「公開されるモデレーション（タイトル変更／削除）」のパターンを理解したくてツールを作成。特にタイトルの差し替えや投稿の削除が話題性にどう影響するかに注目している。
- 仕組み（技術的ポイント）：
  - 公式HN APIの top stories を毎分取得する（最大90件）。
  - 直近の「トップ30（フロントページ）」と1分前のデータを比較し、過去のトップ30に存在したが現在はトップ90にいない投稿を「削除された可能性あり」としてログに残す。
  - 初回フロント掲載時のタイトル／URLを保持し、削除時のポイント数・コメント数・ランクは削除時点の値を記録する。
  - 再びフロントに戻った投稿はログから削除される。Second-chance pool（復活プール）にいる投稿は除外される。
- 前提と限界：
  - コアの仮定は「投稿が1分で30位→90位以下に急落するのは削除以外に考えにくい」という点。しかしこの前提はHNコミュニティで議論があり、完全無欠ではない（重複投稿や一時的な順位変動、API遅延などのノイズがある）。
  - 自動で重複投稿を判定できないため、重複による削除は誤検出になりうる。
  - 作者自身もHN支持者であり、透明性のために公開する意図を明確にしている。
- 付加情報：各投稿のIDは news.social-protocols.org のページへリンクし、投稿のフロントでの位置推移をグラフで見ることができる。

## 実践ポイント
- まず見る：GitHubリポジトリをウォッチしてリアルタイムな一覧を確認し、気になる削除のトレンド（例：LLM関連ばかり消える）を観察する。
- 自分で使う：ローカルで動かしてアラートを建てる（WebhookやSlack通知）と、関係する自分の投稿が「なぜ」見えなくなったかを早く把握できる。
- 検証の手順：削除を見つけたら（1）重複投稿か？（2）タイトル編集で意図が変わっていないか？（3）news.social-protocols.orgで順位推移を確認、の順で判断する。
- 貢献方法：誤検出を減らすためにリポジトリにIssueを出すか、重複判定やAPI安定化のためのPRを送るのが有益。
- 簡易実行例（.NETが必要）：

```bash
git clone https://github.com/vitoplantamura/HackerNewsRemovals.git
cd HackerNewsRemovals
dotnet run --project Program.csproj
```

短く言えば、このプロジェクトは「見えないモデレーション」を可視化して議論を促すツールです。日本の開発者・広報担当は、国際的な露出が不自然に減ったと感じたときの初動調査ツールとして覚えておくと役立ちます。
