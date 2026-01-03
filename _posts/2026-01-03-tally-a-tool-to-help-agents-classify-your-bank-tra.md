---
  layout: post
  title: "Tally – A tool to help agents classify your bank transactions - Tally — エージェントが銀行取引を分類するツール"
  date: 2026-01-03T12:34:10.427Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://tallyai.money/"
  source_title: "Tally - AI-Powered Transaction Classification Tool"
  source_id: 46475218
  excerpt: "AIとローカルで銀行CSVを自動分類し、細かな家計や事業費をプライバシー守って可視化するツール"
  image: "https://tallyai.money/screenshot.png"
---

# Tally – A tool to help agents classify your bank transactions - Tally — エージェントが銀行取引を分類するツール
クリックしたくなるタイトル案：AIとローカルファイルで家計を自動仕分けする「Tally」が日本でも使える理由

## 要約
TallyはAIコーディングアシスタント（GitHub Copilot、Claude Code、Codexなど）と連携して、銀行・カード取引CSVを自動で細かく分類するコマンドラインツール。ルールはプレーンなファイルで管理し、クラウドに送らずローカルで完結する点が特徴。

## この記事を読むべき理由
日本では口座情報の取扱いや会計カテゴリの細分化が重要（例：交通費・社内交際費・家計のサブカテゴリ）。Tallyはプログラマ向けの既存AIアシスタントを使い、手作業を減らしつつプライバシーを保って細かいカテゴリを作れるため、エンジニアや個人事業主、家計管理を自動化したい技術者に有益です。

## 詳細解説
- 問題点：銀行取引のCSVは「WHOLEFDS MKT」「AMZN MKTP」など分かりにくい表記が多く、銀行のカテゴリは大雑把（例：「Shopping」）で、詳細な集計が難しい。
- アプローチ：TallyはAIアシスタントへ逐次的に指示を出し、
  1. 未分類の取引を抽出
  2. AIが店舗名・コードを解釈してルールを生成（人間が書くような英語のルール）
  3. Tallyが適用して分類を繰り返す
- データ管理：設定とルールはローカルのファイル（DB/クラウド不要）。企業内や個人使用でのデータ流出リスクを低減できる点が大きな利点。
- 対応AI：コマンドラインで動くAIアシスタント（Copilot/Claude Code/Codexなど）と併用。AIに「SQ * は Square」「WHOLEFDS MKT は Whole Foods」といった解釈をさせ、ルール化する。
- 典型的ルール例（プレーン英語）：
  - "ZELLE to Sarah is babysitting → Childcare"
  - "COSTCO with GAS is fuel, otherwise groceries"
- ワークフロー：
  1. 銀行・カードからCSVをエクスポート
  2. tally init（設定フォルダとAIへの指示テンプレを作成）
  3. AIと対話しつつルールを生成
  4. tally runで分類済みのレポートを出力
- プラットフォーム：Linux/macOS向けのインストールスクリプトとPowerShellスクリプト（Windows）を提供。オープンソース（MIT）でGitHub公開。
- 注意点（日本固有）：
  - 銀行CSVのエンコーディング（Shift_JISなど）やカラム形式は銀行ごとに異なるため、事前にUTF-8変換とカラムマッピングが必要。
  - 日本語商号（コンビニ、飲食店名）、交通系IC（Suica等）の明細はAIに学習させる際にサンプルを多めに用意すると精度が上がる。
  - マルチ通貨や振込（振込人名）などはルールで細かく扱えるが、手作業でのルール調整が初期は必要。

インストール例（公式スクリプト）
```bash
curl -fsSL https://tallyai.money/install.sh | bash
```
Windows PowerShell:
```powershell
irm https://tallyai.money/install.ps1 | iex
```

基本コマンド：
```bash
tally init    # 設定フォルダ作成
tally run     # 分類してレポート生成
```

## 実践ポイント
- 最初は代表的な10〜50件で試す：CSVを少量で走らせ、AIが生成するルールを確認・修正する。
- CSV前処理：Shift_JIS→UTF-8変換、不要列削除、日付フォーマット統一を自動化しておく。
- 日本用ルールのテンプレ：コンビニ（コンビニチェーン名→「Food > Convenience」）、交通費（駅名・IC表記→「Transport」）、サブスク（Amazon定期→「Subscription」）などのサンプルを先に用意。
- バージョン管理：ルールファイルをGitで管理して差分を把握、バックアップを取る。
- プライバシー配慮：APIキーや個人情報はローカルに限定。必要なら社内のAIモデル（オンプレ）と組み合わせる。
- 貢献：オープンソースなので、日本語サンプルや銀行CSVのマッピングをGitHubで共有するとコミュニティ貢献になる。

短く言えば、Tallyは「AIと手元ファイルで高度な家計/会計分類を自動化」するツール。日本語取引や銀行フォーマットに合わせた前処理と少しのルール整備で、即戦力になる可能性が高いです。
