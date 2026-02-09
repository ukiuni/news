---
layout: post
title: "Reverse Engineering the PROM for the SGI O2 - SGI O2用PROMのリバースエンジニアリング"
date: 2026-02-09T04:33:47.540Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://mattst88.com/blog/2026/02/08/Reverse_Engineering_the_PROM_for_the_SGI_O2/"
source_title: "mattst88's blog - Reverse Engineering the PROM for the SGI O2"
source_id: 46939187
excerpt: "消えたSGI O2のPROMを逆解析し、900MHz対応化を可能にした実践手法と再構築ツールの全貌"
---

# Reverse Engineering the PROM for the SGI O2 - SGI O2用PROMのリバースエンジニアリング
消えたSGIの心臓部を解剖 — O2のPROMを読み解き、900MHz化の扉を開けた手法

## 要約
SGI O2のブートPROMをバイナリから逆解析し、再アセンブル可能な可読アセンブリに復元するツール（ip32prom-decompiler）を作成。PROM内部のセクション構造やチェックサム、関数境界の見つけ方を明らかにし、RM7900（900MHz）対応の改変を可能にした。

## この記事を読むべき理由
日本でも根強いレトロUNIX/ワークステーション愛好家や組込みファームウェアに関わる開発者にとって、「動かない古いハードを動かす」「ファームウェアを安全に改変する」ための実践的な逆解析手法が学べるから。

## 詳細解説
- 入手物と初手
  - 対象は 512 KiB の ip32prom.rev4.18.bin。まず `mips64-unknown-linux-gnu-objdump -D -b binary -m mips -EB` で逆アセンブルし、`strings` を併用して手がかりを得た。
- セクションヘッダ（"SHDR"）の発見
  - バイナリ内に "SHDR" マジックが複数回出現。ヘッダはブランチ＋遅延スロットを含めて72バイト程度と推定。
  - ヘッダはセクション名（例: sloader, env, post1, firmware, version）、バージョン、セクション長らしきフィールドを持つ。ヘッダ内の未知フィールドはタイプやフラグ／オフセットと思われる。
- セクション長とチェックサム
  - 各セクション末尾には「存在し得ない命令（bogus instruction）」があり、これがセクション長で切られる位置に一致。これらはおそらくセクションチェックサム。
- コード領域の復元と関数境界の検出
  - `jr ra` / `nop` の並びや典型的な戻り動作、レジスタの使い方から関数境界を推定。例：strlen相当のループ、tlb初期化ルーチン（tlb_init）などの識別。
  - レジスタ／CP0命令（mtc0/mfc0）を読み解き、CPU初期化処理（TLB、キャッシュ無効化、KSEG1ジャンプなど）を特定。
- 可読性改善と再構築
  - ip32prom-decompiler は定数の置換、アドレス→ラベル化、コメント生成、関数境界表示などを行い、.S（アセンブリ）へ出力。labels.json / comments.json / functions.json / operands.json / relocations.json / bss.json といった注釈ファイルで人間可読性を付与。
  - 生成したアセンブリは再アセンブルしてビット単位で一致するPROMイメージを得られることを検証（正確な逆解析の証明）。
- 結果的な応用
  - これにより、RM7900のサポートに必要なIP32 PROM改変が、SGI由来のソース無しで可能になった。

## 実践ポイント
- まずやること
  - バイナリ取得→`strings`→`objdump`で荒い分解→マジック／繰り返しパターンを探す。
- 便利なツール
  - mips objdump（クロスツールチェイン）、hexdump/xxd、strings、radare2/Ghidra、簡易スクリプト（Python）でパターン抽出。
- 解析のコツ
  - 関数終端（jr ra / move v0, ...）や典型的ループで境界を特定。文字列と数値を突き合わせてヘッダ構造を推定。
  - セクション末尾の「おかしな命令」はチェックサムやマーカーの可能性が高い。
- 安全な改変手順
  - まずエミュレータで動作確認→ビット同一性を保った再アセンブル→フラッシュ前に必ずバックアップを取る。
- コミュニティ活用
  - NekochanやSGI Depotのような既存の知見を参照し、変更はレトロコンピューティングコミュニティで検証すると成功率が上がる。

この記事で得られるのは「古いファームウェアを読み解き、改変して動作させるための実践的手順」と「どこを見れば構造が分かるか」を示す経験知です。興味があれば、元記事のip32prom-decompilerや注釈ファイルを追いかけると具体的な実装例が得られます。
