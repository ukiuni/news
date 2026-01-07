---
  layout: post
  title: "PostgreSQL 18 RETURNING Enhancements: A Game Changer for Modern Applications - PostgreSQL 18 の RETURNING 強化：モダンアプリに効く革命"
  date: 2026-01-07T09:22:51.668Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.pgedge.com/blog/postgresql-18-returning-enhancements-a-game-changer-for-modern-applications"
  source_title: "PostgreSQL 18 RETURNING Enhancements: A Game Changer for Modern Applications"
  source_id: 1543461989
  excerpt: "Postgres18のRETURNINGで旧値・新値を単文取得、同期と監査を簡素化"
  ---

# PostgreSQL 18 RETURNING Enhancements: A Game Changer for Modern Applications - PostgreSQL 18 の RETURNING 強化：モダンアプリに効く革命
Postgres 18で「変更前／変更後」を一発で取れる！MERGE＋RETURNINGの新機能で同期・監査が劇的にシンプルに

## 要約
Postgres 18は`RETURNING`句に`OLD`/`NEW`エイリアスを導入し、`INSERT`/`UPDATE`/`DELETE`/`MERGE`の各操作で「変更前」と「変更後」を同一文で取得可能にした。これにより追加のSELECTや複雑なトリガーを減らし、同期・監査処理が大幅に簡素化される。

## この記事を読むべき理由
日本のSaaS/EC/業務システムではデータ同期・差分監査が頻出課題。複数テーブルのアップサートや外部データ取り込みで往復クエリやアプリ側ロジックに頼っているなら、Postgres 18の機能で運用コストとレイテンシを下げられる可能性が高い。

## 詳細解説
背景：従来の`RETURNING`は操作タイプごとに返せる値が限定され、更新前後の比較を行うには事前SELECTやトリガー、アプリでの比較が必要だった。Postgres 17で`MERGE`に`RETURNING`が追加されていたが、18ではさらに`OLD`/`NEW`という特殊エイリアスを導入し、全てのDMLで一貫して利用できるようになった（実装はDean Rasheedらによるコミット）。

何ができるか：
- 単一文でアップサートの結果（追加・更新・削除）を把握できる
- `OLD`は変更前、`NEW`は変更後の行を参照
- エイリアスは`WITH (OLD AS previous, NEW AS current)`のようにリネーム可能

例：在庫同期のMERGE（抜粋）
```sql
-- sql
MERGE INTO products p
USING product_staging s
ON p.product_code = s.product_code
WHEN MATCHED THEN UPDATE
  SET product_name = s.product_name,
      price = s.price,
      stock_quantity = s.stock_quantity,
      last_updated = CURRENT_TIMESTAMP
WHEN NOT MATCHED THEN INSERT (product_code, product_name, price, stock_quantity)
  VALUES (s.product_code, s.product_name, s.price, s.stock_quantity)
RETURNING p.product_code,
          merge_action() AS action,
          old.product_name AS old_name,
          new.product_name AS new_name,
          old.price AS old_price,
          new.price AS new_price,
          (old.price IS DISTINCT FROM new.price) AS price_changed;
```

監査用途：トリガー不要でJSONBに旧値／新値／差分を格納することで、単一トランザクションで完全な監査ログを作成できる（上記MERGEを`WITH merge_results AS (...)`で囲んで監査テーブルにINSERTする構成が有効）。

実装・互換性のポイント：
- Postgres 18での追加機能なのでアップグレードが必要
- アプリの既存クエリやトリガー設計を見直せば余計な処理を削減可能
- 将来的な拡張（MERGEの細かなWHEN拡張やRETURNINGでの集約返却など）も期待されている

## 実践ポイント
- 小さく試す：まず開発環境で既存の一連のアップサート処理を`MERGE ... RETURNING old/new`に置き換え、性能・行数・トランザクション境界を確認する。
- 監査の簡素化：監査用テーブルを用意して`jsonb_build_object`で旧値／新値を格納すれば、トリガーを外して監査ロジックの可観測性を上げられる。
- レガシー排除：事前SELECTやアプリ側差分ロジックを削減するとネットワーク往復とバグの温床を減らせるが、アップグレード計画とロールバック戦略は必ず用意する。
- 日本市場向け運用例：複数拠点で在庫／価格を同期するECプラットフォームや、金融系の訂正ログ取得など「原子性の高い差分取得」が重要な領域で即効性がある。

Postgres 18の`OLD`/`NEW`付き`RETURNING`は、SQLレベルで「何が変わったか」を明示的に返せるため、実運用での手戻りを大きく減らす武器になる。まずは影響範囲の小さい処理から置き換えて効果を確かめることをおすすめする。
