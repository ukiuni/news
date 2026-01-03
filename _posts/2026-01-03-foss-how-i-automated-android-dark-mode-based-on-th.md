---
  layout: post
  title: "[FOSS] How I automated Android dark mode based on the light sensor - 光センサーでAndroidのダークモードを自動化する方法"
  date: 2026-01-03T13:41:06.673Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/xLexip/Adaptive-Theme"
  source_title: "GitHub - xLexip/Adaptive-Theme: 💡 Auto dark mode based on ambient light for Android. Get it on Google Play!"
  source_id: 472127629
  excerpt: "光センサーで画面点灯時に低負荷で自動ダーク/ライト切替、簡単セットアップの実用OSS"
  image: "https://repository-images.githubusercontent.com/879389086/b3c27f3d-5c20-49ff-8649-c4b8b40ea034"
---

# [FOSS] How I automated Android dark mode based on the light sensor - 光センサーでAndroidのダークモードを自動化する方法
光で切り替わるダークモード──目に優しく、省エネにもなる“現実世界ベース”の自動テーマ切替

## 要約
Ambient light（照度センサー）を使って画面オン時に自動でLight/Darkを切り替えるAndroidアプリ「Adaptive Theme」。画面点灯時のみセンサーを参照するイベント駆動設計でバッテリー影響を最小化し、WRITE_SECURE_SETTINGS権限を使ってシステムテーマを変更する。

## この記事を読むべき理由
職場や通勤で昼夜・照明環境が頻繁に変わる日本の現場では、単純なスケジュール切替より照度ベースの方がユーザ体験と目の疲れ対策で有利。開発者視点でも「実機センサー利用」「権限付与の工夫」「モダンAndroid実装（Kotlin/Compose/Coroutines）」が学べる実用OSSとして有益。

## 詳細解説
- コンセプト：物理的な照度センサー（lux）を基準に、閾値を越えたらLight↔Darkを切替。スケジュールや時間帯ではなく“実際の光”に適応する。
- バッテリー対策：常時ポーリングせず「画面がオンになった直後」にのみセンサーをチェックするイベント駆動方式。バックグラウンドで常時動くことはなく、これにより実質的なゼロバッテリー負荷を実現。
- センサー信頼性：手やポケットで覆われていないかを検証する妥当性チェックを行い、誤検知による不安定な切替を防止する。
- 権限とセットアップ：
  - システムテーマ変更に必要な WRITE_SECURE_SETTINGS を付与する必要があるため、以下の方法を案内：
    - Webツール（推奨、WebADB利用でPCや別端末から簡単に付与）
    - Shizuku（アプリ内で付与可能）
    - Root（ワンタップで付与）
    - 手動ADB（従来のコマンド）
  - 設定は一度行えば以降自動で動作する。
- 実装スタック（リポジトリ技術要点）：
  - 言語/UI：Kotlin、Jetpack Compose、Material 3（Material You）
  - アーキテクチャ：Single-Activity + MVVM、ViewModelはKotlin Flowでリアクティブに管理
  - 並行処理：Coroutines
  - 永続化：Jetpack DataStore（型安全の設定保存）
  - ライセンス：GPL-3.0（オープンソース、広告なし）
- 互換性：多くのカスタムUI（MIUI、OneUI等）でもネイティブなAndroidダークモード実装を尊重する場合は動作するが、機種差あり。Android 14〜17など最新世代での対応を意識している。

## 実践ポイント
- まずは試す：Google PlayからAdaptive Themeをインストールし、lexip.dev/setup（Webツール）でWRITE_SECURE_SETTINGSを付与してみる。
- 閾値調整：明るい/暗い環境で閾値（lux）をいくつか試して、自分の通勤／オフィス照明に最適な値を決める。
- テスト方法：画面をオフ→オンにして切替が起きるか確認。センサーが覆われていないことを確かめること（ポケット・ケースで遮られがち）。
- Root/Shizukuを使う場面：多数台数の社内端末や自動化を簡略化したい場合はShizukuやRootでのセットアップが便利。企業向けはADBスクリプトやMDM連携を検討。
- 代替案との比較：Tasker等の自動化ツールと比べ、Adaptive Themeはセンサー専用・低負荷設計で信頼性が高い点がメリット。
- セキュリティ確認：アプリが要求するのはシステム設定変更のみで、ユーザデータやroot権限を勝手に取得するわけではない。不要ならアンインストールで元に戻る。

このリポジトリは学習用途にも最適で、実機センサー利用や権限周り、Kotlin/Composeベースの現代的なAndroid設計を手早く学べます。興味があればリポジトリをフォークして閾値ロジックや検出条件をカスタマイズしてみてください。
