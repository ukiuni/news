---
layout: post
title: "lshaz: a static analysis tool for finding microarchitectural latency hazards - lshaz：マイクロアーキテクチャのレイテンシ障害を検出する静的解析ツール"
date: 2026-03-23T01:20:26.001Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://abokhalill.github.io/lshaz-writeup/writeups/abseil-deep-dive/"
source_title: "We ran lshaz on Abseil. Here's what compile-time microarchitectural analysis actually finds in production C++. | lshaz"
source_id: 416918958
excerpt: "静的解析でコンパイル時に隠れたキャッシュ競合を発見しC++遅延を可視化"
---

# lshaz: a static analysis tool for finding microarchitectural latency hazards - lshaz：マイクロアーキテクチャのレイテンシ障害を検出する静的解析ツール
心臓部の“キャッシュライン争い”をコンパイル時に見つけ出す──あなたのC++が静かに遅くなる原因を暴く一手

## 要約
Clang/LLVMベースの静的解析ツール「lshaz」は、構造体のフィールド配置やアトミック操作によるキャッシュライン競合（false sharing）や原子競合など、コンパイル時に見落とされがちなマイクロアーキテクチャ上の遅延要因を検出する。Abseilに対する適用で実用的な問題点を複数発見している。

## この記事を読むべき理由
日本のミッションクリティカルなサービスや低レイテンシを求めるシステム開発では、ソースは正しく見えてもハードウェア側での「知られざる」遅延が性能を圧迫することが多い。lshazはそれらを事前に洗い出し、最小のコストで効果的な修正案を示すため、運用中のC++コードやライブラリ改善に直結する知見を得られる。

## 詳細解説
- ツールの仕組み  
  lshazはClang/LLVMのAST（ASTContext, ASTRecordLayout）を使って構造体のフィールドオフセットを算出し、15種類のルールでマイクロアーキテクチャの「ハザード」を検出する。誤検出を抑えるためにオプションでIR（中間表現）まで追い、最適化後のIRにハザードが残るかで「検証済み（proven）」か「推定（likely/speculative）」かを切り分ける（--no-irでIRパス無効化可）。
- Abseilに対する結果の要点  
  157翻訳単位で352件の診断、クリティカル層で18件のFL002（false sharing）などを報告。Googleのハード寄りにチューニングされたライブラリでも実用的なホットスポットが見つかったことが示唆される。
- 代表的な検出事例  
  1) HashtablezInfo：複数のstd::atomicフィールドが3つのキャッシュラインに跨って配置され、40件以上のペアワイズなfalse sharingを誘発。修正は熱いカウンタを同一キャッシュラインにまとめる（例：alignas(64)でグループ化）。  
  2) ThreadIdentity：ticker（スレッド自身が頻繁更新）と他スレッドが書くフィールドが同一ラインにありキャッシュのping-pongを発生。設計上のトレードオフと明記されていたが、ツールは「意図的なコスト」を可視化した。tickerを独立ラインに移すだけで影響を解消できる。  
  3) MutexGlobals：構造体にABSL_CACHELINE_ALIGNEDが付与されていたが、フィールド内部でspinloop_iterationsが隣接フィールドと同ラインにあり、全スレッドのスピン設定が無意味に無効化される。構造体内部でのフィールド隔離が必要。

- 拡張性と実運用性  
  lshazはC/C++をサポートし、Redis/PostgreSQL/LLVMなど他の大規模OSSでも有意な所見を出している。ソースは公開済み（https://github.com/abokhalill/lshaz）。

## 実践ポイント
- 自分のリポジトリで試す：lshazをビルドしてCIで実行。まずは--no-irでスキャンを回し、ホットパスに絞ってIR検証を有効化する。  
- ホットなアトミック群はまとめる：頻繁に更新されるカウンタを同一alignas(64)の領域にまとめる。例：
```cpp
// C++
struct alignas(64) HotCounters {
  std::atomic<size_t> capacity;
  std::atomic<size_t> size;
  // ...
};
```
- グローバル設定は内部フィールドも注意：struct単位のキャッシュライン整列だけでなく、内部フィールドの隔離（パディング／alignas）を検討する。  
- 意図的トレードオフを文書化：意図的に共有キャッシュラインを許す設計ならコメントで理由を残し、ツールのアラートを抑止（あるいはレビューで判断）する。  
- 測定で検証：変更後はマイクロベンチや実負荷で効果を確認。無駄なメモリ増加と引き換えに得たレイテンシ低減を数値で示す。

リポジトリと詳細は https://github.com/abokhalill/lshaz 。まずは自分のサービスで数ファイルを流してみることをおすすめします。
