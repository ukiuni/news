---
  layout: post
  title: "Firefox extension to redirect x.com to xcancel.com - x.comをxcancel.comへリダイレクトするFirefox拡張"
  date: 2026-01-07T11:39:49.229Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://addons.mozilla.org/en-US/firefox/addon/toxcancel/"
  source_title: "ToXCancel – Get this Extension for 🦊 Firefox (en-US)"
  source_id: 46524873
  excerpt: "ボタン一つでログイン不要、Xスレッドをxcancelで即表示するFirefox拡張"
  image: "/static-frontend/02ea754b37fd50cca41d6aa1747a3848.png"
---

# Firefox extension to redirect x.com to xcancel.com - x.comをxcancel.comへリダイレクトするFirefox拡張
ログイン無しでX（旧Twitter）のスレッドを読む最短ルート — Firefox拡張「ToXCancel」レビュー

## 要約
ToXCancelは、x.com（twitter.com）へのアクセスを自動的にxcancel.com（xのミラー）へリダイレクトして、アカウントなしでスレッドや返信を閲覧できるFirefox拡張です。Firefox（Android向けに公開）で動作し、GPLv3で配布されています。

## この記事を読むべき理由
- 日本でもXのログイン壁や閲覧制限に困っている人は増えています。手早くスレッドを確認したい場合、この拡張は即効性のある実用的な解決策です。  
- ブラウザ拡張のシンプルな実装パターン（リクエスト監視→リダイレクト）を知ることで、同様のユーティリティ開発や運用時の注意点が学べます。

## 詳細解説
- 主な機能  
  ToXCancelはブラウザがx.comまたはtwitter.comへ移動しようとした直前に、そのリクエストを検知してxcancel.comへ差し替えます。結果として、ログインを要求する公式ページを経由せずにミラー上のコンテンツを表示できます。

- 動作環境・メタ情報  
  - 公開先：Mozilla Add-ons（Firefox向け、案内ではFirefox for Androidに対応と明記）  
  - ユーザー数：約2,000人、評価4.8（17件）  
  - ライセンス：GNU GPL v3.0  
  - バージョン：1.3（最終更新：2025-05-11）  
  - 必要権限：x.comおよびtwitter.comドメインへのアクセスは「オプション権限」として要求（拡張はこれらのサイトデータにアクセスする可能性があるため、インストール時に確認が必要）

- 技術的背景（実装の概念）  
  WebExtensionとしては、ページ読み込み前にリクエストをフックしてリダイレクトする仕組みを使っています。Firefoxでは webRequest の onBeforeRequest（または同等の宣言型API）でホスト名を判定して別URLへ置き換えるのが一般的です。ホスト権限を限定的に設定し、リダイレクトループや入れ子のリダイレクトを防ぐ処理が重要です。

- 限界と注意点  
  - ミラーは完全な機能互換を保証しないため、埋め込みメディアや一部のインタラクションは動作しない場合があります。  
  - 拡張がサイトデータへアクセスする権限を持つため、信頼できるソースかどうかを必ず確認してください。  
  - 法的・利用規約上の問題やミラー運営の可用性に依存するため、常に動作を保証するものではありません。

## 実践ポイント
- すぐ使う方法  
  1. Mozilla Add-onsのToXCancelページを開く（アドオンページにアクセス）  
  2. 権限を確認してインストール（x.com/twitter.comへのアクセス許可をチェック）  
  3. XのスレッドURLを開くと自動的にxcancel.comへ切り替わるか確認

- 開発・管理者向けチェックリスト  
  - 最小限のホスト権限に留める（例：具体的なサブドメインのみ要求）  
  - リダイレクトループ対策（同一ドメインの再リダイレクトを防ぐフラグ）  
  - Androidとデスクトップでの挙動差をテストする（ユーザーエージェントやUA依存の差異）  
  - 利用者に対してプライバシーと権限の説明を明示する

- 代替手段  
  - 別のミラーやリーダーモードを試す（ミラーは停止する可能性があるため複数手段を把握）  
  - 企業・教育機関の環境ではネットワークポリシーに抵触しないか確認する

短くまとめると、ToXCancelは「手早く・ログイン不要でXの公開スレッドを読む」ための実用的ツールです。導入前に権限とミラーの挙動をチェックすれば、日常の情報収集を少し快適にしてくれます。
