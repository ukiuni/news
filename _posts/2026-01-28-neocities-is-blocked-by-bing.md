---
layout: post
title: "Neocities Is Blocked by Bing - Bing による Neocities ブロック"
date: 2026-01-28T11:22:54.720Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.neocities.org/blog/2026/01/27/bing-block.html"
source_title: "Neocities Is Blocked by Bing"
source_id: 1522629960
excerpt: "BingがNeocitiesをドメイン丸ごと検索から排除、150万サイトの発見性が消えた理由と対策"
---

# Neocities Is Blocked by Bing - Bing による Neocities ブロック
Bingが150万以上の個人サイトを丸ごと検索結果から消した理由 — インディーWebの“発見性”が脅かされる

## 要約
Bingが neocities.org（および全サブドメイン）を検索インデックスから完全に除外し、一時的に詐欺サイトを上位に表示するなどの問題が発生。Neocities側は複数回の問い合わせで説明や解決を得られず、現在はBing及びBing依存の検索エンジン回避を推奨している。

## この記事を読むべき理由
検索エンジンからの流入は個人サイトやポートフォリオ、小規模サービスの生命線です。日本でも同様のホスティングや個人制作が多く、発見性が失われることはクリエイターや企業の可視性・信頼に直結します。

## 詳細解説
- 完全除外（block）とは：ランキング低下や一時的クロール問題ではなく、ドメイン単位で検索結果から排除される状態。neocities.org と example.neocities.org のようなサブドメインすべてが対象になった。  
- 表示されたリスク：neocities 検索で詐欺サイトが上位に出現し得るため、ユーザー被害の可能性がある（発見性低下と並行して安全性の懸念）。  
- 対応の経緯：NeocitiesはBingのWebmasterツールやサポート、内部チャネルを通じ複数回問い合わせたが、明確な理由提示や解除が得られていない。  
- 技術的要因の否定：Neocitiesはマルウェア蔓延や明確なポリシー違反、一般的な設定ミスを原因とはしておらず、モデレーションや通報対応も行っていると説明。  
- 連鎖影響：DuckDuckGo 等、Bingの結果を利用する検索エンジンにも波及するため、被害が広範に及ぶ可能性がある。  
- 検索の仕組み観点：検索エンジン側はドメインブロック、手動のペナルティ、または機械学習に基づくフィルタで結果を操作できる。ドメイン単位の全除外は復旧交渉無しには難しい。

## 実践ポイント
- 自サイトの可視性確認：Google、Bing、DuckDuckGo 等で自サイト（サブドメイン含む）が見えるかチェック。  
- サーチコンソール類の確認：Google Search Console と Bing Webmaster Tools にサイトを登録し、クロール／インデックス状況を確認。異常があればスクリーンショットとログを保存。  
- 基本の整備：sitemap.xml、robots.txt、正しいCanonical、構造化データを整えておく。  
- 通知と広報：検索で見つからない可能性をユーザーに告知。RSSやSNS、ディレクトリにミラーを置く。  
- 不審サイト対策：検索で偽装・フィッシングと思われる結果を見つけたらBingへ報告し、訪問者へ注意喚起。  
- 代替発見経路の活用：Googleや独立したディレクトリ、インディーWebコミュニティ、archive.org 等を活用して発見性を確保する。

短く言えば：検索依存のリスクを分散し、インデックス状況の監視と代替流入経路の確保が今すぐ必要です。
