---
layout: post
title: "Web Security: The Modern Browser Model - ウェブセキュリティ：モダンブラウザモデル"
date: 2026-02-03T04:39:10.071Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nemorize.com/roadmaps/web-security-the-modern-browser-model"
source_title: "Web Security: The Modern Browser Model - Learning Roadmap | Nemorize"
source_id: 410586256
excerpt: "Same‑Origin/CORS/CSP/COOPなどで守る最新ブラウザ防御と実践対策"
image: "https://nemorize.com/favicon.png"
---

# Web Security: The Modern Browser Model - ウェブセキュリティ：モダンブラウザモデル
今すぐ押さえたい！ブラウザが守る最新のWebセキュリティの全体像

## 要約
モダンブラウザはSame‑Origin Policy、CORS、HTTPS、CSP、Cookie制御、リソース分離（COOP/COEP/CORP）など複数のレイヤで攻撃を防ぎ、さらにSpectre緩和やTrusted Typesで高度な脆弱性にも対処します。本記事はそれらの原理と実務で使える対策を分かりやすくまとめます。

## この記事を読むべき理由
日本のWebサービス（決済、SaaS、広告配信、SNSなど）はクロスサイト攻撃やプライバシー規制の影響を直接受けます。ブラウザ側の防御モデルを理解すれば、安全設計・実装ミスの発見と対策が迅速にでき、ユーザー信頼と法令順守に直結します。

## 詳細解説
- Same‑Origin Policy（SOP）
  - originはスキーム（http/https）、ホスト、ポートで定義され、DOMや一部のリソースの読み書きを隔離する基本ルールです。SOPの例外や実装差に注意。

- Cross‑Origin Read Blocking（CORB）
  - ブラウザが機密レスポンスをクロスオリジンで誤って公開するのを防ぐ軽量フィルタ。画像やテキストの誤読み込みを遮断します。

- HTTPS・トランスポートセキュリティ
  - HTTPS必須。HSTSで強制的にHTTPSへリダイレクト、証明書ピンニングは過信禁物（運用負担）。Mixed Contentはブラウザがブロックまたは制限。

- Cross‑Origin Resource Sharing（CORS）
  - サーバー側ヘッダで安全にクロスオリジンアクセスを許可する仕組み。Simple vs Preflight（OPTIONS）や、Credentials（Cookie/認証情報）を使う際の「ワイルドカード＋認証禁止」などの落とし穴に注意。

- リソース隔離（COOP/COEP/CORP）
  - Cross‑Origin‑Opener‑Policy（COOP）とCross‑Origin‑Embedder‑Policy（COEP）でページをクロスオリジンから隔離し、SharedArrayBufferやSpectre緩和を安全に使える環境を作ります。CORPは埋め込み資源のポリシー制御。

- コンテンツセキュリティポリシー（CSP）
  - スクリプト・スタイル・メディア等の読み込み先を白リスト化。報告（report-uri/report-to）で侵入試行を検知。Strictなポリシーは互換性問題が出るため段階的導入が有効。

- Trusted Types
  - DOM XSS（innerHTML等）を減らすためのAPI。文字列→危険なDOMに変換する際に開発側で明示的な許可を与えるモデル。

- CookieセキュリティとPartitioning
  - SameSite（Lax/Strict/None）でCSRFリスクを低減。Noneを使う場合はSecureが必須。__Secure- / __Host- プレフィックスで設定の厳格化。CHIPSやPartitioned Cookiesはサードパーティ追跡の代替・制限に関係。

- 権限・Feature Policy（Permissions‑Policy）
  - カメラやマイク、サブリソースの機能使用をページやiframe単位で制御。最小権限原則を適用。

- Spectre対策とSharedArrayBuffer
  - サイドチャネル攻撃対策のためブラウザが追加の分離を要求。COOP/COEPを満たすことで一部機能が利用可能に。

## 実践ポイント
- サイト全体でHTTPSを強制し、HSTSを設定する（プリロード検討）。
- 認証系Cookieは Secure + SameSite=Lax/Strict、可能なら __Host- または __Secure- を付与。
- CORSは最小許可に留める。Credentialsを使うなら Access‑Control‑Allow‑Origin にワイルドカードを使わない。
- CSPはまず report‑only で導入し、段階的に厳格化していく。CSPレポートを集約して解析する。
- 外部リソースはCORP/COEPを活用して分離し、SharedArrayBufferなどの必要機能は明示的に許可する。
- DOM操作の危険箇所にはTrusted Typesを適用し、テンプレートやライブラリで安全化する。
- 権限はPermissions‑Policyで絞る。iframeの機能委譲は最小限に。
- ブラウザDevToolsでCSP/CORS/ネットワークの挙動を常時チェックし、セキュリティテスト（SAST/DAST）をCIに組み込む。
- 日本の広告・解析事業者は第三者Cookieの制限に備え、サーバーサイド集計やファーストパーティ同意フローを検討する。

以上を踏まえれば、ブラウザ側の防御機能を活用して堅牢でプライバシー配慮したWebサービス運用が可能になります。
