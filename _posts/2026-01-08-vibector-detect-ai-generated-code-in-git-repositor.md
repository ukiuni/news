---
layout: post
title: "Vibector: Detect AI-generated code in Git repositories by analyzing commit patterns - Vibector：コミットパターンでAI生成コードを検出するツール"
date: 2026-01-08T16:17:25.471Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/anisimov-anthony/vibector"
source_title: "GitHub - anisimov-anthony/vibector: AI Code Detector based on commit patterns"
source_id: 468010736
excerpt: "Git履歴の急速な大規模変更を可視化し、AI生成疑いのコミットをオフラインで抽出"
image: "https://opengraph.githubassets.com/c183a9c3df1a1463d6eca0da8173b47f9bee8251df7d95bffb1fed29a2efa3af/anisimov-anthony/vibector"
---

# Vibector: Detect AI-generated code in Git repositories by analyzing commit patterns - Vibector：コミットパターンでAI生成コードを検出するツール
Git履歴の「速すぎる」「大きすぎる」変化を見える化して、AI生成や自動生成の疑いがあるコミットを素早く発見する

## 要約
VibectorはローカルのGitリポジトリを解析し、コミット間の差分・速度・統計的異常から「AIや自動生成の可能性がある」コミットを検出するオープンソースのGo製ツールです。読み取り専用でネットワークアクセスしないため、社内監査に使いやすい設計です。

## この記事を読むべき理由
日本企業やOSSの現場ではGit履歴を使ったコード監査やコードレビューの優先付けが重要です。CopilotなどAI支援が広がる今、短時間で大量の行が追加されたコミットや不自然なコミット間隔はレビュー対象を絞る手がかりになり、Vibectorはその候補を自動で抽出できます。データ流出を伴わないオフライン解析は特に日本のセキュリティ志向の強い現場で有益です。

## 詳細解説
- 解析の基本フロー
  - コミット取得：リポジトリからコミット列を取得（マージコミットはスキップ）。
  - ペア作成：連続するコミットをペアにして差分を計算。
  - Diff解析：各ペアの追加行数(additions)・削除行数(deletions)を計測。
  - 速度計算：コミット間の時間差からLOC（行数）/分の速度を算出。
  - 統計解析：リポジトリ全体のパーセンタイルなどを出して文脈を補足。
  - 閾値判定：設定値を超えるコミットを疑わしいものとしてフラグ化。
- 検出基準（READMEに基づく）
  - 絶対サイズ（例：追加500行超をフラグ）
  - 速度閾値（例：追加100 LOC/min、削除500 LOC/minなど）
  - 時間差（短すぎるコミット間隔をフラグ）
  - 統計的文脈（パーセンタイルによる相対的異常検出）
- 主な特徴
  - ローカルで完結（ネットワーク不要、テレメトリ送信なし）
  - 読み取り専用（リポジトリを変更しない）
  - 設定ファイル(.vibector.yaml)とコマンドラインオプションで閾値を柔軟に調整
  - ファイル除外指定（ログや生成ファイルを除いてノイズを減らす）
  - レポート出力はテキスト/JSON対応
- 実装と導入
  - Go製（go buildでビルド）。CI連携は「読み取り専用でオフライン」という性質上、社内CIや監査スクリプトに組み込みやすい。

簡単なインストール／実行例:
```bash
git clone https://github.com/anisimov-anthony/vibector.git
cd vibector
go build -o vibector ./cmd/vibector
# リポジトリ解析（例）
./vibector analyze /path/to/repo --output report.txt --suspicious-additions 500 --max-additions-pm 100
```

## 実践ポイント
- 初期閾値の目安：人間の典型的な追加速度は $20\text{–}50\ \mathrm{LOC/min}$、AI支援では $100+$ LOC/min が観測されるため、まずは `--max-additions-pm 100` などから試す。最低でも1つ以上の閾値を有効にする必要あり。
- 社内ルールとの組合せ：Vibectorは「疑わしいコミット」を列挙するツールなので、CIで自動ブロックするよりも人間レビューの優先度付けや監査ログ生成に使うのが安全。
- 除外設定を活用：ビルド生成物や大量ログを除外して誤検出を減らす（`.vibector.yaml`の`exclude_files`）。
- プライバシー要件が厳しい現場で使える：解析は完全にローカルで完結するため、社外へコードを送れない案件でも導入しやすい。
- 日本の現場での活用例：
  - OSSのメンテナが大量コミットを精査する際の補助リスト生成
  - 開発チームのコード品質監査・コンプライアンスチェック
  - セキュリティレビューでの事前スクリーニング
- 注意点：Vibectorは「AI生成の決定」ではなく「検査すべき異常コミットの検出」を目的とするため、検出結果は必ず人のレビューで裏取りすること。

以上を踏まえ、まず自分のリポジトリで閾値を緩めに設定して試し、誤検出の傾向を把握してから運用ルールに組み込むのが現場導入の近道です。
