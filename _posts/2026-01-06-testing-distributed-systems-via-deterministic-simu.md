---
  layout: post
  title: "Testing distributed systems via deterministic simulation (writing a \"hypervisor\" for Raft, network, and disk faults) - 分散システムを決定論的シミュレーションで試験する（Raft・ネットワーク・ディスク障害用の“ハイパーバイザ”を作る）"
  date: 2026-01-06T18:53:04.092Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/octopii-rs/octopii"
  source_title: "GitHub - octopii-rs/octopii: 🦑 Distributed Systems Kernel written in rust"
  source_id: 469451992
  excerpt: "稀なクラッシュを瞬時に再現してバグを大量発見するRust製決定論的分散シミュレータ"
  image: "https://opengraph.githubassets.com/85488796ad52bdd04ac0df5791cdd0cad8b7eb3acb6cc4553a52ff90282849db/octopii-rs/octopii"
---

# Testing distributed systems via deterministic simulation (writing a "hypervisor" for Raft, network, and disk faults) - 分散システムを決定論的シミュレーションで試験する（Raft・ネットワーク・ディスク障害用の“ハイパーバイザ”を作る）
魅せるタイトル: 「クラッシュを再現して“バグを爆速で炙り出す”――Rust製分散カーネル Octopii の決定論的シミュレーションが示す現場改善の道筋」

## 要約
OctopiiはRustで実装された「分散システムのカーネル」で、Raft・ネットワーク・ストレージ・ランダム性を抽象化し、生産運用と決定論的シミュレーション（DST）による大規模故障注入テストを両立する点が特徴。短時間で再現可能なクラッシュケースを大量検証できる。

## この記事を読むべき理由
日本企業では金融・製造・通信など「可用性と整合性」が重要なシステムが多く、プロダクションで稀にしか出ないクラッシュバグを再現・検証するインフラは価値が高い。Octopiiのアプローチは、テスト工数を劇的に減らし運用前の信頼性保証を強化する実践的な手法を提供する。

## 詳細解説
- コア概念  
  - Raft: 2種類の実装を提供。openraft は非同期で本番向け、raft-rs はシミュレーション用。  
  - Walrus WAL: 独自のWrite-Ahead Log。二相コミット＋デュアルトピック（main/recovery）で途中クラッシュに対する耐性を持つ。復旧時はコミットマーカーのあるエントリのみ可視化する設計。  
  - QUIC（Quinn）: 暗号化・多重化されたトランスポートを採用し、コネクションプール管理も行う。  
  - 決定論的シミュレーション（DST）: 時間・I/O・ネットワーク・乱数を抽象化し、故障注入を制御可能。シードで再現性を担保。FoundationDB や TigerBeetle の手法に近い。  

- シミュレーションの中身（重要ポイント）  
  - 時間: 実運用は tokio::time::Instant、シミュレーションは制御可能な SimInstant。  
  - 乱数: 実環境はシステムRNG、シミュでは固定シードの XORshift（SimRng）で決定論的挙動。  
  - ファイルI/O: 実運用は実FS、シミュはVFSで部分書き（torn pages）やfsync失敗を注入。  
  - ネットワーク: QUIC/TCP 実装と、メモリ内でのパーティション・遅延注入を切り替え可能。  
  - 検証: 一貫性・耐久性（DurabilityOracle）・Raft不変条件・復旧の冪等性などを自動検査。

- テストカバレッジと運用性  
  - 11,000+ 行のテスト、複数カテゴリ（I/O故障・ネットワーク分断・複合故障・多サイクルクラッシュ）を複数シードで実行。  
  - デフォルトは各カテゴリ50シード・1回あたり1,000操作（ストレスは5,000）。環境変数 CLUSTER_SEED_COUNT で拡張可能。  

- 実装者向けポイント  
  - カスタムStateMachineは StateMachineTrait を実装すれば、決定論的にレプリケーション可能。  
  - 二相コミット＋デュアルトピックのモデルは、部分書き込みや中断に強い設計思想で、特にディスクの整合性が重要な用途で効く。

- 利用コマンド（抜粋）  
  - 実行例（openraft機能でノードを立てる）:

```rust
use octopii::{Config, OctopiiNode, OctopiiRuntime};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let runtime = OctopiiRuntime::new(4);
    let config = Config {
        node_id: 1,
        bind_addr: "127.0.0.1:5001".parse()?,
        peers: vec!["127.0.0.1:5002".parse()?],
        wal_dir: "./data/node1".into(),
        is_initial_leader: true,
        ..Default::default()
    };
    let node = OctopiiNode::new(config, runtime).await?;
    node.start().await?;
    node.propose(b"SET key value".to_vec()).await?;
    let value = node.query(b"GET key").await?;
    println!("Value: {:?}", String::from_utf8(value.to_vec()));
    Ok(())
}
```

- テスト実行例:  
  - 標準: cargo test --features openraft  
  - DST（故障注入）: cargo test --features simulation  
  - さらにシード数増加: CLUSTER_SEED_COUNT=200 cargo test --features simulation

## 実践ポイント
- まずはローカルでシミュレーションを動かす：--features simulation を使い、少数シードで挙動を把握。再現シードを控えてバグ報告に添える。  
- 単体のStateMachineを実装して決定論的に動くことを確認することで、本番移行前の安全域を拡大できる。  
- Walrusの二相コミットモデルは「中途半端な書き込みを見えなくする」ので、ディスク障害の多い環境（オンプレ・エッジ）で有効。設計に採り入れる価値が高い。  
- CIにDSTを組み込む：短時間のシードセットをCIで回し、定期的にシード数を増やすことで回帰と確率的バグ検出を両立する。  
- 日本の金融・組込系プロジェクトでは、再現性のあるクラッシュテストが監査・安全基準の説明材料として有用になる。

参考: Octopii リポジトリは Apache-2.0 ライセンス、Rustベース。興味があれば examples と docs（ARCHITECTURE.md / CUSTOM_STATE_MACHINES.md / SHIPPING_LANE.md）から始めると実装と検証の流れが掴みやすい。
