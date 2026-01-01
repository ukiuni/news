---
  layout: post
  title: "hindsight: GitHub-style git activity visualizer for terminal - 端末用GitHub風gitアクティビティ可視化ツール"
  date: 2026-01-01T12:34:39.035Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/chaosprint/hindsight"
  source_title: "GitHub - chaosprint/hindsight: GitHub-style git activity visualizer for your terminal."
  source_id: 1220660664
  excerpt: "ローカルでGitHub風貢献グラフを端末に表示し、作者別集計やTSV出力で活動分析できるツール"
  image: "https://opengraph.githubassets.com/e7893c5c63f6279daf04d088dd3dc4e192913085a0490577ba1608870b9b7a9c/chaosprint/hindsight"
---

# hindsight: GitHub-style git activity visualizer for terminal - 端末用GitHub風gitアクティビティ可視化ツール
端末だけで自分の「貢献グラフ」を一望できる――hindsightでローカルリポジトリ群を可視化して開発習慣を見える化しよう

## 要約
hindsightはRust製のCLI/TUIツールで、指定ディレクトリ以下のgitリポジトリを走査してGitHub風の貢献ヒートマップ（青いピクセルのカレンダー）を端末上に表示します。ローカルで素早く履歴を可視化でき、TSVエクスポートや作者フィルタなど実用的なオプションを備えています。

## この記事を読むべき理由
- クラウドに履歴を上げずにローカルで活動を可視化したい開発者やチームに有効。  
- モノリポジトリや複数ワークスペースの貢献傾向を端末だけで確認でき、生産性分析やふりかえり資料作成に役立つ。  
- 軽量なRust製ツールなのでローカル開発環境（Linux/macOS/WSL）で手早く使える。

## 詳細解説
- 実装と公開情報  
  - 言語: Rust（リポジトリはRust 100%）  
  - ライセンス: MIT  
  - GitHubで軽量に公開されており（スター数は少数）、主にREADMEとソースで構成されています。

- 主な機能  
  - TUI表示（引数なしで現在ディレクトリを走査して起動）でGitHub風の年間ヒートマップを端末に描画。  
  - 指定日数分だけ遡る、ディレクトリ深度を制限して再帰的にリポジトリを検出、特定作者のみを集計するなどフィルタリングが可能。  
  - 集計結果をTSVでエクスポートしてスプレッドシートや社内ダッシュボードに取り込める。  
  - コンソール出力用の詳細テーブル表示（--list）も備える。

- 主要コマンドとオプション（概要）  
  - インストール: cargo経由で導入（Rustとcargoが必要）。  
  - オプション例: --path（走査ディレクトリ）、--days（過去N日、デフォルト365）、--depth（再帰深度、デフォルト3）、--authors（カンマ区切りで名前指定）、--export-tsv（ファイル出力）。  
  - モノリポや大量リポジトリを扱う場合は--depthや--pathで走査範囲を絞ると高速化できる。

## 実践ポイント
- インストールと基本実行例
```bash
# Rustが入っている前提で
cargo install hindsight

# 現在の作業ディレクトリを走査してTUI起動
hindsight

# 指定ワークスペースを30日分だけ解析
hindsight --path ~/Dev --days 30

# 自分のコミットだけを表示
hindsight --authors "Taro Tanaka,tanaka@example.com"

# 年間集計をTSVとして保存
hindsight --export-tsv 2025_stats.tsv
```
- 日本のプロジェクトでの活用アイデア  
  - リモートワーク／フレックスで見えにくい貢献を定量化して週次・月次のふりかえり資料にする。  
  - 社内レポート用にTSVを生成して、BIやスプレッドシートで可視化を拡張する。  
  - セキュリティや企業ポリシーで外部サービスにコミット履歴を出せない場合のローカル代替手段として有効。  
- 注意点  
  - Windowsネイティブで使う場合はWSLやGit for Windows＋cargoのセットアップが現実的。  
  - 大規模ワークスペースでは走査時間がかかるため--depthや--pathで調整する。

## 引用元
- タイトル: hindsight: GitHub-style git activity visualizer for terminal  
- URL: https://github.com/chaosprint/hindsight
