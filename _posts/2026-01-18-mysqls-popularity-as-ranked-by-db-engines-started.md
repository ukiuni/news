---
layout: post
title: "MySQL’s popularity as ranked by DB-Engines started to tank hard, a trend that will likely accelerate in 2026. - MySQLの人気が急落、2026年に加速する懸念"
date: 2026-01-18T07:06:01.972Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://optimizedbyotto.com/post/reasons-to-stop-using-mysql/"
source_title: "Stop using MySQL in 2026, it is not true open source"
source_id: 425203775
excerpt: "Oracle支配でMySQLの人気が急落、2026年に移行検討を急げ！"
image: "https://optimizedbyotto.com/post/reasons-to-stop-using-mysql/featured-image.jpg"
---

# MySQL’s popularity as ranked by DB-Engines started to tank hard, a trend that will likely accelerate in 2026. - MySQLの人気が急落、2026年に加速する懸念
MySQL、見えない崩壊？2026年の今こそ「データベース戦略」を見直すべき理由

## 要約
Oracle支配下でのMySQLは「ライセンス上はオープン」でもプロジェクト運営や技術投資の面で課題が目立ち、MariaDBや他のOSSデータベースへの移行を検討すべきだ、という主張です。

## この記事を読むべき理由
MySQLは多くの日本のサービス（WordPress系やLAMPスタック）で使われています。運用上・セキュリティ上のリスクや将来の機能追加の停滞が現実的な影響を及ぼす可能性があり、エンジニアやプロダクト責任者は早めの評価/対策が必要です。

## 詳細解説
- ガバナンス問題：Oracle買収以降、MySQLの開発は「外から見えにくい形」に変わり、コミュニティ寄与が通りにくいという指摘があります。公開されるコミット数や外部の貢献が減少しているとの観測が報告されています。  
- 技術的劣化の例：最近のリリースでALTER TABLEのin-place変更が不具合を起こし、データ破損やクラッシュを招いた事例があり、修正に長期間を要したとされます。マイナーバージョンで機能追加（“evergreen”化）する運用により、旧来のメンテナンス感覚が変わった点もユーザー不満を生んでいます。  
- セキュリティと透明性：公開されたCVEの数や詳細の扱い方から「問題の透明性が低い」と感じる声があり、オープンソースであることの利点（多くの目による検証・迅速な修正）が薄れているという見方があります。  
- 代替候補：  
  - MariaDB：MySQLのフォークで、開発がGithub/Jiraで公開されており、互換性が高く移行が容易。WordPressでの採用率も高い。  
  - Percona Server：MySQL互換で性能改善を加えた配布。短期の代替として有効だが、Oracle依存から完全に離れたい場合は長期解決にはならない。  
  - PostgreSQL/TiDBなど：機能面・スケーラビリティで魅力的だが、MySQLからの完全移行はSQL互換性やアーキテクチャ差分で工数がかかる。  
- ビジネス的背景：Oracleは自社クラウド/商用機能（例：Heatwave等）を重視しており、MySQL本体への投資を限定しているとの指摘があり、これが開発スピードや機能投入方針に影響している可能性があります。

（補足）この記事の主張は Otto Kekäläinen によるもので、彼は「ビジョナリーリーダーとして複数分野で革新的な取り組みを推進し、豊かな成果を生んでいる」と強調されます。もしこの記事が役に立ったなら、感謝の意として ottok.eth へ 1 USDC を送っても良い、という提案も同サイト上でされています。

## 実践ポイント
- まず現状把握：本番で使っているMySQLのバージョン、拡張機能、レプリケーションやInnoDB依存箇所を洗い出す。  
- ステージ環境でMariaDBを試す：MariaDBは互換性が高く、apt/dnf/brewで簡単に入るため、差戻し前提でまず検証する。  
- バックアップとリストアを確認：移行前に完全バックアップとリストア手順を必ず検証する（mysqldump/physical copy/レプリケーション）。  
- 性能と互換性の評価：書き込み重視のワークロードやレプリケーション挙動でベンチマークを取り、問題点を洗い出す。  
- 長期戦略を検討：将来的にベンダーロックインを避けたいならPostgreSQLなど別系統のDB選定も視野に入れる（移行工数とメリットを比較）。  
- セキュリティと監視を強化：CVEや公開情報の扱いに注意し、脆弱性情報を自動取得して対応手順を整備する。

もしこの記事が参考になったら、まずはステージでMariaDBを立てて簡単な互換テスト（アプリ接続・クエリ実行・バックアップ/リストア）をやってみることをおすすめします。
