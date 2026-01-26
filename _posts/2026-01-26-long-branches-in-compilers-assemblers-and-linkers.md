---
layout: post
title: "Long branches in compilers, assemblers, and linkers - コンパイラ／アセンブラ／リンカにおける「長距離分岐」問題"
date: 2026-01-26T04:39:13.858Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://maskray.me/blog/2026-01-25-long-branches-in-compilers-assemblers-and-linkers"
source_title: "Long branches in compilers, assemblers, and linkers | MaskRay"
source_id: 418584308
excerpt: "巨大バイナリで分岐が届かず壊れる原因とコンパイラ／アセンブラ／リンカの具体的対処法を解説"
---

# Long branches in compilers, assemblers, and linkers - コンパイラ／アセンブラ／リンカにおける「長距離分岐」問題
巨大バイナリで「呼び出し先が遠すぎて命令に収まらない」――そんな地味で致命的な問題をツールチェーンがどう吸収するかをやさしく解説。

## 要約
命令の分岐は多くのアーキテクチャでPC相対の有限レンジを持つため、大きな実行ファイルでは分岐先が届かずリンクエラーや性能低下が起きる。コンパイラ・アセンブラ・リンカはそれぞれ異なる段階で「分岐の延長（relaxation／thunk）」を解決する。

## この記事を読むべき理由
大規模サービスや組込み・ファームウェア開発、RISC-V/AArch64の採用が進む日本の現場では、知らぬうちに「分岐レンジ問題」でビルドが壊れたり実行性能に影響が出る。対策の仕組みを理解するとトラブル回避や最適化ができる。

## 詳細解説
- なぜ起きるか：多くのCPUは分岐命令に「現在位置からの相対距離」を小さいビット幅でしか持たない。距離が超えるとその命令ではジャンプできない。
- アーキテクチャ差：代表例を抜粋すると、AArch64の関数呼び出しは ±128MiB、RISC‑Vのjalは約 ±1MiB（小さい）、x86‑64のnearは ±2GiB（大きい）。RISC‑Vや一部の組込みISAでは特にレンジが短いため頻繁に問題になる。
- どの段階で解くか：
  - コンパイラ（IR→アセンブリ）：関数内や小範囲の条件分岐が届かないとき、条件を反転して短い条件分岐＋無条件ジャンプを挿入する（branch relaxation）。
  - アセンブラ（アセンブリ→オブジェクト）：同一セクション内で距離がわかっている場合、より長いエンコーディングに差し替える（instruction relaxation）。
  - リンカ（最終配置時）：オブジェクト間やセクション間で届かないと判明した場合、リンカが小さな「thunk／veneer／trampoline」を生成して元命令をそこへ向けさせる。
- thunkの種類：短いthunk（短い分岐命令しか含まない、チェーン可能）と長いthunk（間接分岐でほぼ任意距離に対応）。例（概念）：
  
  ```asm
  asm
  // 短いthunk（単純に別ラベルへ分岐）
  .Lthunk_dst:
      b target        // 元の分岐はこのthunkへ向く
  ```
  ```asm
  asm
  // 長いthunk（ページロード＋間接分岐で遠方を参照）
  .Lthunk_long_dst:
      adrp x16, target
      add  x16, x16, :lo12:target
      br   x16
  ```
- 実装上のポイント：コンパイラ側で楽観的に短い命令を出す（例：RISC‑Vでjalを出す）と、リンク時に多くのtrampolineが生まれる。GCC/Clangは別戦略（auipc+jalr）を使うこともある。LLVMには BranchRelaxation や各アーキテクチャ用のパスがある。

## 日本市場との関連
- モバイル／組込み（ARM/AArch64, RISC‑V）や家電向けファームウェアで特に顕著。国内SoCベンダやIoT製品のビルドでは注意が必要。
- Linuxサーバやクラウド（x86‑64）は範囲が広いため起きにくいが、静的リンクや巨大バイナリを作る場合はGoogle/Metaと同様の問題に直面する可能性がある。
- RISC‑V採用の増加により、ツールチェーン側の緩和機構やリンカのサポートが国内プロジェクトで重要になる。

## 実践ポイント
- ビルドで問題が出たらまずmapファイルやリンカエラーを確認し、「relocation out of range」などのメッセージを探す。
- 小さな対策
  - -ffunction-sections / -fdata-sections とリンカの --gc-sections を併用し、セクション分離で距離を縮める。
  - コンパイラ・アセンブラの最適化（branch relaxation を有効にする）や最新ツールチェーンを使う。
- 大きな対策
  - 必要ならリンカ（ld.lld や GNU ld）のrange-extension設定やトランポリン生成の挙動を確認する。
  - x86‑64ならコードモデル（small/large）を意識、RISC‑Vならコンパイラにauipc+jalr生成を選ばせるかリンカのtrampolineに頼るかを設計する。
- テスト：大規模バイナリを意図的に作ってリンクテストを行い、trampolineの数や位置をmapで把握する。

短く言えば：分岐の「届く/届かない」はコンパイルチェーン全体の協調問題。設計段階でレンジ制約を意識し、ツールチェーン設定を調整すればトラブルを未然に防げます。
