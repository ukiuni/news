---
  layout: post
  title: "Show HN: Muad-Dib – Open-source tool to detect npm supply-chain attacks - Muad‑Dib：npmサプライチェーン攻撃検出ツール（オープンソース）"
  date: 2026-01-02T16:03:44.913Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/DNSZLSK/muad-dib"
  source_title: "GitHub - DNSZLSK/muad-dib: Supply-chain threat detection &amp; response for npm. Detects Shai-Hulud, typosquatting, credential theft, and more."
  source_id: 474146541
  excerpt: "Muad‑Dib：npmのサプライチェーン攻撃を検出し対応手順まで提示"
  image: "https://opengraph.githubassets.com/22f1062a2c6c608691a39f24445309047343e300a10f2a7d2cbef41061ccf4a2/DNSZLSK/muad-dib"
---

# Show HN: Muad-Dib – Open-source tool to detect npm supply-chain attacks - Muad‑Dib：npmサプライチェーン攻撃検出ツール（オープンソース）
魅力的な見出し: npmの「根本治療」──Shai‑Huludやタイポスクワットまで検出し、対処手順まで示すオープンソーススキャナー

## 要約
Muad‑Dibはnpm向けのオープンソースなサプライチェーン脅威検出・対応ツールで、AST解析やデータフロー分析、タイポスクワット検出、IOCマッチング、MITRE ATT&CKマッピング、プレイブック出力などを備え、CLI/VS Code/CI連携で現場の対応を支援する。

## この記事を読むべき理由
npm依存のプロジェクトは日本でも極めて多く、サプライチェーン攻撃は一度侵入すると広範囲に被害が及ぶ。検出だけで終わらない「検出→優先度付け→対応手順」をワンストップで提供する点が実務目線で有益だから。

## 詳細解説
- 検出技術の要点
  - AST解析（acornベース）により、怪しいAPI呼び出しやスクリプトパターンを抽出。
  - データフロー分析で「資格情報読み取り（.npmrc / env / readFileSync）」→「ネットワーク送信（fetch等）」の流れを追跡し、機密漏洩の兆候を検出（高危険度）。
  - タイポスクワット検出はレーベンシュタイン距離などを使い、lodash→lodahsのような類似名パッケージを警告。
  - IOC（YAML）データベースで既知のマルウェア/キャンペーン（例：Shai‑Hulud / event-stream / protestware）と照合。
  - 検出結果にMITRE ATT&CKタグを付与し、影響技術や参考情報、対応プレイブックまで提示。

- 出力・連携
  - CLI出力（リスクスコア0–100、詳細説明モード）、JSON/HTML、SARIF（GitHub Code Scanning連携）をサポート。
  - Discord/Slack webhook送信、VS Code拡張でエディタ内スキャン、デーモン/ウォッチモードでnpm install時の自動スキャン。
  - CI例：GitHub Actionsでmuaddib scan . --sarif results.sarifを実行し、Code Scanningに結果を投げるワークフローを想定。

- 運用面
  - スコアとseverity（critical/high/medium/low）でトリアージ可能。--fail-onオプションでCIの阻止条件を設定。
  - IOCはiocs/のYAMLで容易に拡張可能。コミュニティでのIOCs共有を前提とする設計。

## 実践ポイント
- まずローカルで試す（推奨：グローバルインストール）
```bash
# bash
npm install -g muaddib-scanner
muaddib scan .
muaddib scan . --explain
muaddib scan . --sarif results.sarif
```
- CI導入（GitHub Actions）例：成果物をSARIFでアップロードするとSecurity > Code scanningに表示される。重要度が高いものは--fail-on highでビルド失敗に。
- エディタ統合：vscode-extensionフォルダを開いてF5で拡張機能を試し、開発中に自動スキャンを有効化。
- リアルタイム監視：muaddib daemon/watchでnpm install時に自動検査。サプライチェーン感染の早期発見に有効。
- 日本向け運用Tips：
  - Slackが主流のチームにはWebhook連携を設定してアラートを流す（Discord/Slack両対応）。
  - SARIF→GitHub Securityのフローは、既存のセキュリティレビュー運用に自然に組み込みやすい。
  - ローカルで出たプレイブックを翻訳・社内テンプレ化して対応手順を統一する。

短く言うと、Muad‑Dibは「検出して終わり」ではなく「検出→優先度付け→対応手順の提示→CI/エディタ連携」で現場運用に落とせるツールチェーンを提供する。まずローカルでスキャンを回し、CI連携とWebhookアラートを整えることが初動として効果的。
