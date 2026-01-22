---
layout: post
title: "Spotify won court order against Anna’s Archive, taking down .org domain | Lawsuit was filed under seal; Anna’s Archive wasn’t notified until after takedown - SpotifyがAnna’s Archiveに対して裁判所命令を獲得、.orgドメインが削除される｜訴訟は非公開で提出され、Anna’s Archiveは削除後に通知された"
date: 2026-01-22T17:17:31.945Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://arstechnica.com/tech-policy/2026/01/annas-archive-said-spotify-scrape-didnt-cause-domain-suspension-it-was-wrong/"
source_title: "Spotify won court order against Anna’s Archive, taking down .org domain - Ars Technica"
source_id: 420288190
excerpt: "Spotifyが影のライブラリの.orgを非公開訴訟で差し止め、300TB超の流出問題暴露"
image: "https://cdn.arstechnica.net/wp-content/uploads/2026/01/spotify-logos-1152x648-1767642275.jpg"
---

# Spotify won court order against Anna’s Archive, taking down .org domain | Lawsuit was filed under seal; Anna’s Archive wasn’t notified until after takedown - SpotifyがAnna’s Archiveに対して裁判所命令を獲得、.orgドメインが削除される｜訴訟は非公開で提出され、Anna’s Archiveは削除後に通知された

300TBに及ぶとされる「Spotifyスクレイプ」が引き金に——影のライブラリAnna’s Archiveの.orgドメイン差し止めの裏側

## 要約
Spotifyと主要レーベル（Sony、Warner、UMG）がAnna’s Archiveを米裁判所に提訴し、非公開のまま差し止め（ex parte）の仮差止命令が出されて.PIRやCloudflareを通じて.orgドメインが利用不能になった。裁判所は後に仮処分を拡大する予備的差止を認めた。

## この記事を読むべき理由
ドメイン/CDN運用やスクレイピング、コンテンツ配信に関わる技術者やサービス運営者にとって、法的手段がどのようにインフラ側（登録機関・CDN）に効力を及ぼすかの実例であり、日本のホスティング事業者や研究者にも即応策やリスク管理の示唆があるため。

## 詳細解説
- 訴訟経緯：Spotifyと主要レーベルが年末にNY南部連邦地裁へ提訴。証拠保全や差し止めのため当初は訴状を封印（filed under seal）し、1月2日に裁判所が当日付けで仮差止（TRO）を出した。原告は被告に通知される前に措置を実施するよう求めたため、Anna’s Archiveは通知を受けたのちは既にドメインが遮断された状態だった。
- 技術的手法：裁判所命令はPublic Interest Registry（.orgの運営）やCloudflareなどCDN／ネームサーバ事業者に対し、該当ドメインの名前解決停止やホスティング停止を命じる形で実効性を持たせている。Cloudflareのようなリバースプロキシは、外部登録のドメインでも名前解決を介してアクセスを制御できるため、裁判所はこれを利用してアクセス遮断を実現した。
- 配布状況：Anna’s ArchiveはSpotifyから取得したとされるメタデータやトレントを一部公開していた。問題となったトレント群は数TB〜数十TB規模（個別で約6.2TBのセットが確認され、全体では報道で約300TBとされる）。一部ドメインは遮断されたが、別ドメインや直接リンクでファイル取得が続いている例もある。
- 法的論点：裁判所はAll Writs Actなどを根拠に第三者インフラ事業者へ命令を及ぼし、幅広い登録事業者・ホスティング会社（具体名を列挙）にも効力を及ぼすとした。匿名運営・仮想通貨での資金調達・海外レジストラの利用は執行の難易度を上げる一方で、裁判所はインフラ側を通じた実効的措置を選んだ。
- 関連判決：別件でWorldCat運営もデフォルト判決を取り、データ削除命令を得ている。実効性には疑問が残るが、運営側に圧力をかける手段として機能している。

## 実践ポイント
- サービス運営者/ホスティング事業者：不正配布や大規模スクレイピングの疑いがある場合、匿名利用やCDN依存のリスクを踏まえた利用規約・監視・インシデント対応フローを整備すること。
- 開発者/エンジニア：CDN・ネームサーバは法的命令でアクセス遮断手段になり得る。ログ保全やアクセス制御の設計を事前に見直す。
- 研究者/アーカイブ担当：大規模データ収集は権利者の許諾を得ることが最優先。公共性や学術目的でも法的リスクを評価し、オープンな代替手段を検討する。
- 日本市場への示唆：海外での裁判を起点に、日本のプロバイダや決済・クラウド事業者にも対応要請が波及する可能性があるため、国内事業者は国際的な権利侵害対応の体制整備を急ぐべき。

（出典：Ars Technicaの記事を基に要約・再構成）
