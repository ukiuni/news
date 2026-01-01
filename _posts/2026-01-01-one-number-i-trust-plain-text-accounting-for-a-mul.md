---
  layout: post
  title: "One Number I Trust: Plain-Text Accounting for a Multi-Currency Household - 単一の信頼できる数値：多通貨家計のプレーンテキスト会計"
  date: 2026-01-01T14:49:23.122Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://lalitm.com/post/one-number-i-trust/"
  source_title: "One Number I Trust: Plain-Text Accounting for a Multi-Currency Household - Lalit Maganti"
  source_id: 1060096751
  excerpt: "Beancountで多通貨家計をプレーンテキスト管理し、週20分で一つの信頼できる純資産を作る方法"
  ---

# One Number I Trust: Plain-Text Accounting for a Multi-Currency Household - 単一の信頼できる数値：多通貨家計のプレーンテキスト会計
「通貨が違っても、たった1つの“信頼できる純資産”を作る方法 — エンジニア視点のPlain‑Text会計」

## 要約
エンジニアがBeancount（Pythonライブラリ）とプレーンテキスト会計で構築した、多通貨・二人分の家計管理システム。毎週20分の運用で「信頼できる一つの純資産数字」を得る手法を紹介する。

## この記事を読むべき理由
日本でも海外資産や外貨建て投資を持つ個人が増えている今、銀行や家計アプリの目に見えないズレ（遅延、欠落、集計ミス）を避け、完全に可査証（audit）できる方法は価値が高い。エンジニアや細かい管理を好む人にとって実践的で拡張しやすい選択肢になる。

## 詳細解説
- 根幹は「複式簿記（double-entry bookkeeping）」。任意の取引は複数の側面を持ち、合計は常にゼロに保つ。例：
  - 振替（口座A→口座B）の表現は $-1000 + 1000 = 0$。
  - 友人と行った会食（合計$90$）は $-90 + 30 + 30 + 30 = 0$ と表せ、個人負担だけを正確に把握できる。
- プレーンテキスト会計の利点：
  - すべてテキストで管理するためgitで差分や履歴確認が容易。プライバシーを保ちつつ変更理由を追える。
  - フォーマットが自由なためエクスポート・変換・スクリプト処理が簡単。
- Beancountを選ぶ理由：
  - Pythonライブラリとしてインポート処理やカスタム処理が書きやすい。
  - アカウント宣言や取引の整合性チェックが厳格でミスを早期発見できる。
  - FavaなどのGUIで残高表、損益、トランザクションジャーナル、クエリ、チャートを可視化可能。
- 実際の運用フロー（著者の例）：
  - 銀行PDFからインポーターで取引を取り込み（CSVよりPDFの方が安定する場合あり）。
  - ウェブUIでカテゴリ分けを行い、スクリプトを走らせてレポート生成、gitでコミット。
  - 毎週20分×週一回で最新の純資産推移を保守。

## 実践ポイント
- まずは実物で試す：BeancountとFavaを入れて、サンプルリポジトリから始める。
  - 例：git clone でデモを取得して動かすとイメージが掴みやすい。
  - 設定の最小手順（ローカルでの試用）を短時間で終えられる。
- アカウント設計を丁寧に：
  - 資産（Assets）、負債（Liabilities）、収入（Income）、費用（Expenses）、資本（Equity）を明確に分ける。
- マルチカレンシー対策：
  - 為替換算ルール（基準通貨、評価日時）を決めて自動化。外貨建て資産は定期的に時価評価するスクリプトを用意する。
- 自動化と可監査性：
  - PDF→取引のインポーターを作る／流用し、gitで履歴管理。税務や監査時に差分と説明が残る利点は大きい。
- 労力配分：
  - 日常の家計管理だけなら過剰投資。複数通貨や投資・配偶者等で複雑なら有力な選択肢。

## 引用元
- タイトル: One Number I Trust: Plain-Text Accounting for a Multi-Currency Household
- URL: https://lalitm.com/post/one-number-i-trust/
