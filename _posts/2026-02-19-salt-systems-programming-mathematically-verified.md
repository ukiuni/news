---
layout: post
title: "Salt: Systems programming, mathematically verified - Salt：システムプログラミングを数理的に検証する言語"
date: 2026-02-19T15:15:13.719Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://salt-lang.dev/"
source_title: "Salt: Systems programming, mathematically verified"
source_id: 974029229
excerpt: "Z3契約検証＋アリーナで実行時負荷ゼロ、C超性能の証明可能なシステム言語Salt"
image: "https://bneb.github.io/lattice/og_image.png"
---

# Salt: Systems programming, mathematically verified - Salt：システムプログラミングを数理的に検証する言語
クリックせずにはいられない：性能と安全性を両立した「証明されるシステム言語」Saltの全貌

## 要約
SaltはZ3によるコンパイル時契約検証＋アリーナメモリ＋MLIRコード生成で、ランタイムコストなしに「数学的に安全」を実現するシステム言語。ベンチマークでC相当またはそれ以上の性能を示します。

## この記事を読むべき理由
高性能なLLM推論、ベアメタルunikernel、低レイテンシネットワークなど、日本でも需要が高い「性能×安全性」を同時に達成できる技術だから。組み込み・クラウド・金融・ゲームなど性能と信頼性が必須の現場に直接刺さります。

## 詳細解説
- コア設計
  - コンパイル時証明：関数にrequires()/ensures()を書き、コンパイラがZ3で全呼び出し箇所を証明。未証明ならビルド失敗。実行時オーバーヘッドなし。
  - アリーナメモリ：GCや借用検査を使わず、領域単位で割当て・一括解放。コンパイラが参照の領域越えを証明し排除。
  - MLIRコード生成：MLIR経由でハードウェア最適化を行い、ループのタイル化などでclang -O3を凌ぐ場合も。
- 言語体験
  - パイプ演算子(|>), エラー伝播(|?>), f-strings、明示的なunsafe境界、@trustedでFFIを管理。
  - 標準で多くのモジュールを備え、依存は最小限（spパッケージマネージャ）。
- 実例プロジェクト（短く紹介）
  - Basalt：Llama 2推論エンジン。メモリマップ、MLIRタイル化、Z3で配列境界検証。数百行で実装。
  - Lattice：x86ベアメタルunikernel。GDT/IDT/PIT/プリエンプティブスケジューラ等をSaltのみで実装。
  - Sovereign Train：MNIST学習器をSaltで実装。配列アクセスはZ3で検証。
  - Lettuce：Redis互換インメモリDB。ゼロコピーRESP、アリーナハッシュテーブルで高スループット。
  - FACET：Metalバックエンドを使った2Dレンダラ。ピクセル書き込みの検証付き。
  - C10Mベンチ：kqueueベースの高接続負荷でもCと同等のスループット。
- ベンチマークと再現性
  - 22ベンチ全てでclang -O3と同等か上回ると主張。プラットフォームや手法は公開済み。
- ライセンスとエコシステム
  - MITでオープン。spでプロジェクト作成→sp run→sp checkの流れが短時間で済む。

## 実践ポイント
- トライアル手順：sp new でプロジェクト作成、sp runで実行、sp checkで契約検証を試す。まずはサンプル（BasaltやLettuce）を動かす。
- 取り入れ候補領域：LLM推論カーネル、ベアメタル/unikernel、ネットワーク・高頻度処理、GPUでの数値カーネル。パフォーマンスと静的安全性が同時に求められる箇所に適合。
- 注意点：エコシステムはまだ若く、ライブラリ互換性や運用周り（デバッグツール、IDE統合）は成熟度検証が必要。unsafe境界とFFI部分は設計注意。
- 次の一歩：ソースとベンチ、ビルド手順が公開されているので、まずはローカルでサンプルをビルドしてZ3契約の感触を掴む。

Saltは「証明可能な安全性」をパフォーマンスと共に実運用に持ち込もうとする挑戦的な言語です。日本の高信頼・高性能分野での実践導入検討に値します。
