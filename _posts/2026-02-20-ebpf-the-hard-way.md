---
layout: post
title: "eBPF the Hard Way - eBPFを原始的に扱う方法"
date: 2026-02-20T14:59:33.105Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://feyor.sh/blog/ebpf-the-hard-way"
source_title: "eBPF the Hard Way | feyor.sh"
source_id: 1660978376
excerpt: "libbpf/Clang無しで生eBPFバイトコードを作りVerifierやBTFを攻略する実践ガイド"
---

# eBPF the Hard Way - eBPFを原始的に扱う方法
カーネルの奥を直接触る――libbpf/ClangなしでeBPFバイトコードを直書きして動かすための実践ノウハウ

## 要約
作者は「libbpf/LLVM/GCCに頼らず、bpf syscallへ生のバイトコードを渡す」ためのハウツーを提示。bpf syscallの流れ、Verifierの挙動、マップでのデータ受渡し、BTFとfunc_infoによる型情報の扱いまで、低レイヤーから検証ログを読み解く実践的手順を示します（Linux 6.18ベース）。

## この記事を読むべき理由
eBPFは観測・セキュリティ・パケット処理で重要性が急増中。libbpfで抽象化されている層を理解すると、Verifierのエラー原因が即分かり、NICオフロードや超低レイテンシ処理など日本のクラウド／ネットワーク事業者・組み込み開発で差別化できる実務スキルになります。

## 詳細解説
- ロードの流れ：ユーザ空間でeBPF命令列を作り、BPF_PROG_LOADサブコマンドでカーネルに渡し、ソケット／kprobe等にアタッチする。ロード時にVerifierへログバッファを渡せるので、失敗原因はまずこれを見る。
- Verifierの制約（代表例）：
  - 最大命令数は制限あり（例: 4096）
  - 無限ループ・後方ジャンプ（back edges）は原則禁止（bpf_loopなど特別な仕組みを要する）
  - サブプログラム（静的関数）を使う場合はfunc_info＋BTFが必要
  - 権限のないプロセスは使えるプログラム種類が限定（通常は socket filter / cgroup skb 等）
  - 多くのヘルパーやKFunc、特定機能はCAP_BPF / CAP_NET_ADMIN / CAP_PERFMON等の権限が必要
  - レジスタ定数のsanitizeや死コードの扱いなど、Verifierは多面的に最適化・制約を加える
- マップと読み取り専用文字列：ユーザ→カーネルの定数文字列を渡す場合、read-onlyマップ（BPF_F_RDONLY_PROG）に文字列を置き、VerifierがARG_PTR_TO_CONST_STRで検査できる形にする。プログラム側でmap_lookup_elemしてポインタを取得し、strncmp相当のヘルパーで比較するパターンが紹介されています。
- パケットフィルタ例：ソケットフィルタ（歴史的なBPFの起源）でskb_load_bytesを使ってパケットを部分読みし、文字列を検出したらDROPする例。挙動検証はsocketpairで簡易的に行う。
- BTF（BPF Type Format）：Verifierは型情報を検証に利用するため、サブプログラムの型シグネチャ（BTF_KIND_FUNC_PROTO）やfunc_info（サブプログラムのオフセット→type id）を与えないとコールバックやローカル関数を使えない。BTFはbpftool/pahole/clangで作るのが一般的だが、手作りで埋め込むことも可能（ただし面倒）。
- 実践中のトラブル：Verifierの「missing btf func_info」などは、サブプログラムやKFuncを使う際によく出る。ログのレベルを上げて詳細を確認すること。

## 実践ポイント
- まずはVM上で実験：カーネル6系など比較的新しい環境で再現性を確保する。
- Verifierログを必ず有効化：prog_load時にログバッファを渡して原因解析に使う（ログレベルを上げる）。
- 権限周りを確認：CAP_BPF/CAP_NET_ADMIN/CAP_PERFMONが必要なケースを把握する。無権限だと使えるprogram typeが限られる。
- 定数文字列はread-onlyマップに入れる：ARG_PTR_TO_CONST_STR要件を満たし、strncmp相当のヘルパーを正しく使う。
- BTFを用意する：サブプログラム／コールバックを使うならfunc_infoとBTF（またはbpftoolで自動生成）を準備する。
- 参考資料を併読：BPF ISA、bpf syscallリファレンス、btf仕様、ebpf.ioドキュメントを合わせて読むと理解が早い。
- 最初は高レベルツール（libbpf/clang）で動作確認→低レイヤーに落とす：差分を追うことでVerifierの挙動を学べる。

参考：元記事は実際のZigコード例やVerifier出力のサンプルを使って具体的に説明しています。まずは「小さなsocket filter」を自前で作り、Verifierログで詰まる箇所を潰す練習をおすすめします。
