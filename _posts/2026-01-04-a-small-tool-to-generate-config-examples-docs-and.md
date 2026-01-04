---
  layout: post
  title: "A small tool to generate config examples, docs, and JSON Schema from one definition - 1つの定義から設定例・ドキュメント・JSON Schemaを生成する小さなツール"
  date: 2026-01-04T16:27:27.025Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/abstractrenderblocks/arb"
  source_title: "GitHub - abstractrenderblocks/arb: Deterministic recursive text compiler for structured generation. One source of truth. Many outputs."
  source_id: 471228640
  excerpt: "単一YAMLで設定例・ドキュメント・JSON Schemaを一貫生成し整合性を保証。"
  image: "https://opengraph.githubassets.com/f34daaa0d95123dae27d0ec18f0b9505a5e256dcd54532295b4e6b9455f80a46/abstractrenderblocks/arb"
---

# A small tool to generate config examples, docs, and JSON Schema from one definition - 1つの定義から設定例・ドキュメント・JSON Schemaを生成する小さなツール
驚くほど安全で再現性のある「一元定義→多出力」コンパイラ：arbがもたらすドキュメントと設定運用の未来

## 要約
arbはYAMLで定義した単一の「ソース・オブ・トゥルース」から、例示設定ファイル、ドキュメント、JSON Schema、CLIコードなどを再現性高く生成する決定論的コンパイラ。テンプレートのロジック混入や部分生成を防ぐ設計が特徴。

## この記事を読むべき理由
設定やドキュメントの整合性がプロダクト品質に直結する日本企業・チームにとって、手作業での同期ズレや無秩序なテンプレート実装を根本から防げる実運用アイデアを得られる。

## 詳細解説
- コア概念
  - 入力はバリデート済みのYAML。テンプレートパッケージ（packages）が出力ルールを持つ。
  - arbは「テンプレートエンジン」やスクリプトではなく、厳格なコンパイラ。出力の再現性・安全性を重視する。

- 主要保証
  - 決定論的出力：同じ入力は常に同じバイト列を生成。
  - スキーマファースト検証：テンプレート実行前に入力データを検証。エラーは早期に検出。
  - コード実行不可：テンプレートから任意コードやシステムコマンドは呼べないため安全。
  - 再帰と参照の安全性：インクルードは循環検査と深さ／サイズ上限で保護。
  - フェイルファスト：失敗時は部分出力を残さない。既存出力は完全成功時のみ上書き。

- 付属パッケージ例
  - docs-suite：単一YAMLからREADME、overview、quickstart、FAQ、manページ、MkDocs設定など一式を生成。ドキュメント運用の「差分発生源」を排除。
  - cli-rust：YAML定義からclapベースのRust CLIのコマンドツリー・助け表示・ディスパッチスキャフォールディングを生成。コードジェネレータ用途の実例。
  - config-schema：設定仕様から config.example.yaml、docs/config.md、config.schema.json（JSON Schema）を同時生成。ヒューマン向け例、参照ドキュメント、機械検証定義を同期保守。

- 実装スタック
  - Rust製のCLI（crates/arb-cli）。設計はv1で機能を限定し、正確性と安全性を最優先。

## 日本市場との関連性
- 大企業やFinTech、産業向けで多い「複数プロダクトに跨る設定」「監査向けドキュメント整備」「セキュリティポリシー遵守」に直結。設定ミスで起こる運用障害や監査指摘リスクを低減する。
- 多言語化／ローカライズの際も「一つの仕様から派生する出力」を使えば翻訳差分管理が容易に。CIに組み込んで生成→テスト→配布を自動化すれば品質担保がしやすい。

## 実践ポイント
- 試す手順（リポジトリからビルド）
```bash
# リポジトリをクローンしてビルド
git clone https://github.com/AbstractRenderBlocks/arb.git
cd arb
cargo install --path crates/arb-cli
```
- 60秒でハンズオン
```bash
mkdir arb-demo && cd arb-demo
# サンプルデータをコピー（リポジトリ相対）
cp ../packages/docs-suite/examples/data.example1.yaml data.yaml
arb compile --package ../packages/docs-suite --data data.yaml --out out
# 出力を確認
ls out
```
- CIへの組み込み案
  - プルリクで arb validate を実行してスキーマ準拠を必須化。
  - masterマージ時に arb compile → 生成物をアーティファクトとして保存／デプロイ。
- 運用上の注意
  - パッケージのテンプレートはロジックを持たせない設計方針に従う。複雑な振る舞いは入力スキーマで表現する。
  - 生成物は自動化されたレビューと差分チェックで運用し、手動編集を避ける。

このツールは「一元仕様から確実に多様な成果物を作る」ことを目指している。ドキュメントと設定の整合性をコード化して運用コストを下げたいチームは、まずパッケージ例（config-schema, docs-suite）を触ってみると導入可否の判断が早まる。
