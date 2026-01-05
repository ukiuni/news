---
  layout: post
  title: "Gatekeepers of Law: Inside the Westlaw and LexisNexis Duopoly - 法の門番：WestlawとLexisNexisの寡占の内幕"
  date: 2026-01-05T20:36:42.006Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.thebignewsletter.com/p/gatekeepers-of-law-inside-the-westlaw"
  source_title: "Gatekeepers of Law: Inside the Westlaw and LexisNexis Duopoly"
  source_id: 46502736
  excerpt: "WestlawとLexisNexisの寡占が法情報とAIの可能性を奪う現状と対策"
  image: "https://substackcdn.com/image/fetch/$s_!yPNE!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa12d7b2d-3c6e-4d69-a075-40772d1bff12_1152x920.png"
---

# Gatekeepers of Law: Inside the Westlaw and LexisNexis Duopoly - 法の門番：WestlawとLexisNexisの寡占の内幕
法は誰のものか？AI時代に迫る「リーガル情報の有料化」とその打開策

## 要約
米国の判例・法令データは長年、WestlawとLexisNexisという二大プラットフォームに支配されてきた。歴史的な編集手法とM&A、裁判所の有料提供が組み合わさり、検索コストと参入障壁が高止まりしている。

## この記事を読むべき理由
検索やAIによる法的説明が一般化する今、法情報が閉ざされていることは技術者・起業家・市民すべてにとって重大な課題。日本でも同様の情報独占やデータ利用ルールが新しいサービスの出現を左右するため、現状と打開策を知っておく必要がある。

## 詳細解説
- 歴史的背景：米国では印刷時代にWest Publishingが「National Reporter System（地域別の判例集）」と独自のKey Number（法トピックの目次化）を整備し、ページ番号やヘッドノートが事実上の参照インフラになった。これが業界標準の索引・引用方式を作り、強いロックイン効果を生んだ。
- 技術革新と争点：1970〜80年代の電子化でLexisが最初に判例検索をデータベース化、WestもWestlawで追随した。問題は「ページネーションや編集付加」が著作権の対象となり得るかで、1991年のFeist判決以降、単なる機械的付番は創作性がないとされたが、業界の慣行と参照規則（例：Bluebook）がロックインを維持した。
- 集中と政治的経緯：90年代以降の買収ラッシュで主要プレイヤーが統合され、実質的な寡占が成立。経済的・政治的背景が合併の監視を弱めたことも指摘される。結果、ある検索一回で数百ドルに上る価格設定や、裁判所が電子記録のアクセスで手数料を課す事例が残る。
- AI時代のインパクト：生成AIは質の高い法データにアクセスできれば解釈支援が可能だが、データが有料・クローズドであればAIの力は限定的。さらにKey Numberのような構造化されたメタデータは検索精度と説明可能性に直結するため、誰がそのメタデータをコントロールするかが重要。

## 実践ポイント
- エンジニア/プロダクト責任者向け
  - 公的判例・法令はまずはパブリックドメインを掘る。政府や裁判所が公開している生データから独自のインデックス・メタデータを作る余地がある。
  - Open citation（引用の開放）と互換フォーマット（法令ID、タイムスタンプ、段落参照など）を採用し、Bluebook型のページ依存に依存しない設計を検討する。
  - AIに投入するデータは出典付きで保守し、説明責任（explainability）を確保するために独自の注釈レイヤーを持つ。
- 法務／政策提案者向け
  - 行政／裁判所に対して、判決テキストの無償公開と機械可読フォーマットでの提供を求めるアドボカシーを行う。
  - 競争政策の観点から、情報インフラの寡占がサービス価格とアクセスに与える影響を監視・提言する。
- 起業家向け
  - 有料データに頼らない差別化：注釈・ケースサマリ、AIによる要約、Jurisdiction特化型UIなど付加価値で勝負する。
  - 大学や公共機関と協業してオープンデータの収集・整備を行い、信頼できる代替基盤を作る。

短く言えば、データの所有権と参照方式（どのページを「正しい」とするか）が技術とビジネスの勝敗を決める。AIが法を「民主化」する可能性はあるが、その鍵は「誰が法情報の索引とアクセスを握るか」にある。日本の技術者や政策担当者も、この局面で能動的にインフラ設計と公開ルールを議論する必要がある。
