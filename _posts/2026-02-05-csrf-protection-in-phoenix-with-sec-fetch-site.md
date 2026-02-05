---
layout: post
title: "CSRF protection in Phoenix with Sec-Fetch-Site - PhoenixでSec-Fetch-Siteを使ったCSRF対策"
date: 2026-02-05T16:11:37.624Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mediremi.com/writing/phoenix-csrf-protection-with-sec-fetch-site/"
source_title: "CSRF protection in Phoenix with Sec-Fetch-Site | Médi-Rémi Hashim"
source_id: 815203848
excerpt: "Sec-Fetch-SiteでPhoenixのCSRFをトークン不要にして簡潔に防御する手順"
---

# CSRF protection in Phoenix with Sec-Fetch-Site - PhoenixでSec-Fetch-Siteを使ったCSRF対策
PhoenixでCSRFトークンを置き換える——Sec-Fetch-Siteでシンプルに守る方法

## 要約
ブラウザが送るSec-Fetch-Site/Originヘッダーを使い、PhoenixアプリでCSRFトークンを不要にするPlug実装を紹介。安全なHTTPメソッドはそのまま許可し、クロスオリジンの危険なリクエストだけを拒否するアプローチ。

## この記事を読むべき理由
CSRFトークンは確実だが実装・運用で面倒（全リクエストへの埋め込み、BREACH対策、セッション更新で無効化等）。日本でもSPAやモバイル、CDN経由の構成が増える中、ヘッダーで簡潔に防御できればフロント実装が楽になり、脆弱性対策の負担を減らせます。

## 詳細解説
- 背景：従来はCSRFトークン（metaタグやヘッダー）で「同一サイト」を担保していたが、トークンの配布／更新コストやBREACH対策が煩雑。
- ブラウザの進化：2023以降、主要ブラウザはすべてのリクエストにSec-Fetch-Siteを付与可能になった（値は same-origin / same-site / cross-site / none）。これによりサーバー側で簡潔に「クロスオリジンかどうか」を判定できる。
- 実装方針（元記事のPlugのロジック）：
  - 安全メソッド（GET, HEAD, OPTIONS）は常に許可。
  - Sec-Fetch-Site が存在する場合：
    - same-origin, none を許可。
    - same-site, cross-site は拒否。
  - Sec-Fetch-Site がない場合は Origin ヘッダーを確認：
    - Origin が無ければ「同一オリジンまたはブラウザ外リクエスト」とみなして許可（例：curlやサーバ間通信）。
    - Origin が存在する場合は Host（とポート）と比較し一致すれば許可、そうでなければ拒否。null origin は拒否。
  - 特定パス（bypass_patterns）は例外として許可できる（例えば公開APIや外部 webhook）。
- テスト：元記事はGoのv1.25 CrossOriginProtectionテスト群を参考にしたExUnitテストを用意しており、各ケース（ヘッダー有無、値、メソッド、バイパスパス）を検証している。
- 注意点：
  - ブラウザがヘッダーを送らないケースやプロキシ等で改変されるケース、古いクライアントにはフォールバックや確認が必要。
  - 非ブラウザクライアント（APIクライアントなど）はOrigin/Sec-Fetch-Siteを送らないため許可される設計だが、意図しない許可を避けたい場合は別途認証整備を。

## 実践ポイント
- ルーターでCSRFトークンPlugを置き換える：
```elixir
# elixir
# router.ex
- plug :protect_from_forgery
+ plug MyAppWeb.CrossOriginProtection
```
- レイアウトやJSでcsrf-token参照を削除／更新：
```elixir
# elixir
# layout.eex から以下を削除
- <meta name="csrf-token" content={get_csrf_token()} />
```
- セッション再生成コードからdelete_csrf_tokenを削除：
```elixir
# elixir
defp renew_session(conn) do
  # delete_csrf_token()
  conn |> configure_session(renew: true) |> clear_session()
end
```
- LiveView/WebSocket設定：Originでチェックし、CSRFチェックはオフに
```elixir
# elixir
socket "/live", Phoenix.LiveView.Socket,
  websocket: [check_origin: true, check_csrf: false, connect_info: [session: @session_options]]
```
- 導入後の確認リスト：
  - ブラウザ（Chrome/Firefox/Safari）でSec-Fetch-SiteとOriginの送信を検証。
  - APIや外部クライアントが正しく動くか（必要ならトークンを維持）。
  - バイパス対象パスを明示的に設定して意図しない遮断を防ぐ。
  - 影響範囲を把握するためにユニット/統合テストを追加。

この手法は「トークン管理の複雑さを減らしつつ、ブラウザ経由の悪意あるクロスオリジン操作をブロックする」現代的な選択肢です。導入前に利用するクライアント環境（プロキシや古いブラウザ）を必ず確認してください。
