---
  layout: post
  title: "I built a \"Zero Trust\" linter for AI-generated code - 「Zero Trust」なAI生成コード向けリンターを作った"
  date: 2026-01-08T08:34:02.940Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/skew202/antislop"
  source_title: "GitHub - skew202/antislop: A blazing-fast, multi-language linter for detecting AI-generated code slop"
  source_id: 469406516
  excerpt: "AI生成の「動くけど怪しい」コードを瞬時に検出し、CIで手戻りとセキュリティリスクを削減するリンター"
  image: "https://opengraph.githubassets.com/6e738c7ebb5013f6b2385f9c6230b0b075aad63151d10adf2dc62934cbae1a2d/skew202/antislop"
---

# I built a "Zero Trust" linter for AI-generated code - 「Zero Trust」なAI生成コード向けリンターを作った

AIが出す「動くけど怪しい」コードを瞬時に暴く—Zero Trustリンター「AntiSlop」を使って手戻りを減らす方法

## 要約
AI補助で書かれた「やっつけコード（slop）」を検出する高速マルチ言語リンター。TODO・仮実装・「for now」系の保留表現・ダミーデータなど、意図と実装のズレを素早く見つけることを目的にしている。

## この記事を読むべき理由
日本でもCopilotやChatGPTを開発現場で使うチームが急増しています。自動生成コードは一見動くが保守性や安全性で課題を残すことが多く、そうした“隠れた欠陥”をCI段階で自動検出できれば、手戻り・セキュリティリスクを大幅に減らせます。

## 詳細解説
- 検出対象（分かりやすく分類）
  - プレースホルダ（TODO / FIXME / HACK / XXX）
  - 保留・先送り表現（"for now", "temporary fix"）
  - 不確かさを示すヘッジ（"should work", "hopefully"）
  - スタブ／ダミー（空関数、todo!()、固定のダミーデータ）
  - ノイズな冗長コメント（意味の薄いコメント）
- 設計思想
  - Zero Trust：AI生成コードは「疑って検証」を前提にする。意図と実装のギャップ（Intent != Implementation）を重視。
  - 速度重視：数ミリ秒で検出できることを重視し、即時フィードバックを可能にしている。
  - MECE（相互排他的かつ網羅的）：既存の静的解析（ESLint/Clippy等）とはターゲットを分け、重複を避ける。
- 実装のポイント
  - tree-sitter を使ったAST解析＋正規表現のハイブリッド。言語ごとにAST解析かRegexのみを選べる。
  - 「ゼロ誤検知」ポリシーをコアに、検出対象の厳しさはProfile（core / standard / strict）で調整。
- 性能・スケーリング（リポジトリ公開ベンチマークの抜粋）
  - 言語別（ASTモード）例：Python 4.0 ms（416 KiB/s）、Go 1.3 ms（1.2 MiB/s）
  - Regexモードはさらに高速（Python 0.47 ms）
  - スケール例：1,000行 = 10.5 ms、50,000行 = 392 ms（ラップトップ機での計測）
- インテグレーション
  - CLIでローカル実行、JSON出力対応でCI連携しやすい
  - GitHub Actionsサンプルがあり、CIでブロック条件にできる
- 配布とカスタマイズ
  - バイナリ配布（npm, Homebrew, PowerShell経由）やcargoでのビルドが可能
  - antislop.tomlで独自パターンを追加してプロジェクトに合わせて調整できる
  - モジュラーで言語ごとの機能をオン／オフしてバイナリサイズを最適化可能

使用例（ローカル実行・JSON出力）
```bash
antislop --profile antislop-standard src/ api/
antislop --json > antislop-report.json
```

サンプルGitHub Actions（抜粋）
```yaml
jobs:
  antislop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install AntiSlop
        run: curl -sSf https://raw.githubusercontent.com/skew202/antislop/main/install.sh | sh
      - name: Run Scan
        run: antislop --profile antislop-standard .
```

設定例（antislop.tomlの一部）
```toml
file_extensions = [ ".py", ".rs", ".js", ".ts" ]

[[patterns]]
regex = "(?i)TODO:"
severity = "medium"
message = "Placeholder comment found"
category = "placeholder"
```

## 実践ポイント
- まずは「standard」プロファイルで日次スキャンを開始：誤検知を避けつつ、保留表現やダミー値を捕捉できる。
- CIでのゲート化は「core（最小）→standard（推奨）→strict（監査）」の段階導入を推奨。まずはブロック条件を厳しくしすぎない。
- antislop.tomlでプロジェクト固有のパターン（社内TODOタグ、モックデータの表現）を追加して精度向上。
- 大規模レポジトリやモノレポではRegexモードや言語選択機能を使いバイナリサイズ＆速度を最適化。
- 日本語コメントや社内慣習に合わせて正規表現を調整すること。AIが生成する表現はローカル文化や日本語特有の曖昧表現も含むため、カスタムルールを作る価値が高い。

短く結論：AI生成コードを単に信頼せず「Zero Trust」で検査する仕組みをCIに組み込めば、バグや保守コストを未然に減らせます。AntiSlopはその最初の一歩として実用的なツールです。
