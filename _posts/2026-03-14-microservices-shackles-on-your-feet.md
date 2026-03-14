---
layout: post
title: "Microservices: Shackles on your feet - マイクロサービス：足かせの正体"
date: 2026-03-14T22:15:02.964Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://howtocenterdiv.com/beyond-the-div/microservices-shackles-on-your-feet"
source_title: "Microservices vs Monolith: When Splitting Your App Makes Things Worse | How to Center a Div"
source_id: 382934118
excerpt: "無闇なマイクロサービス化が招く運用地獄と回避法を実践的に解説"
image: "https://cdn.howtocenterdiv.com/howtocenterdiv/avatars/cmml03x220001wegy81hia7yo/1773484858412-dd4f5dfa21ffd.svg"
---

# Microservices: Shackles on your feet - マイクロサービス：足かせの正体
「分割すれば解決」は幻想——まずはモノリスの境界をきちんと引こう

## 要約
モノリスを無闇にマイクロサービス化すると、可用性・デバッグ・運用コストが著しく悪化する。分割が意味を持つのは、チーム独立性・スケーリング特性・人数（概ね150人超）など明確な条件が揃ったときだけ。まずはモジュラーモノリスと観測性を整えるべき。

## この記事を読むべき理由
日本のスタートアップ〜中堅開発チームは「マイクロサービス＝先進」が誤解になりがち。無駄な分割で夜中のアラート地獄やオンボーディング地獄を招く前に、判断基準と実践ステップを押さえると時間とコストを節約できます。

## 詳細解説
- 本質的問題は「分割」ではなく「境界設計」
  - デプロイが壊れる、スケールできない、読みづらいコード──多くはテスト不足、密結合、DB設計の問題。サービス化で直らず、むしろネットワーク障害や分散トランザクションといった新しい障害モードが増える。
- ネットワークは嘘をつかない（＝失敗する要素）
  - 単純な関数呼び出しが、タイムアウト・リトライ・サーキットブレーカー等で複雑化する。
- 分散トランザクションのコスト
  - 単一SQLコミットが、イベント連鎖＋補償ロジックに変わるため信頼性運用が難しくなる。
- ロギング・トレーシングが必須
  - 分割前に分散トレーシング（Jaeger/Tempo）、メトリクス（Prometheus/Grafana）、集中ログ（Loki/ELK）を構築しないと原因追跡が不可能。
- ローカル開発とオンボーディング負荷
  - 複数サービスを起動する開発環境は新規参加者の生産性を大きく下げる。
- 第三の選択肢：モジュラーモノリス
  - 単一デプロイを保ちつつ、モジュール（公開インタフェースのみで通信）で厳格な境界を設ける。将来サービス化するとき抽出作業が単純になる。
- 分割するなら「ストレンジャーフィグ（段階的抽出）」を使い、ファサードで呼び口を変えず徐々に外出しする。大改修（rewrite）は避ける。

（例：モノリス vs マイクロサービスの呼び出し — Go）
```go
// go
// Monolith: 単純、失敗点少ない
func GetUserOrder(userID string) (*Order, error) {
  user := userRepo.Find(userID)
  order := orderRepo.Latest(user)
  return order, nil
}

// Microservices: ネットワーク障害が入り込む
func GetUserOrder(userID string) (*Order, error) {
  ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
  defer cancel()
  user, err := userClient.Find(ctx, userID)
  if err != nil { return nil, fmt.Errorf("user service down: %w", err) }
  order, err := orderClient.Latest(ctx, user.ID)
  if err != nil { return nil, fmt.Errorf("order service down: %w", err) }
  return order, nil
}
```

（例：モノリスの単一トランザクション — SQL）
```sql
-- sql
BEGIN;
UPDATE inventory SET stock = stock - 1 WHERE product_id = 42;
INSERT INTO orders (user_id, product_id) VALUES (101, 42);
COMMIT;
```

（例：ファサードで段階的に外出しする — TypeScript）
```typescript
// typescript
class PaymentFacade {
  constructor(private svc: PaymentService) {}
  async charge(amount: number, customerId: string) {
    return this.svc.charge(amount, customerId); // in-process
  }
}
// 後に同じインタフェースで HTTP 呼び出しに差し替え可能
```

## 実践ポイント
- 分割前チェック（4つの質問）
  1. 単独でデプロイできるか？ → NOなら分割しない
  2. 真に異なるスケーリングプロファイルがあるか？ → NOなら再検討
  3. 分散トレーシングと集中ログはあるか？ → NOなら先に構築
  4. 境界をエンドツーエンドで管理できる体制か？ → NOなら待つ
- まずはモジュラーモノリス化：モジュールは公開APIのみで通信、ユーティリティへのクロス参照を禁止すること
- 観測性を投資：Jaeger/Tempo、Prometheus/Grafana、Loki/ELK を導入してから分割を検討
- 分割は段階的に：ストレンジャーフィグとファサードでリスクを吸収。絶対に大規模な書き換え（rewrite）は避ける
- 規模目安：チームが150人を超え、独立リリースが真に必要になったときがマイクロサービスを本気で検討するタイミング

短く言えば：問題の本質を見極め、まずは境界と観測性を整えよ。マイクロサービスは万能薬ではなく、適切な文脈でのみ意味を持ちます。
