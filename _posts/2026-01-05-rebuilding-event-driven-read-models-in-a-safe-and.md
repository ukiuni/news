---
  layout: post
  title: "Rebuilding Event-Driven Read Models in a safe and resilient way - イベント駆動のリードモデルを安全かつ堅牢に再構築する"
  date: 2026-01-05T19:24:23.986Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://event-driven.io/en/rebuilding_event_driven_read_models/"
  source_title: "Rebuilding Event-Driven Read Models in a safe and resilient way - Event-Driven.io"
  source_id: 470366131
  excerpt: "PostgreSQLのアドバイザリロックで停止ゼロにリードモデルを安全に再構築する方法"
  image: "https://event-driven.io/static/9e38ed3c86bf4b6ef2a88b6e89966001/2a4de/2026-01-05-cover.png"
---

# Rebuilding Event-Driven Read Models in a safe and resilient way - イベント駆動のリードモデルを安全かつ堅牢に再構築する
停止ゼロでリードモデルを差し替える——PostgreSQLアドバイザリロックで実現する「安全なリビルド」パターン

## 要約
イベントログを使ったリードモデルの再構築は、要件変更やバグ修正で必須になるが、ダウンタイムや競合を招きやすい。本稿は「インライン vs 非同期」「インプレース更新 vs ブルー/グリーン」「同時実行対策」にフォーカスし、PostgreSQLのアドバイザリロックを使った現実的な解決策を示す。

## この記事を読むべき理由
- 日本でもPostgreSQL採用が多く、イベント駆動やアウトボックスを使うシステムが増えている。  
- バックフィルやビュー変更を安全に行えれば、機能追加やデータ修正のリスクを大幅に下げられる。  
- Kubernetes環境での冪等性・並列処理問題に実務で直面している開発者に即役立つ手法を提示する。

## 詳細解説
1) リードモデル再構築が必要になる局面
- 要件追加（例：カートにステータスや商品詳細を追加）や過去の誤データ修正で既存プロジェクションを作り直す必要が出る。  
- 「そのままアップデートして良いか」「新しい読み取り用ビューを作るか」は影響範囲（UI/他クエリ）を見て判断する。

2) インライン投影（inline）と非同期投影（async）のトレードオフ
- インライン：イベント保存と同一トランザクションでプロジェクションを更新 → 即時整合性。だがトランザクションが長くなりスループット低下、デッドロックのリスク増加。  
- 非同期：イベントを持つログを別プロセスで読み取りプロジェクションを作る → バッチ処理や水平スケールが可能。だが再構築時のラグ（eventual consistency）を管理する必要あり。  
- 実務ルール例：単一ストリーム・単純プロジェクションはインラインで十分、複雑処理やワークフロー連携は非同期を選ぶ。

3) 再構築の戦略（インプレース vs ブルー/グリーン）
- インプレース：既存テーブルをtruncateして再プロジェクト。簡単だがその間クエリは空/古い状態に。  
- ブルー/グリーン：新テーブル（例: carts_v2）を並列で作り、バックフィル完了後に切り替える。ダウンタイムが無く安全だが、切替ロジックやDBスキーマの動的管理が必要（ORMの制約に注意）。

4) チェックポイントと再処理
- イベントログには単調増加するポジションがある。プロセッサは処理済み位置を保存（チェックポイント）して再起動時に再開する。再構築はチェックポイントを先頭にリセットするか、新しいプロセッサを走らせる方法で実施する。

5) 同時実行と分散ロックの解
- 問題：再構築中に新しいイベントが来る / 複数の再構築ワーカーが走ると競合や重複処理が発生する。  
- 解法：分散ロックで「唯一の再構築ワーカー」を保証しつつ、インライン投影は通常処理を続けられるようにする。

6) PostgreSQLのアドバイザリロックを使った設計
- row-level lock（SELECT ... FOR UPDATE）は明示的だが、インラインで毎回使うとスループットを殺す（全プロセスが順番待ちになる）。  
- advisory lockは任意の整数に対するロックで、テーブル行を消費しない。shared（複数保有可）と exclusive（単独）をサポートするため、下記のように使える：
  - インライン投影はsharedロックを取得して通常処理を継続（同時複数可）。  
  - 再構築はexclusiveロックで取得 → 全てのsharedロックをブロックして安全に再構築。  
- projection名+バージョンをハッシュして整数にマップする（md5→64ビット等）。衝突リスクは低いが気になる場合はメタテーブルのIDを使う。

サンプル（SQL）:
```sql
-- shared: インライン投影側（失敗したらスキップ）
SELECT pg_try_advisory_xact_lock_shared(
  ('x' || substr(md5($1), 1, 16))::bit(64)::bigint
) AS acquired;

-- exclusive: 再構築ワーカー（待機 or ブロック）
SELECT pg_try_advisory_lock(
  ('x' || substr(md5($1), 1, 16))::bit(64)::bigint
) AS acquired;
```

短いTypeScriptの投影evolve例（概念）:
```typescript
type CartSummary = { total: number; count: number; items?: any[] };

function evolve(doc: CartSummary | null, evt: any): CartSummary {
  const base = doc ?? { total: 0, count: 0 };
  switch (evt.type) {
    case 'ProductAdded':
      return { ...base, total: base.total + evt.price * evt.qty, count: base.count + evt.qty };
    case 'ProductRemoved':
      return { ...base, total: base.total - evt.price * evt.qty, count: base.count - evt.qty };
    default:
      return base;
  }
}
```

7) advisory lockだけでは足りない点
- advisory lockはセッションスコープ。接続が切れると自動解放されるため、途中で死んだワーカーの再試行や監視が必要。  
- 実運用では「advisory lock + projectionsメタテーブル（status, last_heartbeat） + ワーカーヘルス監視」を組み合わせるのが現実的。KubernetesではLeader Election（configmap/coordination）やRedisで補助するのも選択肢。

## 日本市場との関連性
- 日本のSaaS／EC事業者はPostgreSQL＋Kubernetes構成を採ることが多く、提案するパターンはそのまま適用しやすい。  
- 年末・セール時の高TPS環境でも、インラインでのロック負荷を避けつつ安全にビューを差し替えられるのは運用負担を下げる。  
- 多くの企業がORMを使っているため、ブルー/グリーン実装時のテーブル追加やマイグレーション手順を事前に整備しておくとスムーズ。

## 実践ポイント
- まず判断：新モデルを別テーブルで作るか既存を更新するかをUI影響範囲で決める（デフォルトは分離）。  
- 再構築は可能ならブルー/グリーンを採用し、切替条件（ラグ閾値、イベントポジション）を明確にする。  
- 同時実行制御はPostgreSQLのアドバイザリロックを中心に、メタテーブルでstatus/heartbeatを合わせて運用する。  
- インライン投影でsharedロック、再構築でexclusiveロック。インラインはfail-fast、再構築は待機（あるいはリトライ）ポリシーを定める。  
- ORMsを使う場合は動的なテーブル追加や切替をどう扱うか（ネーミング戦略、マイグレーション）を設計段階で検討する。  
- テスト：意図的にワーカーを落とす、複数ワーカーで同時再構築を試す、ラグ閾値で切替成功を検証する。

短くまとめると、イベント駆動の利点（追跡可能性・バックフィル性）を生かしつつ「アドバイザリロック＋チェックポイント＋ブルー/グリーン」で安全にリードモデルを差し替えるのが実務で有効なアプローチです。
