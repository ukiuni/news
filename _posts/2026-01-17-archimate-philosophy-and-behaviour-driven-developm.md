---
layout: post
title: "ArchiMate philosophy and Behaviour Driven Development - ArchiMateの哲学と振る舞い駆動開発"
date: 2026-01-17T15:39:34.907Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://andremoniy.medium.com/archimate-philosophy-and-behavior-driven-development-3dcf2b62353e"
source_title: "ArchiMate philosophy and Behaviour Driven Development"
source_id: 424548853
excerpt: "BDDシナリオをArchiMateに直結し要件から設計・検証まで一貫管理"
---

# ArchiMate philosophy and Behaviour Driven Development - ArchiMateの哲学と振る舞い駆動開発
仕様はシナリオで設計する――ArchiMateとBDDが示す「同じ言語」

## 要約
ArchiMate（エンタープライズアーキテクチャ言語）とBDD（振る舞い駆動開発）は、一見別物に見えるが、同じ情報システムの「誰が・何を・なぜ・いつ・どこで・どうやって」を扱う共通哲学を持つ。具体的なシナリオ（例：Gherkin）からアーキテクチャ要素へ自然に落とし込める点が強みだ。

## この記事を読むべき理由
日本のSI／プロダクト開発現場では、要件の断片化やドキュメントと実装の乖離が課題になりやすい。ArchiMateとBDDを結び付けることで、ビジネス要求→振る舞い→構造（モデル）まで一貫した設計とトレーサビリティを実現しやすくなるため、現場の意思疎通と品質が向上する。

## 詳細解説
- 背景（ISA, Zachman, Sowa）
  - Zachmanの6列（What/How/Where/Who/When/Why）という情報システムの分類観が基礎にあり、Sowaらの概念グラフ理論が関係性の形式化を支える。
  - ArchiMateはこれを実務向けに整理し、層（Strategy/Business/Application/Technology/Implementation）と側面（Passive Structure／Behavior／Active Structure／Motivation）で表現する。

- ArchiMateとBDDの共通点
  - BDDのフィーチャ（As a / I want / So that）は、それぞれArchiMateのアクティブ構造（誰が）、振る舞い（何を）、動機（なぜ）に対応する。
  - Gherkinの Given / When / Then は、文脈（What／Where）、イベント（When／Who）、期待結果（What／Who／How）という具合にISAの列と重なる。
  - つまり「具体的なシナリオ＝自然言語で記述された振る舞い」が、そのままアーキテクチャ要素（アクター、プロセス、データ、トリガー、成果物）へマッピング可能。

- 具体例（要約）
  - 例：Given（時刻表） / When（8:00に出発したい） / Then（8:02の列車を案内される）  
  - このシナリオからは「時刻表（Passive Structure）」「旅客（Active Structure）」「旅程案内プロセス（Behavior）」「鉄道事業者の役割（Active Structure）」などが導出できる。

- 関係性の取り扱い
  - Sowaの概念グラフ的にシナリオを解析すると、述語（Agent, Object, Recipient, Obligation など）に対応するArchiMateの関係（Assignment, Access, Flow, Triggering 等）を割り当てられる。
  - これにより、BDDテストケースとアーキテクチャ図の間で意味的に一貫したトレーサビリティが確保できる。

## 実践ポイント
1. まず「シナリオ」を書く（BDDのGiven/When/Then）
   - ドメインの具体例を収集して短いシナリオにする。技術チームだけでなく事業側の言葉で書くのが肝心。
2. シナリオをArchiMateの要素にマッピングする
   - As a → Active Structure（誰）
   - I want → Behavior（何を）
   - So that → Motivation（なぜ）
   - Given/When/Thenそれぞれから Passive Structure / Event / Result を抽出して図に落とす。
3. 自動化・検証の導線を作る
   - GherkinシナリオはBDDツールで自動テストに繋げ、ArchiMateモデルは設計とドキュメントに使う。両者をリンクして変更時の影響を追えるようにする。
4. ツールとチーム運用
   - Archiや他のEAツールにシナリオ→要素を登録するテンプレートを作る。要件管理ツール（Jira等）と結びつけてトレーサビリティを保つ。
5. 日本市場での応用ポイント
   - 鉄道、金融、公共など規制と業務プロセスが複雑な領域で特に有効。実例をシナリオ化してから設計に落とすことで、合意形成と監査対応が楽になる。

まとめ：仕様書を「図」と「テストシナリオ」で同時に作る習慣を取り入れれば、要求→設計→実装の齟齬が減り、変更にも強いアーキテクチャが得られる。ArchiMateの構造化思想とBDDの例示的アプローチは、相性が良い。

---
