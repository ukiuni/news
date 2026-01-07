---
  layout: post
  title: "The most popular Go dependency is… - 最も人気のあるGo依存は…"
  date: 2026-01-07T12:53:12.052Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://blog.thibaut-rousseau.com/blog/the-most-popular-go-dependency-is/"
  source_title: "The most popular Go dependency is… | Thibaut Rousseau&#x27;s Blog"
  source_id: 1477940862
  excerpt: "40Mノード解析で判明：最も依存されるGoライブラリは stretchr/testify"
  image: "https://blog.thibaut-rousseau.com/images/og-image.png"
---

# The most popular Go dependency is… - 最も人気のあるGo依存は…
テストライブラリが圧倒的トップに！Goモジュール全網羅で見えた「使われ方」の実態

## 要約
Goのモジュール公開インデックスを丸ごと解析して依存グラフをNeo4jに構築した結果、最も多く参照されるライブラリは github.com/stretchr/testify であることが明らかになった（データセットは約4000万ノード／4億辺）。

## この記事を読むべき理由
依存関係の実利用状況は「スター数」や「更新頻度」だけでは見えません。日本のプロダクトでもサプライチェーンや互換性、保守性を考える上で、実際にどれだけ“食われている”かを把握することは重要です。本記事はその手法と結果、実務で使えるクエリ例を短くまとめます。

## 詳細解説
- データ収集の発想
  - 著者は当初GitHubクローンからgo.modを辿る方法を試したが、サンプル偏りと遅さの問題で断念。
  - 代わりに proxy.golang.org と index.golang.org の公開フィードを利用し、2019年以降のモジュール名とバージョンをローカルにダウンロードして解析した（不変キャッシュとして保存）。

- モデル（Neo4j）
  - ノード: Module { name, version, ... }（後に timestamp, latest フラグや semver 分解などを追加）
  - リレーション: (dependent)-[:DEPENDS_ON]->(dependency)
  - 制約・インデックス:
    - (name, version) の一意制約（MERGEでのupsertを前提）
    - name に対するインデックス（大量データでは明示的に作る必要あり）

- 挿入とクエリの要点
  - ノードの upsert:
```cypher
MERGE (m:Module { name: $name, version: $version }) RETURN m
```
  - 依存関係の作成（存在しない場合でも作成する安全な書き方）:
```cypher
MERGE (dep:Module { name: $dependencyName, version: $dependencyVersion })
MERGE (ctr:Module { name: $dependentName, version: $dependentVersion })
MERGE (ctr)-[:DEPENDS_ON]->(dep)
```
  - あるモジュールの直接依存元（最新バージョンのみをカウント）:
```cypher
MATCH (dep:Module { name: 'github.com/pkg/errors', version: 'v0.9.1' })
MATCH (m:Module)-[:DEPENDS_ON]->(dep)
WHERE m.isLatest
RETURN m.versionTime.year AS year, COUNT(m) AS nbDependents
```
  - トランジティブな参照（深さ指定や全階層探索が簡潔）:
```cypher
MATCH (dep:Module { name: 'github.com/pkg/errors', version: 'v0.9.1' })
MATCH (m:Module)-[:DEPENDS_ON*1..]->(dep)
WHERE m.isLatest
RETURN COUNT(DISTINCT m) AS nbDependents
```
  - 比較: Cypherの *1.. に対して、同等のSQL（再帰CTE）はずっと複雑になる。

- 規模と知見
  - 解析結果: 約40Mノード、約400Mリレーション。平均で直接依存の数は約10。
  - トップ依存（抜粋）:
    1. github.com/stretchr/testify — 約259,237件
    2. github.com/google/uuid — 約104,877件
    3. golang.org/x/crypto — 約100,633件
    4. google.golang.org/grpc — 約97,228件
    5. github.com/spf13/cobra — 約93,062件
    ･･･（上位はテスト／ユーティリティ／標準拡張が占める）

- 再現と配布
  - ソース: go-stats リポジトリ（解析スクリプト）
  - 大規模Neo4jダンプ（約11GiB）が配布されており、指示に従えばローカルでクエリ可能。

## 実践ポイント
- まずは自分のプロジェクトで「誰が自分の依存を参照しているか」を把握する:
```cypher
MATCH (dep:Module { name: 'あなたの/モジュール', version: 'vX.Y.Z' })
MATCH (m:Module)-[:DEPENDS_ON]->(dep)
WHERE m.isLatest
RETURN m.name, m.version
```
- プロダクトのサプライチェーン把握:
  - 重要な依存（例: testify や x/crypto）が壊れた場合の影響範囲をトランジティブに評価する。
- 自分でスケール解析をするなら:
  - proxy.golang.org の index を使う（ローカルに保存してイミュータブルなキャッシュにするのが高速化の鍵）。
  - Neo4j に投入する際は必ずインデックス／制約を先に作ること（性能が劇的に変わる）。
- 小規模でも役立つツール:
  - go mod graph や go list -m -json を使って社内パッケージを収集し、同様のグラフ解析にかけると供給網の可視化に有効。
- 注目ライブラリの扱い:
  - テストライブラリ（testify）は多方面で依存されているため破壊的変更には注意。互換性のチェックや代替手段の検討をおすすめ。

参考: 元解析は Thibaut Rousseau さんの「The most popular Go dependency is…」。大規模なオープンデータとNeo4jを使った実例は、依存関係の実態把握に強い示唆を与えます。
