---
  layout: post
  title: "Jeffgeerling.com has been Migrated to Hugo - JeffGeerling.com は Hugo に移行されました"
  date: 2026-01-04T14:04:55.891Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.jeffgeerling.com/blog/2026/migrated-to-hugo/"
  source_title: "JeffGeerling.com has been Migrated to Hugo - Jeff Geerling"
  source_id: 46487498
  excerpt: "20年分のコンテンツを保ちつつDrupalからHugoへ移行し執筆に集中でき、運用負担を削減"
  ---

# Jeffgeerling.com has been Migrated to Hugo - JeffGeerling.com は Hugo に移行されました
20年分のコンテンツを捨てずに軽量化したい人へ — Drupal を離れて Hugo を選んだ理由と実践知

## 要約
個人ブログ（約20年・3500+投稿）を重厚なDrupalから静的サイトジェネレータHugoへ移行。Markdownネイティブなワークフローと運用負荷の劇的な軽減が狙い。コメントや検索はフェーズ2で対応予定。

## この記事を読むべき理由
- 大規模な既存コンテンツを抱える日本の技術ブログ運営者やプロジェクト記録者にとって、CMS→SSG移行のリアルな判断基準と落とし穴が学べる。
- 運用コスト（PHP/Composer/DB/キャッシュ等）と創作コスト（記事を書く時間）のトレードオフは多くの現場で直面する課題だから。

## 詳細解説
- 背景：著者は長年Drupalでサイトを運用してきたが、複数のメジャーアップグレード、プラグイン互換性、メディア管理や公開ワークフローの複雑さに疲弊。個人ブログでは「書くこと」に集中したいという理由で静的化に踏み切った。
- なぜHugoか：HugoはGo製で高速、設定が比較的シンプル、Markdownをそのまま扱えるため既存の執筆フローを損なわない。JekyllはGitHub Pages向きだが、Rubyに馴染みがない場合はHugoの方が敷居が低い。
- 移行の難所：20年分・3500+の記事、画像参照の壊れ、旧URLのリダイレクト、コメントや検索インデックスの移行は時間と手間がかかる。完全自動化は難しく、移行用のスクリプトと段階的検証が必要。
- 執筆ワークフローの改善：以前はDrupal上でMarkdownを貼り付け、画像を個別アップロードして挿入、公開フラグやキャッシュパージを手動で行っていた。HugoではMarkdownファイル＋フロントマターの更新でビルド＆デプロイ（例: hugo && git push）すれば完了し、クリエイティブ作業に集中できる。
- 運用観点：静的化によりサーバーサイドの管理対象（PHP、DB、Drush、Composer、Nginxなど）が大幅に減る。一方で、コメントや全文検索などはSaaSや別ソリューションで補う必要がある。
- 注意点（日本語固有の課題）：全文検索や形態素解析（日本語の分かち書き）を正しくやるには、Solr/ElasticsearchのkuromojiやMeilisearch/Typesenseの導入検討が必要。日本語のランキングやファセットは英語とは別設計になることが多い。

## 実践ポイント
- 移行計画を段階化する：まずはコンテンツのエクスポート→Markdown化→静的テンプレート適用→徐々にリダイレクト設定、画像確認、コメント／検索対応の順。
- リダイレクトは最優先で用意する：SEOと既存ブックマーク対策に必須。サーバー側の301ルールやCDNで対応。
- 画像とメディアを一括変換・検証する：パスの正規化、レスポンシブ画像、不要ファイルの除去を自動化するスクリプトを用意する。
- フロントマターを整備する：投稿日・タグ・カテゴリ・draftフラグを正しく移すとHugoワークフローがスムーズ。
- コメント／検索の選択肢：
  - コメント：Giscus / Utterances（GitHub Issues連携）、Staticman、Self-hostedの選択肢を比較検討。
  - 検索：小規模ならLunr/Elasticlunr、スケールや日本語対応ならElasticsearch + kuromoji、MeilisearchやTypesenseも検討。
- デプロイとCI：ビルドをCI（GitHub Actions等）で自動化し、hugo build → CDNへデプロイで更新を短縮。
- 現場のコスト試算：運用コスト（サーバー・保守時間）と執筆時間の価値を比較して、静的化のROIを数値化しておく。

短くまとめると、個人で「書く」ことを第一にしたいなら、Hugoへ移るメリットは大きい。ただし大規模な既存資産を壊さず移行するには計画とツール選定（特に日本語検索・コメント）が重要。
