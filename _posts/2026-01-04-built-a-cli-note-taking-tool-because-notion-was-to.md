---
  layout: post
  title: "Built a CLI note-taking tool because Notion was too slow - Notionが遅すぎたのでCLIメモツールを作った"
  date: 2026-01-04T15:17:59.080Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "http://github.com/amritessh/ezNote"
  source_title: "GitHub - amritessh/ezNote: Zero-friction note taking for developers who live in the terminal"
  source_id: 471264573
  excerpt: "Notionより高速、即時起動で検索も速いRust製CLIメモezNote"
  image: "https://opengraph.githubassets.com/705da948f6c56dabe41881c038f67becdc4b531217d9ec2ee7ef32dad55193d4/amritessh/ezNote"
---

# Built a CLI note-taking tool because Notion was too slow - Notionが遅すぎたのでCLIメモツールを作った
ターミナルで一瞬でメモを取る――遅いNotionにサヨナラする開発者向けCLI「ezNote」の実力

## 要約
ターミナルに特化した軽量メモツール「ezNote」は、Rust製の単一バイナリでサブ10msの起動、SQLite FTS5による全文検索、ローカルファースト設計を特徴とする。Notionの重さ・コンテキストスイッチを嫌う開発者に即効性のある代替を提供する。

## この記事を読むべき理由
国内でもリモート開発やSSH／WSL中心のワークフローが増え、GUIツールへの往復で生産性を落としがち。企業のネットワーク制約やデータ保護方針のもとで「ローカルで高速にメモを取れる」ツールは実用的な価値が高い。ezNoteはそのギャップを端的に埋める実装例だ。

## 詳細解説
- アーキテクチャと技術選定  
  - 言語：Rust（速度・バイナリ配布の容易さ、低メモリ）  
  - ストレージ：SQLite（単一ファイルでバックアップ／同期が容易）、全文検索はFTS5を利用し高速な検索を実現。  
  - 配布：単一バイナリ（macOS/Linux/Windows）、Homebrew配布やインストールスクリプトを用意。依存なしで即実行可能。  

- 性能・UX  
  - コールドスタート < 10ms、ノート追加 < 5ms、10k件検索 < 50ms（著者のベンチマーク）。バイナリサイズは約3–5MB、メモリ使用 <10MB。  
  - カラフルで読みやすいターミナルUI、タグ・優先度によるフィルタリング、統計表示（利用習慣の可視化）。  

- CLI操作の流れ（典型例）  
  - 即時キャプチャ：ezn add "Fix auth bug in prod" --tag urgent --priority high  
  - 検索：ezn search "authentication bug"  
  - 日次振り返り：ezn today  
  - データはOSごとの定位置に保存（例：macOSなら ~/Library/Application Support/eznote/notes.db）。この単一ファイルはDropboxやiCloudで同期可能。  

- 開発・拡張性  
  - ソースはCargoでビルド可能。構造はCLI層、DB層、モデル、サービスに分かれており、機能追加（編集、エクスポート、同期、Web UIなど）の余地が明確。  

- セキュリティ・運用面の利点  
  - ローカル保存は企業のデータポリシーに適合しやすく、機密メモを外部に送らない運用がしやすい。内部ツールとの統合（CIコンテキストで自動タグ付け等）も将来のロードマップにある。

## 実践ポイント
- すぐ試す（Homebrew推奨）
```bash
# macOS / Linux (Homebrew)
brew tap amritesh/eznote
brew install eznote
# すぐ試す
ezn add "デプロイ前チェック: DBマイグレーション確認" --tag deploy --priority high
ezn list --today
```

- 使い方のコツ
  - ショートカット化：シェル関数やキーバインド（Alacritty/Kittyなど）に ezn add を割り当てると一発でキャプチャ可能。  
  - バックアップ：notes.db を定期的にクラウドストレージへコピーすれば簡単に同期・保全できる。  
  - 検索活用：FTS5なので複合語やフレーズ検索が高速。タグと組み合わせて運用するとTODO管理にも便利。  

- 企業導入での注意点
  - データ保護ポリシーに合わせて同期先を決める（社内NAS、S3互換ストレージ、個人クラウドなど）。  
  - Windows環境では PATH に追加するか WSL 経由で使うのが現実的。  

導入のハードルは低く、"Notionが重い・接続できない・ローカルに残したい" と感じる場面が多ければ即座に価値を発揮するツールです。興味があればGitHubリポジトリを覗いてビルドやプラグイン提案をするのも良い手です。
