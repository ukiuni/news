---
layout: post
title: "Microsoft Has Killed Widgets Six Times. Here's Why They Keep Coming Back. - Microsoftがウィジェットを6回葬った理由 — なぜ何度も戻ってくるのか"
date: 2026-02-04T09:27:10.605Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://xakpc.dev/windows-widgets/history/"
source_title: "Microsoft Has Killed Widgets Six Times. Here&#39;s Why They Keep Coming Back."
source_id: 409615733
excerpt: "六度の廃止から導かれた設計で、より安全で実用的に甦るウィジェット"
image: "https://xakpc.dev/resources/widgets-history/og.png"
---

# Microsoft Has Killed Widgets Six Times. Here's Why They Keep Coming Back. - Microsoftがウィジェットを6回葬った理由 — なぜ何度も戻ってくるのか
ウィジェットの“失敗の教訓”が今の設計を決めた理由 — 30年にわたるWindowsウィジェットの興亡史

## 要約
Microsoftは1997年以降、同じ「常時情報表示」の問題を何度も実装→撤回してきた。その都度の失敗（性能・画面占有・セキュリティ・エンゲージメント・プライバシー）が、現在の安全で宣言型なウィジェット設計を形作っている。

## この記事を読むべき理由
日本のデスクトップ／ノート中心の利用実態（狭い画面・業務効率重視・プライバシー敏感）では、過去の失敗から学んだ設計判断がそのまま実務的な指針になる。ウィジェット開発や導入を考える開発者・IT担当者は必読。

## 詳細解説
- Push Era (1997): Internet ExplorerのTridentをexplorer.exeに組み込み、Active DesktopでHTMLを壁紙に常駐。CDF（XML）でコンテンツ同期。結果は計算資源の枯渇とexplorerのクラッシュ→原因：性能。
- Glass Era (2007): VistaのAero Sidebar。.gadgetはHTML/CSS/JSのZIPで簡単作成だが、150px程度の常設領域が画面を圧迫し、メモリリークで実用性低下→原因：画面スペース。
- Free Era (2009–2012): Windows 7でウィジェットを自由に浮かべられるようにしたが、.gadgetはローカル権限で実行（サンドボックスなし）。Black Hat 2012での攻撃チェーン（HTTP改ざん→JS注入→ActiveX実行）で致命的に破綻→原因：セキュリティ。
- Metro Era (2012): Live TilesはWNS経由のXMLテンプレートで描画のみ（実行コードなし）、バッテリに優しいがフルスクリーンや読み取り専用で生産性を阻害→原因：エンゲージメント（対話性不足）。
- Interlude (2015–2021): Cortanaカードは深い個人データアクセスで便利だがプライバシー懸念、News & Interestsは意図しない開閉でユーザーを不快にした→原因：プライバシー／誤動作の妨害。
- Board Era (2021–2024): Windows 11のWidget BoardはEdge WebView2上でAdaptive Cards（宣言的JSON）を採用し、コード実行を避ける設計に。だがWebView2の重さと強制MSNフィードで批判を受け、EUの規制（DMA）で再設計を迫られた。
- 現状の教訓: 今日のアーキテクチャ（宣言的フォーマット、ネイティブレンダラ、オーバーレイ表示）は過去の“傷”（scar tissue）による制約そのもの。各制約は恣意的でなく具体的な事故の結果。

主要技術要素（要点）
- Trident統合→explorer.exe崩壊リスク
- .gadget = ZIP(HTML/JS) → サンドボックス欠如
- Black Hat攻撃例：HTTP改ざん→ActiveX経由で任意実行
- Live Tiles/WNS：プッシュ通知でXMLテンプレート描画（宣言的）
- Adaptive Cards：JSONでUIを記述、実行コード不可
- Widget Board：WebView2レンダリング、IWidgetProvider COM、PWAマニフェスト経由の参入経路

## 実践ポイント
- ウィジェットを作るなら宣言型（Adaptive Cards）を第一選択にし、実行コードを避ける。
- メモリ/CPU負荷を最優先で計測。低スペック機での挙動を必ず確認する。
- 画面占有を最小化し、オーバーレイや非常駐表示を採用する（常設領域は嫌われる）。
- インタラクティブ性は重要：読み取り専用より簡単な操作（チェック、再生）を提供する。
- プライバシー設計を明確化し、動作は意図的に（ホバーで誤開閉しないなど）実装する。
- WebベースならPWA経由での実装が参入障壁が低いが、WebViewのリソース負荷に注意する。
- EUの規制はグローバル影響が大きい。日本向けでも仕様変更の波を想定しておく。

短く言えば：ウィジェットは「便利だが危険」だった。今は「宣言的・サンドボックス・意図的」になり、過去の失敗が安全で実用的な道筋を作っている。日本の現場では、まず性能・画面占有・プライバシーを満たすことが採用の鍵。
