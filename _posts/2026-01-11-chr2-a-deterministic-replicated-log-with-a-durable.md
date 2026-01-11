---
layout: post
title: "chr2 - a deterministic replicated log with a durable outbox for side effects - chr2：副作用に耐える耐久型アウトボックスを持つ決定論的レプリケーテッドログ"
date: 2026-01-11T00:27:32.645Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/abokhalill/chr2"
source_title: "GitHub - abokhalill/chr2: A deterministic, crash-safe distributed state machine with exactly-once side effects."
source_id: 465970507
excerpt: "耐久アウトボックスで副作用を厳密に一度だけ実行するchr2設計を解説"
image: "https://opengraph.githubassets.com/f2bf1fab32c8345ec0560a3a91ced6c5202f2e45f007c177b8780338983fa556/abokhalill/chr2"
---

# chr2 - a deterministic replicated log with a durable outbox for side effects - chr2：副作用に耐える耐久型アウトボックスを持つ決定論的レプリケーテッドログ
クラッシュしても「副作用は必ず一度だけ」──Rust製の分散ログ実装 Chronon（chr2）の核をやさしく解説

## 要約
Chronon（chr2）は、Viewstamped Replication（VSR）を用いた決定論的レプリケートログと「耐久的アウトボックス」を組み合わせ、クラッシュやリーダー交代が起きても副作用（メール送信・ webhook 等）がちょうど一度だけ実行されることを目指すプロジェクトです。

## この記事を読むべき理由
金融・決済・在庫管理など「データ損失や副作用の重複実行が許されない」領域は日本でも多く、そうしたシステム設計の実例を知ることは設計力向上に直結します。また、Rust + io_uring 等の最新スタック採用例としても学びが多いです。

## 詳細解説
- コア保証
  - Durability：コミットしたエントリは単一ノード障害から復旧する
  - Consistency：クォーラム合意で線形化可能な読み書き
  - Exactly-Once：副作用はクラッシュやフェイルオーバー後でも一度だけ実行
  - Determinism：同じログから複製ノードが同一状態に収束

- アーキテクチャ（概念）
  - Control Plane（ハートビート、選挙、ビュー変更）と Data Plane（ログ書き込み、耐久性）を分離。これによりディスクI/Oの遅延がクラスタ可用性を悪化させにくくしている。
  - 主なコンポーネント：LogWriter（O_DSYNC で同期耐久）、Snapshots（ログ圧縮）、Durable Outbox（副作用用）、VsrNode（VSR の実装）、Executor（決定論的状態機械）、SideEffectManager（フェンシング付き実行）

- 耐久的アウトボックスの考え方（重要）
  - アプリケーションは「副作用の意図（intent）」をイベントとしてログに書き込む（実行はしない）。
  - アウトボックスは複製されたアプリケーション状態の一部として保持される。
  - プライマリだけが実行責任を持ち、実行後に AcknowledgeEffect イベントをコミットする。
  - フェイルオーバー後、新プライマリは未確認の意図を再実行するが、アプリ側での idempotency と確認イベントにより結果的に exactly-once を達成する（少なくとも1回実行＋アプリ側の冪等性 = 厳密に1回）。

- 実装上の工夫
  - fdatasync / O_DSYNC を明示的に使い「書き込みしたら確実にディスクへ」を保証（implicit キャッシュは許さない設計）。
  - ハッシュチェーンで整合性検出（エントリ間リンクで破損を発見）。
  - Chaos テスト（Nemesis）を重視：パーティションやノード殺し込みで「壊れないこと」を検証する文化。

- 技術スタック
  - 言語：Rust（安全性と性能）
  - Linux 特化で io_uring / O_DIRECT をサポート（ゼロコピーや低レイテンシを狙う）
  - 単一スレッドで決定論を保つ Executor、バックグラウンドでの非同期耐久化スレッドなどの並列設計

コードの例（アプリ実装の骨格、実際はライブラリの trait を実装する）:
```rust
// rust
impl ChrApplication for MyApp {
    type State = MyState;
    type QueryRequest = MyQuery;
    type QueryResponse = MyResponse;
    type Error = MyError;

    fn apply(&self, state: &Self::State, event: Event, ctx: &ApplyContext)
        -> Result<(Self::State, Vec<SideEffect>), Self::Error> {
        // イベントを適用し、必要なら SideEffect の意図を返す
        Ok((new_state, vec![]))
    }
    // query, snapshot, restore, genesis を実装する
}
```

## 日本市場との関連性
- 金融・決済：重複実行が金銭的損失に直結するため「exactly-once」は大きな価値。
- サプライチェーン/製造：外部システムへの副作用（在庫更新や発注通知）で誤実行が致命的。
- 国内SRE/プラットフォームチーム：ディスク遅延や一時的I/O問題が可用性に与える影響を最小化する設計は運用負荷低減に寄与。
- Rust の採用が進む企業（特にインフラ系）にとって、実践的な参考実装となる。

## 実践ポイント
- 試す：リポジトリをクローンして付属のクラッシュテストを動かす
  - cargo run --release
  - cargo run --release -- write / recover / test（段階的に試せる）
- 組み込み案：自社の副作用（メール送信・外部API呼び出し）をアウトボックス意図に置き換え、アプリ側で冪等化キーを用意する
- 評価項目：フェイルオーバー時の副作用二重実行、ログ破損検出、スナップショットでの復元時間、io_uring を使った性能改善効果
- 注意点：プロジェクトは活発に開発中。商用採用前にテストカバレッジ・運用シナリオ（バックアップ、監視、スキーマ進化）を十分検証すること

Chronon（chr2）は「クラッシュしても副作用は1回だけ」を目指す明確な設計と、Rust＋Linuxの最新I/O機能を活用した実装例です。興味があれば実際にデモを動かして、自分のユースケースでの振る舞いを確かめてみてください。
