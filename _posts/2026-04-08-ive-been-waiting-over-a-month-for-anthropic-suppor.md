---
layout: post
title: "I've been waiting over a month for Anthropic support to respond - Anthropicのサポートからの返答を1か月以上待っている"
date: 2026-04-08T20:22:05.314Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://nickvecchioni.github.io/thoughts/2026/04/08/anthropic-support-doesnt-exist/"
source_title: "I’ve been waiting over a month for Anthropic support to respond to my billing issue | Nick’s Thoughts"
source_id: 47693679
excerpt: "AnthropicのAI応答のみで誤請求約$180が放置、1か月以上未対応の実態"
---

# I've been waiting over a month for Anthropic support to respond - Anthropicのサポートからの返答を1か月以上待っている
魅力的タイトル: 「$180が勝手に請求されたら？Anthropicの“AIだけ”サポートが招いた顧客対応の穴」

## 要約
Claude Max契約者が3月初旬に約$180の「Extra Usage」請求を受け、証拠を添えて3月7日に問い合わせたが、即時応答はAIチャットボットのみで以降1か月以上人間からの対応が来ていない。類似問題は他ユーザーからも報告されている。

## この記事を読むべき理由
クラウドAIを業務利用する日本の開発者・企業にとって、誤請求や可観測性（billing/usage transparency）は直接コストと信頼に関わる。AIベースのセルフサービスが主流化する中で「人間によるエスカレーションの欠如」がどれだけ致命的かを示す実例になるから。

## 詳細解説
- 何が起きたか：著者はClaude Max利用者で、3月3〜5日に$10〜$13の「Extra Usage」請求が16件、合計約$180発生。本人はその期間ノートPCを使っておらず、使用履歴も合致しない（ダッシュボードはセッション100%表示、実際のCodeセッションは3月5日に合計7KB未満のみ）。
- サポートの流れ：3月7日に詳細なメールを送付すると、即時に「Fin AI Agent」というAnthropicのAIエージェントが応答し、アプリ内の返金フローを案内。しかしそのフローはサブスクリプション向けで「Extra Usage」には適用されず、人的確認を求めても自動受領メール以降応答なし。3月17、3月25、4月8にフォローするも無回答。
- 広がる影響：同様の報告がGitHubやReddit（claude-code#29289, #24727など）に多数あり、計測メーターの誤表示と誤課金の組み合わせが確認されている。
- 技術的示唆：課金は通常使用メトリクスに基づく。ダッシュボードと実際のAPIセッションログ（トークン/バイト数）に齟齬がある場合、システム側の計測・集計パイプライン（メトリクス収集、バッチ処理、ID紐付け）にバグや遅延がある可能性が高い。AIチャットでの一次対応は速いが、異常系の根本原因調査やクレジット調整は人的オペレーション/権限を要することが多い。

## 実践ポイント
- すぐやること：請求のスクリーンショット、ダッシュボードの履歴、APIログ（request id, timestamp, byte/token数）を保存して時系列で立証できるようにする。
- 予防策：プロダクションで使うAPIキーに課金上限（hard cap）やアラートを設定し、Extra Usageが急増したら自動で通知・遮断する。
- エスカレーション：公式サポートに無反応なら、請求元の決済会社へチャージバック申請、契約担当窓口（営業/リセラー）やSNSでの公開エスカレーション、GitHub/コミュニティIssueで同様報告をまとめて可視化する。
- ガバナンス：社内調達フローに「ベンダーのサポート可用性」の評価を追加し、SLA・返金ポリシーを契約で明確化する。

短く言えば、AIベースの迅速な一次対応は便利だが、誤課金や計測の不整合には「人」が関与できる体制が不可欠。日本の企業も同様のリスクに備えてログ保存・課金上限・エスカレーション手順を整えておこう。
