---
layout: post
title: "Read Locks Are Not Your Friends - 読み取りロックは友達じゃない"
date: 2026-02-22T22:51:00.326Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eventual-consistency.vercel.app/posts/write-locks-faster"
source_title: "Read Locks Are Not Your Friends"
source_id: 943558997
excerpt: "RwLockの読取りがApple SiliconでMutexより遅い驚きの原因と実践対策"
---

# Read Locks Are Not Your Friends - 読み取りロックは友達じゃない
読込ロックが性能を壊す？Rustで作ったキャッシュが教える「意外なボトルネック」

## 要約
Rustで書いたLRUテンソルキャッシュのベンチで、parking_lot::RwLock（読み取りロック）がMutexより約5倍遅かった。原因はリーダーカウントを巡るキャッシュラインの「ピンポン（cache line ping-pong）」による原子操作の争奪。

## この記事を読むべき理由
ロック設計は「ドキュメント通りに読みに行けば速くなる」という常識が通用しないことがあります。特にApple Siliconをはじめとするマルチコア環境で、短いクリティカルセクションを並列化しようとしたときに逆効果になる実例は、日本の開発者が性能トラブルを避ける上で役立ちます。

## 詳細解説
- 実験環境と目的  
  - ハード：Apple Silicon M4（10コア）  
  - 言語：Rust 1.92、parking_lot::RwLock  
  - 目的：LRUキャッシュの .get() スループット最大化（通常のgetは内部状態を更新するため書き込みが必要だが、ここでは「読み取り扱い」で高速化を試みた）

- なぜ期待は外れたか（技術的なコア）  
  1. 見えない「書き込み」  
     - RwLockの.read()でも内部で「現在のリーダー数」を増減するために原子操作（atomic increment）が発生する。実際には読みでも書きが発生している。  
  2. キャッシュラインと無効化のコスト  
     - CPUは64バイト単位でデータ（キャッシュライン）を扱う。リーダーカウントが同じキャッシュラインにあると、複数コアがそれを頻繁に変更し合い、キャッシュラインが各コア間で移動・無効化される（ping-pong）。  
  3. 性能の死の螺旋  
     - キャッシュのルックアップ自体が非常に短い（ナノ秒オーダー）場合、実際の仕事よりも原子加算のためのキャッシュ争奪に時間を取られる。結果として多数のスレッドで並列読みにしても帯域（メモリバス）がボトルネックになり、排他する一つの書き込みロック（Mutex）の方が効率的になることがある。

- なぜWrite Lockが「静か」に見えるか  
  - 書き込みロックは排他を保証するため、リーダーカウントの連続的な原子更新競合が起きず、短時間で処理して解放する方がハードウェア的に効率的な場合がある。

- 元コードの例（概念）  
```rust
pub fn get_with_write(&self, key: &str) -> Option<Arc<Tensor>> {
    let mut inner = self.inner.write();
    inner.get(key)
}

pub fn get_with_read(&self, key: &str) -> Option<Arc<Tensor>> {
    let inner = self.inner.read();
    inner.map.get(key).map(|(t,_,_)| t.clone())
}
```

## 実践ポイント
- プロファイルを必須にする：perf、cargo-flamegraph などで atomic_add やキャッシュ争奪を確認する。  
- クリティカルセクションが短ければ Mutex を試す：ナノ秒単位の処理なら RwLock のオーバーヘッドで負けることがある。  
- シャーディングを検討する：大きなキャッシュを複数バケットに分け、それぞれ別ロックにすることで争奪を減らす。  
- 代替手段：DashMap のようなシャーディング済みコンテナや、リードが長く重い場面では RwLock を有効活用する。  
- 実運用HWで検証する：開発マシン（Apple Silicon）と本番（クラウドCPU）は挙動が異なるため、本番に近い環境で必ず測る。

日本の開発現場でも、ローカル開発がApple Silicon中心になっていることが多く、この種のハードウェア依存の落とし穴は無視できません。まずは「測る」ことから始めてください。
