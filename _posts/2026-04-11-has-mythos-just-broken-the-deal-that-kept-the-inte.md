---
layout: post
title: "Has Mythos just broken the deal that kept the internet safe? - Mythosはインターネットの安全を守る“契約”を破ったのか？"
date: 2026-04-11T00:29:46.516Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://martinalderson.com/posts/has-mythos-just-broken-the-deal-that-kept-the-internet-safe/"
source_title: "Has Mythos just broken the deal that kept the internet safe? - Martin Alderson"
source_id: 47724957
excerpt: "**Mythosがサンドボックスを突破、ブラウザとクラウド危機、対策必須**"
image: "https://martinalderson.com/img/og/has-mythos-just-broken-the-deal-that-kept-the-internet-safe.png"
---

# Has Mythos just broken the deal that kept the internet safe? - Mythosはインターネットの安全を守る“契約”を破ったのか？
ブラウザもクラウドも危ない？Mythosが示した「サンドボックス破り」が意味する現実的リスク

## 要約
Anthropicの大規模モデル「Mythos」が、FirefoxのJSシェル向けに実動するエクスプロイトを72.4%の成功率で生成したと報告され、長年の「サンドボックスで守る」前提が揺らいでいる。

## この記事を読むべき理由
サンドボックスはブラウザ、スマホ、クラウド仮想化の基礎で、日本のサービスやインフラも依存しているため、攻撃の現実味は国内事業者・エンジニアに直結する問題です。

## 詳細解説
- サンドボックスとは：未信頼コードを隔離して実行権限を制限する仕組み。ブラウザのJS実行環境→ブラウザプロセス→OSアプリサンドボックス、という多層防御が一般的。  
- 事実関係：Anthropicの内部ベンチマークでMythosはFirefoxのSpiderMonkey（JSシェル）向けに実動エクスプロイトを72.4%で生成。数ヶ月前の別モデル(Opus)では1%未満だった。これは「ほぼゼロ」から「高確率」への急速な変化を示す。  
- なぜ危険か：サンドボックスを抜けられると、広告バナーや外部ウィジェット経由で配布された攻撃コードが端末やクラウド上で権限を奪い、データ漏洩や制御奪取を引き起こす可能性がある。クラウドの管理プレーンが侵害されれば大規模障害に発展する恐れがある。  
- 拡散の見通し：大規模モデルの能力は小型モデルにも短期間で先取りされやすく、また新しいハードで重いモデルが広く運用されれば悪用は時間の問題。Anthropicは限定公開とセキュリティ関係者向け対応を優先しているが、「知の漏出」は止められない可能性が高い。  
- 開発・OSSへの影響：Linuxカーネルなど大物は注目されるが、日常的に使われる膨大なOSSコンポーネントの多くはスコープ外のまま残るリスクがある。

## 実践ポイント
1. 基本のアップデート徹底：ブラウザ、OS、ランタイム、依存ライブラリを速やかに更新する。  
2. 最小権限設計：マイクロサービスやコンテナも含め、権限を絞る。管理プレーンのアクセス制御を強化する。  
3. 外部コンテンツの制限：広告やサードパーティスクリプトはCSPで制御、必要なら除去やサンドボックス属性を活用。  
4. 侵入検知とログ監視：異常な挙動や不審なプロセス起動を監視し、迅速な対応体制を整備。  
5. ソフトウェア供給網対策：自社で使うOSS・ライブラリの棚卸しと脆弱性対応計画を持つ。重要なOSSプロジェクトへの支援・連携を検討する。  
6. セキュリティ演習：サンドボックス破りを想定した検証・レッドチーム演習を行い、復旧手順を確認する。

短期的には冷静なパッチ適用と防御の強化、長期的にはサンドボックスに依存しすぎない設計とOSSエコシステムの強化が求められます。
