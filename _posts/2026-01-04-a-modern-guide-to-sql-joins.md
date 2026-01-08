---
  layout: post
  title: "A modern guide to SQL JOINs - SQL JOINsのモダンガイド"
  date: 2026-01-04T15:14:35.372Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://kb.databasedesignbook.com/posts/sql-joins/"
  source_title: "A modern guide to SQL JOINs | Database Design Book"
  source_id: 471315589
  excerpt: "LEFT優先＆ONは外部キー=主キーのみで、給与や請求のJOINバグと性能事故を防ぐ実践ガイド"
---

# A modern guide to SQL JOINs - SQL JOINsのモダンガイド
JOINの“落とし穴”を一瞬で見抜く――現場で効く「LEFT優先＋ID一致」メソッド

## 要約
LEFT JOINを起点に、ONはID等価のみ、JOINは可能な限りN:1（右側に主キー）で書く──このルールだけでバグと性能事故の多くを防げる、という実践的なガイド。

## この記事を読むべき理由
日本の現場ではレガシーSQLや方言、複数ベンダーで混ざったコードベースがよく見られます。給与・請求などのドメインで間違ったJOINにより集計バグや性能劣化が起きるとビジネス影響が大きいため、JOINの正しいメンタルモデルは即戦力になります。

## 詳細解説
- 基本方針（canonical syntax）  
  可読性を優先して統一された書き方を使う：  
  ```sql
  SELECT a.*, b.*
  FROM tableA a
  LEFT JOIN tableB b ON a.id = b.another_id
  WHERE ...
  ```
  ONは結合条件、WHEREはフィルタ。混同しないこと。

- ONは「ID等価」のみを原則に  
  ON句に複雑な条件や非等価を入れると、意味がわかりにくくなりバグの温床になります。実務上ほとんどのケースは外部キー＝主キーの等価で表現可能です。

- N:1 / 1:N / M:N の区別  
  JOINの振る舞いを理解する鍵は、片側の行数関係：
  - N:1（おすすめ）: 左テーブルの各行につき右テーブルは0か1行（右側が主キー）。行数は左テーブルの行数が上限 → 過剰増幅なし、性能良好。  
  - 1:N: 左が主キー側、右が複数行。空の右側はNULL行を生むため意味合いが混在しやすい。  
  - M:N: 双方で複数マッチ。重複・過剰カウントの原因になりやすい。

- 実例（people/payments）  
  スキーマ（抜粋）：people.idは主キー、payments.employee_idはNULL可の外部キー。  
  N:1ケース（支払い→人物）:
  ```sql
  SELECT p.name, pay.amount
  FROM payments pay
  LEFT JOIN people p ON pay.employee_id = p.id;
  ```
  paymentsの行数が結果の上限。employee_idがNULLなら人物列はNULL。  
  1:Nケース（人物→支払い）は、人物に支払いが無ければNULL行が混入し、データの意味合いが混ざるため注意。

- SQLの寛容さが落とし穴に  
  SQLは「書ければ実行する」ため、意図しないクエリが動いてしまう。ONに非等価を入れたり、チェインしたLEFT JOINで右辺が多段に増幅すると、インデックスで解決できない大幅な性能悪化や、GROUP BYでの過剰集計（overcounting）を招きます。

- INNER JOINの本質（概念的）  
  INNER JOINは「フィルタされた直積（Cartesian product）」と考えると誤解が少ない。歴史的な構文や曖昧な説明（ベン図）に頼らず、ID等価＋ケース分類で読み解く方が実務的。

## 実践ポイント
- LEFT JOINは基本に。まずLEFT JOINで考え、意味が合うならINNERにする。  
- ON句は原則「外部キー = 主キー（ID等価）」だけにする。複雑条件はWHEREへ。  
- LEFT JOINでは右側に主キー（N:1）を置くことを優先する。これだけで重複や性能問題の多くを回避できる。  
- M:Nや1:Nが疑われる場合は、事前に集計（COUNT）してデータ分布を確認する。必要ならサブクエリやウィンドウ関数で意図を明示する。  
- GROUP BYやCOUNTで集計する際は、重複行による過剰カウントに注意。必要なら COUNT(DISTINCT ...) や適切なサブクエリで解消する。  
- RIGHT JOINやベン図的説明は避け、読みやすいcanonical構文をチーム規約にする。  
- 既存クエリはEXPLAIN/実行計画と小さなデータ例で挙動を確認。テストデータ（people/paymentsのような代表セット）で回帰テストを用意する。  

日本のシステムでは、給与・請求・受注などのクリティカルな集計処理でJOINの誤りが顕在化しやすいです。ルールをチーム全体で採用し、コードレビューとテストで守るだけで事故を大幅に減らせます。
