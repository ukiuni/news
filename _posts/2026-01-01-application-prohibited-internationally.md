---
layout: post
title: "Application Prohibited Internationally - 国際的に禁止されたアプリケーション"
date: 2026-01-01T01:39:16.170Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://tuckersiemens.com/posts/application-prohibited-internationally/"
source_title: "Application Prohibited Internationally"
source_id: 474007442
excerpt: "ロケール依存でRFC1123表記が崩れpt-PT環境で500エラー発生"
---

# Application Prohibited Internationally - 国際的に禁止されたアプリケーション
なぜ「ロケールの一文字」がサーバー500を呼ぶのか？ プロダクションで起きたDateTimeの国際化ミステリー

## 要約
コマンドラインツールが一部ユーザー（ポルトガル）の環境でだけ500エラーを返す原因は、Accept-Language → スレッドのCurrentCulture → RFC1123文字列生成 → 内部APIの InvariantCulture での ParseExact という「文化依存の食い違い」だった。

## この記事を読むべき理由
日本語ロケールやグローバルユーザーを抱えるサービスでも同様の落とし穴は現実に起こる。小さなロケール依存がマイクロサービス間で壊滅的なバグになる実例を学び、現場で使える対策を手に入れよう。

## 詳細解説
- 事象: ユーザー（pt-PT）がツールを2回目以降実行すると失敗し、キャッシュ削除で回避できると報告。ログに TF400898: An Internal Error Occurred。
- 調査で判明した流れ:
  1. APIクライアントライブラリがローカルの CultureInfo.CurrentUICulture を Accept-Language として送信していた。
  2. サーバ側の「public API」が RFC1123 形式で日時を文字列化して内部APIに渡す実装だったが、DateTime.ToString(RFC1123Pattern) として明示的なカルチャを渡していなかった。
  3. 別箇所で Accept-Language を基に Thread.CurrentThread.CurrentCulture を設定しており、結果として ToString が pt-PT ロケールの曜日/月略称（例: "sáb, 26 out 2024 18:01:42 GMT"）を出力。
  4. 内部APIは受け取った文字列を CultureInfo.InvariantCulture で DateTime.ParseExact(..., "R", InvariantCulture) しており、英語ベースの RFC1123 期待文字列と合わず FormatException → 500 エラー。
- キーポイント: RFC1123 の形式は英語略称前提（Mon, Jan ...）。送信側と受信側の「カルチャの一貫性」が欠けると致命的。

## 実践ポイント
- すぐ直せるパッチ（public API 側）:
```csharp
// 問題の原因になりやすい（Thread.CurrentThread.CurrentCulture の影響を受ける）
var nowBad = DateTime.UtcNow.ToString(RFC1123Pattern);

// 修正：明示的に InvariantCulture を使って安定した英語ベースの RFC1123 を生成
var nowGood = DateTime.UtcNow.ToString(RFC1123Pattern, CultureInfo.InvariantCulture);
```
- 他の対策
  - 受け側（内部API）も堅牢化する: 受信フォーマットを制限せず、可能なら ISO 8601 / RFC3339 を共通仕様に変更する。
  - ランタイムでスレッド全体のカルチャを Accept-Language で変更する設計は副作用が大きい。UI表示用に局所的にカルチャを適用するか、明示的なフォーマッタを使う。
  - 静的解析/リンターを導入: CA1304 / CA1305 などで CultureInfo を明示する習慣を促す。
  - テスト: 非英語ロケール（ja-JP, pt-PT, fr-FR など）でのエンドツーエンド/API結合テストを自動化する。
- 日本市場への注意点: ja-JP でも曜日や月の表現が異なるため、海外/国内混在環境で同様の問題が再現し得る。多言語サービスや海外拠点との連携があるプロダクトは要チェック。

## 引用元
- タイトル: Application Prohibited Internationally
- URL: https://tuckersiemens.com/posts/application-prohibited-internationally/
