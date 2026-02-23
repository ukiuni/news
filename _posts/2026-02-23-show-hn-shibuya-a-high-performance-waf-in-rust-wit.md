---
layout: post
title: "Show HN: Shibuya – A High-Performance WAF in Rust with eBPF and ML Engine - 渋谷 — Rust製 eBPF＋ML エンジン搭載の高性能WAF"
date: 2026-02-23T20:26:16.133Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://ghostklan.com/shibuya.html"
source_title: "Show HN: Shibuya – A High-Performance WAF in Rust with eBPF and ML Engine"
source_id: 47126656
excerpt: "eBPFでカーネル遮断、MLとWASM拡張を備えたRust製WAF"
---

# Show HN: Shibuya – A High-Performance WAF in Rust with eBPF and ML Engine - 渋谷 — Rust製 eBPF＋ML エンジン搭載の高性能WAF

渋谷が“カーネルで止める”WAF革命を起こす——クラウド頼みを脱する自前防御の選択肢

## 要約
Rustで書かれたオープンソースWAF「Shibuya」は、eBPF/XDPによるカーネルレベルの即時ブロック、ONNXベースのML（IsolationForest＋RandomForest）＋SHAP風の説明可能性、615以上のOWASP CRS互換ルール、WASMプラグイン、Shadow/Replayによる本番テスト環境などを統合し、低レイテンシかつ実運用向けの機能セットを提供します。

## この記事を読むべき理由
日本の開発／運用チームが自社環境へ導入できる“自前で高精度かつ低遅延なWAF”の実装例として実務に直結。特にオンプレ／自社クラウド運用やAPI保護、GraphQL対応を検討する企業には即戦力の知見源です。

## 詳細解説
- 基盤と性能  
  - Rust実装でメモリ安全かつ高速。P99レイテンシは<5ms、eBPF/XDPでのパケットドロップは理論上~1µs。Linux専用のカーネルフックにより「アプリに到達する前」に悪性トラフィックを消せる点が最大の差別化。
- MLエンジンと説明可能性  
  - ONNXでIsolationForest（異常検知）とRandomForest（10クラス分類：SQLi/XSS/RCE等）を並列推論。SHAP風の上位特徴表示で「なぜ検出したか」を可視化し、人のフィードバックで学習ループを回せる。
- ルールと互換性  
  - ModSecurity互換のSecRuleパーサーで615+のOWASP CRSをネイティブにサポート。ルールのホットリロードやアノマリースコアリング、ReDoS対策など運用向け機能を備える。
- 拡張性（WASM）  
  - 任意言語→WASMでプラグインを作成可能。サンドボックス、メモリ／実行時間／燃料制限で安全に拡張できる。
- テスト運用と可視化  
  - Shadowモード（ブロックせずログのみ）とトラフィックリプレイを組み合わせ、実トラフィックで新ルールを安全に検証。36ページのSvelteKitダッシュボードでリアルタイム分析・リクエストインスペクタを提供。
- API／GraphQL保護  
  - OpenAPI 3.xから自動でポジティブセキュリティルールを生成。GraphQLは深さ・複雑度・エイリアス数制限など専用チェックを装備。
- 運用・エンタープライズ機能  
  - マルチテナンシー、RBAC、LDAP/OAuth連携、Federated Learning、Post‑Quantum TLS、TPMアテステーション、SBOMなどを搭載し、自己ホスト前提で企業要件に応える。
- 付加機能  
  - 「Ashigaru」攻撃ラボ（6つの脆弱サービス＋自動レッドチーム）同梱で実攻撃検証が手元で可能。NLPポリシーで自然言語からルール生成、脆弱性スキャンと連携して30秒で仮想パッチを用意する仕組みも謳われている。

## 実践ポイント
- まずは検証環境で動かす：Linux環境＋eBPFサポートカーネルでlite版をクローン→setup→start。Shadowモードで既存トラフィックにかけて誤検知を確認。  
- OpenAPIやGraphQLが中心なら仕様を取り込んで自動ルールを生成し、まずはポジティブセキュリティで守る。  
- eBPFは強力だがLinux専用なので、混在環境では段階的導入（ユーザースペース→eBPF有効化）を推奨。  
- カスタム検出が必要ならWASMでプラグインを作成し、ダッシュボードのMLモニタでフィードバックを与える運用を組む。  
- 本番投入前は必ずリプレイで差分レポートを取り、Shadowで一定期間運用してからブロックに移行する。

導入を検討する日本の現場にとって、Shibuyaは「自社で運用・拡張できる次世代WAF」の具体例です。興味があるならまずはリポジトリを触ってShadowモードから始めてみてください。
