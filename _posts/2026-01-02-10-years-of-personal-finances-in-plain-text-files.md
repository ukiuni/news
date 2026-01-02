---
  layout: post
  title: "10 years of personal finances in plain text files - プレーンテキストで10年分の個人財務を管理する"
  date: 2026-01-02T07:05:34.017Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://sgoel.dev/posts/10-years-of-personal-finances-in-plain-text-files/"
  source_title: "10 years of personal finances in plain text files | Siddhant Goel"
  source_id: 794946033
  excerpt: "BeancountとGitで10年分の取引・領収書をプレーンテキストで安全に自主管理する方法"
  ---

# 10 years of personal finances in plain text files - プレーンテキストで10年分の個人財務を管理する
エクセルや家計アプリに頼らない「自分だけの会計台帳」──プレーンテキスト×Beancountで築いた10年分の資産管理術

## 要約
著者はBeancount（プレーンテキスト会計）を使い、毎月30〜45分の作業で10年分の取引をローカルに蓄積。約10,000件の取引、20,000件の投稿、そして500件以上の添付ドキュメントをGitで管理している。

## この記事を読むべき理由
- データ主権：個人の財務データをクラウド依存にせず、自分のマシンとバージョン管理で保つ手法は日本でも重要な潮流。  
- 自動化と透明性：銀行CSV→インポーター→手作業での整合チェックという実務ワークフローは、会計の自動化や税務対応に直結する。  
- 再現性：プレーンテキストなら将来のフォーマット変化に強く、分析や監査が容易。

## 詳細解説
- Beancountの基本  
  - テキストファイルでダブルエントリ（複式簿記）を記録。1件の取引に複数のposting（振替）を持つ。著者のリポジトリは16ファイル・45,000行超、bean-queryで12466ディレクティブ（約9,895取引・19,743投稿）を確認。  
- 月次ワークフロー（所要30–45分）  
  1. 銀行からCSVをダウンロード（PDFよりCSVがパースしやすい）。  
  2. CSVをインポーターでBeancountの構造に変換。  
  3. 変換結果をmain.beancountに追記し、1件ずつ残高が合うか（sum == 0）を確認・修正。  
  4. 年が変わったらその年のファイルを切り分け、mainからincludeする運用で可読性を保つ。  
- インポーター（拡張点）  
  - インポーターはPythonクラスで、銀行ごとのCSVフォーマットをBeancountエントリにマッピングする。著者はドイツ銀行群向けに複数のインポーター（beancount-dkb, beancount-ing, beancount-n26 等）を作成・保守。  
  - 実務上の課題は記述揺れ（説明文の正規化）、未バランスの自動補填ルール、PDF添付の管理など。  
- ドキュメントの添付と税務対応  
  - 取引ごとに領収書や請求書を添付する運用で、確定申告などの際に該当書類をすぐ参照できる。著者リポジトリには500件超のPDFが保存されている。  
- 分析ツール群  
  - bean-queryなどで取引集計やアカウント一覧（著者は1086アカウントを定義）を実行し、カスタムレポートを作れる。

## 実践ポイント
- 最初は直近1〜2ヶ月分から始める：既存の家計アプリを捨てず、小さく移行して運用コストを見積もる。  
- Gitでバージョン管理：差分とメタデータ（いつどのレシートを添付したか）が残る。  
- CSVインポーターは最初は簡易ルールでOK：まずは日付・金額・説明を正しく取り込み、未バランスは手動で補正。徐々に自動ルールを増やす。  
- 年単位でファイルを分割：main.beancountにincludeする運用は可読性とパフォーマンスの両立に有効。  
- 日本の銀行対応：ドイツ向けの実装例を参照しつつ、日本の銀行CSVフォーマットに合わせたインポーターを自作またはコミュニティ実装を探す（銀行ごとにエクスポート仕様が異なるため、テンプレート化が鍵）。  
- すぐ使えるコマンド：bean-queryで年別集計やカテゴリ別集計を作り、月次レビューで使いこなす。

## 引用元
- タイトル: 10 years of personal finances in plain text files  
- URL: https://sgoel.dev/posts/10-years-of-personal-finances-in-plain-text-files/
