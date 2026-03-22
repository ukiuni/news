---
layout: post
title: "My first patch to the Linux kernel - Linuxカーネルへの初パッチ"
date: 2026-03-22T07:57:18.635Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://pooladkhay.com/posts/first-kernel-patch/"
source_title: "my first patch to the linux kernel"
source_id: 47444909
excerpt: "符号拡張ミスでTSSベースが壊れカーネルがハング、単純キャストで直せた話"
---

# My first patch to the Linux kernel - Linuxカーネルへの初パッチ
64ビット環境で起きた「符号拡張」の落とし穴――初めてのカーネルパッチが教えてくれたこと

## 要約
Type‑2ハイパーバイザ実装中に、TSSベースアドレスを組み立てる際のCの整数昇格と符号拡張が原因で不定なホストスタックアドレスが設定され、コアの死活停止や全体のハングを引き起こした。原因特定と修正は単純なキャストの追加だった。

## この記事を読むべき理由
仮想化は日本のサーバ／クラウド運用で当たり前の技術であり、カーネル/ハイパーバイザ周りの細かいC言語の挙動が実機で致命的になる例は、初級者が学ぶべき実戦的な教訓だから。

## 詳細解説
- 背景：x86-64ではカーネルはコアごとにTSS（Task State Segment）を持ち、TRレジスタの隠れた部分（Base, Limit, Access）によりCPUが素早くTSSにアクセスする。ハイパーバイザはホスト・ゲストのTR情報をVMCSに保存／復元する必要がある。
- 症状：VM-exit 後にNMI等でTSSからカーネルスタックを取得しようとして、読み出し先がゴミまたは未マップになりページフォルト→オップス→割り込み不能な「ゾンビCPU」が生まれ、IPI待ちでシステム全体がデッドロックに陥った。
- 根本原因：TSSセグメント記述子は base0 (16bit), base1 (8bit), base2 (8bit), base3 (32bit) を繋げて64bitベースを作る必要があるが、元の実装は小さい型をそのままシフトしていた。Cの整数昇格により8bitなどが32bitの符号付きintに昇格し、左シフト後に uint64_t にキャストされる際に符号拡張が起き、上位32ビットが 1 で埋まって base3 を破壊してしまった。
  - 例：期待値 $0xfffffe7cf8d65000$ が、符号拡張により $0xfffffffff8d65000$ になってしまうケースが発生（base2 の MSB が 1 のときのみ）。
- 探索過程：問題はマルチコア移動時にのみ再現し、仮想環境（vCPUs）や実機での違いからTSS/TR周りに絞り込み、最終的にget_desc64_baseの実装ミスに到達。
- 修正：シフト前に各部品を符号なしの大きな型にキャストするだけで解決。

修正された関数（要点）:

```c
/* C */
static inline uint64_t get_desc64_base(const struct desc64 *desc)
{
    return (uint64_t)desc->base3 << 32 |
           (uint64_t)desc->base2 << 24 |
           (uint64_t)desc->base1 << 16 |
           (uint64_t)desc->base0;
}
```

## 実践ポイント
- ビット結合の前に必ず適切な符号なし型にキャストする（特に小さな整数型 → シフトする場合）。
- マルチコア／実機でのテストは必須。tasksetでコア固定して動くが移動で壊れる、は重要なヒント。
- カーネルや低レイヤ実装では、get_cpu_entry_areaやカーネル既存のper-cpu APIを優先利用する（KVM本体はその方法を使っている）。
- コンパイラ警告（-Wconversion, -Wsign-conversion）や静的解析ツールを有効にしておく。
- 類似バグ検出のため、ログに「NMI→ページフォルト→CPU停止」の連鎖パターンを監視すると早期発見につながる。

（参考）著者が送ったパッチ: https://lore.kernel.org/kvm/20251222174207.107331-1-mj@pooladkhay.com/
