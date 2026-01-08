---
  layout: post
  title: "JavaScript engines zoo – Compare every JavaScript engine - JavaScript エンジン図鑑"
  date: 2026-01-04T13:08:21.943Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://zoo.js.org/"
  source_title: "JavaScript engines zoo"
  source_id: 46486978
  excerpt: "実機ベンチでJSエンジンの速度・バイナリ・ES対応を比較して最適候補を提示"
---

# JavaScript engines zoo – Compare every JavaScript engine - JavaScript エンジン図鑑
目を奪われる実機ベンチで一目瞭然：次のJSランタイム選びがこれ1つで分かる

## 要約
実機（amd64 i9-10900K、arm64 Mac M4）で多種のJavaScriptエンジンを比較し、スコア・バイナリサイズ・言語実装・JIT有無・ESサポートなどを一覧化した総合カタログです。

## この記事を読むべき理由
エンジン選定は性能だけでなくバイナリサイズ、ES互換性、ライセンス、JITの有無で導入可否が変わります。日本のプロダクト（サーバレスコスト最適化、Apple Silicon対応、組込み/IoT用途、セキュリティ制約）では特に有益な比較情報です。

## 詳細解説
- 対象と環境: amd64（Intel i9-10900K 3.7–5.3GHz、Linux VM）と arm64（Mac M4 4.5GHz、Linux VM）でベンチを実行。複数のハードでの挙動差を可視化しています。
- 表示される主要指標:
  - Engine / Score: ベンチ総合スコア（比較の目安）。
  - Binary: 実行ファイルサイズ（組込み・コンテナ最適化で重要）。
  - LOC / Language: 実装言語とコード量（保守性や貢献しやすさの指標）。
  - JIT: JITの有無（パフォーマンスとDeterminismのトレードオフ）。
  - Years / Target: 開発年数と想定用途（ブラウザ、サーバ、組込み等）。
  - ES1-5 / ES6 / ES2016+: ECMAScriptサポート状況（互換性チェックに必須）。
  - Stars / Contributors / Org / License: OSSコミュニティの成熟度と採用リスク評価。
- フィルタ機能: JITlessのみ、特定のベンチセット（v8-v7）などで絞り込みが可能。これにより「セキュアで予測可能な実行環境を優先」や「最新ES機能重視」などの観点で選べます。
- 解釈の注意点:
  - スコアは相対比較の補助であり、実プロダクトのワークロードでの計測が最終判断。
  - CPU・OS差で結果が変わるため、自社環境での再現ベンチは必須。
  - ライセンスやメンテナンス状況（contributors数）は長期運用コストに直結。

## 実践ポイント
- まずターゲット環境（サーバ/組込み/ブラウザ/Apple Silicon）を決め、該当列でフィルタ。
- 組込みやコンテナ最適化ならBinaryサイズとLicenseを最優先に比較。
- セキュリティや決定論が重要なら「JITless」フィルタで候補を絞る。
- 最新ES機能を使う場合はES2016+のサポート状況を確認し、必要ならポリフィルやトランスパイラを併用。
- 候補エンジンは自社の実ワークロードで再ベンチ（同一ハード/同一入力）して最終決定。
- OSS貢献やフォークを検討する場合は、Contributors/Stars/Orgを見て活発度を評価。

短時間で候補の当たりを付け、最終判断は自社環境での再現テスト——JavaScript engines zooはその最初の「可視化」として非常に有効です。
