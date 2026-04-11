---
layout: post
title: "How I went from Oracle to Postgres (with a big NoSQL detour) with podcast guest Gwen Shapira - OracleからNoSQLを経てPostgresへ（Gwen Shapiraインタビュー）"
date: 2026-04-11T02:21:08.414Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://talkingpostgres.com/episodes/how-i-went-from-oracle-to-postgres-with-a-big-nosql-detour-with-gwen-shapira"
source_title: "Talking Postgres with Claire Giordano | How I went from Oracle to Postgres (with a big NoSQL detour) with Gwen Shapira"
source_id: 365986363
excerpt: "Oracle→NoSQLを経てPostgresへ移行した実務者の運用・コスト攻略"
image: "https://img.transistorcdn.com/_Q_MAD83Hcdk7ZWGepVJ6hO4D9zpjtF790Jnc04z-Tw/rs:fill:0:0:1/w:800/h:800/q:60/mb:500000/aHR0cHM6Ly9pbWct/dXBsb2FkLXByb2R1/Y3Rpb24udHJhbnNp/c3Rvci5mbS9iNGE3/ZmRmNmQ3NGVlZWIz/NWVmYWY5OWYzMGZm/ZjkyYi5wbmc.webp"
---

# How I went from Oracle to Postgres (with a big NoSQL detour) with podcast guest Gwen Shapira - OracleからNoSQLを経てPostgresへ（Gwen Shapiraインタビュー）
Oracle愛は捨てずに、NoSQLで迷走し、最終的にPostgresに「落ち着いた」理由――元Oracle運用者が語る現場視点の移行ストーリー

## 要約
元OracleエンジニアのGwen Shapiraが、NoSQLでのスケール経験を経てPostgresに戻り、なぜPostgresが「実務で頼れるDB」なのかを語るポッドキャスト回の要点を紹介します。

## この記事を読むべき理由
日本の多くの企業がOracleや分散NoSQLで悩む中、コスト、運用性、拡張性の観点からPostgresへの移行や共存戦略は実務的価値が高い。移行の勘所や現場で使えるテックヒントを初心者にもわかりやすく伝えます。

## 詳細解説
- 経歴と発見: Gwenは大規模Oracle運用から出発し、スケーラビリティを求めてNoSQLを長く使った経験がある。そこからPostgresに触れて「多くの必要機能が標準で揃っている」ことに気づき、Postgresの良さを再評価した。
- Postgresの強み（技術的ポイント）
  - トランザクションの信頼性と隔離レベルの実装（実運用での一貫性確保が容易）。
  - 拡張性：拡張やプラグインで用途に応じた最適化が可能（例：HypoPGのような仮想インデックスツールでプラン評価）。
  - JSONBや全文検索、パーティショニングなど「NoSQLっぽい機能」を1つのDBで扱える点。
  - コミュニティとエコシステム：ツール／議論（PGConf.dev等）で現場の課題解決が進む。
- キャリアとコミュニティの話: ブログ（例えば「Happiness Hints」）が技術発信とキャリア形成に効いたという実例。コンサルティング現場の鉄則（責任はコンサルの方に転がる、という教訓的な一言）も共有。
- イベントとトピック: PGConf.dev 2026やPG20の動き、Postgresを「Everything Database」とする潮流が注目されている。

## 実践ポイント
- 新規サービスはまずPostgresで検討する：トランザクション性・検索・JSON処理が一つのDBでできる利点を活かす。
- Oracleからの移行では機能対応表を作る（PL/SQL→PL/pgSQL、パーティショニング、シーケンスなどの差分を明示）。
- NoSQLが必要だった理由（スキーマ柔軟性、分散性）を振り返り、JSONBやパーティショニングで代替できるか検証する。
- HypoPGやプロファイラでクエリ設計を試す：本番前にインデックス設計の影響を評価。
- 情報発信（ブログ）やコミュニティ参加で知見を蓄積・共有する：PGConfやローカル勉強会に参加して実戦的な知識を得る。

短時間のポッドキャストから得られるのは「実務で役立つ視点」。Oracle経験者やNoSQLで苦戦した人ほど、Postgresの“静かな正解”に学びがあるはずです。
