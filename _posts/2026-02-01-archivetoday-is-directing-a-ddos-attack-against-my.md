---
layout: post
title: "archive.today is directing a DDOS attack against my blog - archive.todayが私のブログにDDoS攻撃を仕掛けている"
date: 2026-02-01T21:50:53.255Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://gyrovague.com/2026/02/01/archive-today-is-directing-a-ddos-attack-against-my-blog/"
source_title: "archive.today is directing a DDOS attack against my blog &#8211; Gyrovague"
source_id: 754534992
excerpt: "archive.todayのCAPTCHAが閲覧者を踏み台に個人ブログをDDoS化する手口と防御法"
image: "https://i0.wp.com/gyrovague.com/wp-content/uploads/2026/02/image.png?fit=1200%2C798&#038;ssl=1"
---

# archive.today is directing a DDOS attack against my blog - archive.todayが私のブログにDDoS攻撃を仕掛けている
アーカイブサービスが閲覧者を“踏み台”に——個人ブログを狙った奇妙な攻撃の全貌

## 要約
archive.todayのCAPTCHAページ上のJavaScriptが、訪問者のブラウザを使ってGyrovagueの検索エンドポイントへ高頻度リクエストを送り、結果的にDDoSに近い負荷をかけていると報告されています。

## この記事を読むべき理由
外部サービスが利用者をプロキシ化して他サイトへ負荷を与える新たな手口は、日本の個人運営サイトや中小サービスにも現実的な脅威です。対策と検出方法を知っておく価値があります。

## 詳細解説
攻撃の仕組み（要点）
- archive.todayのCAPTCHAページが利用者のブラウザで定期的に検索リクエストを発行するスクリプトを実行。
- リクエストはランダムクエリを付与してキャッシュを効かせないようにし、短い間隔で繰り返すことでサーバ負荷を高める。

問題のスクリプト（抜粋）
```javascript
setInterval(function() {
  fetch("https://gyrovague.com/?s=" + Math.random().toString(36).substring(2, 3 + Math.random() * 8), {
    referrerPolicy: "no-referrer",
    mode: "no-cors"
  });
}, 300);
```

ポイント解説
- mode: "no-cors" と referrerPolicy:"no-referrer" により、ブラウザは簡単にリクエストを送信し、サーバからの詳細なレスポンスは得られないがリクエスト自体は発生する。
- ランダムクエリでキャッシュヒットを防ぎ、サーバ側の検索処理を毎回実行させる設計。
- 実行間隔は300msなので多数の閲覧者が居れば短時間で負荷が急増する。
- uBlock Originなどの広告ブロッカーでブロック可能（既にdns-blocklistsに登録される動きあり）。

経緯（簡潔）
- 2023年8月：著者がarchive.todayを調査する記事を公開。
- 2025年11月：外部報道でarchive.todayに捜査の動き。
- 2026年1月：著者へGDPR申し立てややり取り、そしてCAPTCHA経由の波及リクエストが確認され、コミュニケーションと脅迫まがいの応答も発生。
- 対処としてコミュニティやブロックリストが動き、影響の可視化と抑止へつながった。

法的／倫理的側面
- 利用者を無断で踏み台にする行為は重大な倫理問題であり、サービス提供者やホスティングに報告・証拠保存が必須。

## 実践ポイント
- 即効対策
  - uBlock Originなどでarchive.todayドメインをブロックするよう案内する（利用者側の対策）。
  - サーバ側で該当パターン（短期間の検索クエリの急増、同一UAやreferrerの疑わしいリクエスト）をブロック。
- 永続対策
  - 検索APIにレートリミットを導入。IP単位／セッション単位の閾値を設ける。
  - 検索フォームにトークン（CSRFトークン）やPOST限定化、簡易なCAPTCHAを導入してクロスサイトでの大量発行を防止。
  - WAFやCDN（Cloudflare等）のボット管理・レート制御を利用。
  - ログとネットワークキャプチャを保存し、ホスティング事業者や法的機関への報告に備える。
- コミュニティ連携
  - dns-blocklistsやuBlock等のコミュニティリストに登録依頼して拡散してもらう。
  - 事象を簡潔にまとめて公開し、同様被害の早期発見に寄与する。

短くまとめると、外部アーカイブが「閲覧者を踏み台」にしてDDoS的な負荷を発生させる新しい攻撃ベクトルが現実化しています。まずはログの監視とレート制御、そしてWAF/CDNでの防御を優先してください。
