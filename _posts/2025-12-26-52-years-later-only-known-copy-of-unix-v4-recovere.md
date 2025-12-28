---
layout: post
title: "52 years later, only known copy of Unix v4 recovered from randomly found tape, now up and running on a system — first OS version with kernel and core utilities written in C"
date: 2025-12-26T03:51:00.246Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.tomshardware.com/software/linux/unix-v4-recovered-from-randomly-found-tape-at-university-of-utah-only-known-copy-of-first-os-version-with-kernel-and-core-utilities-written-in-c"
source_title: "52 years later, only known copy of Unix v4 recovered from randomly found tape, now up and running on a system — first OS version with kernel and core utilities written in C"
source_id: 438157045
---

# 「テープからよみがえった“元祖Cカーネル”──52年ぶりに発見されたUnix v4が語る“移植性”の起源」

## 要約
1970年代初頭に作られたUnix v4の唯一既知のコピーが、大学で見つかった古いテープから復元され、当時のマシン（エミュレータ上）で動作することが確認された。Unixカーネルと主要ユーティリティがCで書かれた最初期の実例として、OS史とソフトウェア保存の重要なマイルストーンだ。

## この記事を読むべき理由
OS設計、プログラミング言語の進化、ソフトウェア保存に関心がある技術者にとって、この発見は「現物」のコードから学べるまたとない機会。特に日本の教育機関やレガシーシステムを扱う現場では、移植性や可読性の価値を再確認する材料になる。

## 詳細解説
- 発見の概要：アメリカの大学で偶然見つかった磁気テープから、Unix v4の唯一既知のコピーがデジタル化・復元され、実機（通常はPDP-11のエミュレータ）でブート・実行できる状態になったと報じられている。
- 技術的意義：Unix v4はカーネルとコアユーティリティがC言語で実装された最初期のOSの一つ。アセンブリに依存しない実装は、ハードウェアの違いを吸収しやすくし、「移植可能なOS」というコンセプトを実証した。これはC言語とUNIX哲学がコンピュータ業界全体に与えた影響の根幹にあたる。
- 実行環境と復元作業：復元にはテープ読み取り、データ転送、ディスクイメージ生成、そして現代のエミュレータ（例：SIMH等）でのブート検証が必要になる。古いファイル形式やブロック構造を解釈するためのツールチェインと、失われかけたメタデータを推測するリバースエンジニアリング技術が重要だったはずだ。
- 歴史的文脈：1970年代のUnixは研究機関から広まり、後の商用UNIXやBSD、Linuxに至る思想や実装技術の源流となった。v4の復元は、「原典コード」を通じて当時の設計決定や制約（例えばメモリの限界やプロセス管理の実装）を直接検証できる貴重な資料を提供する。

## 実践ポイント
- 教育利用：OSやコンパイラの授業で実際のv4ソースを教材にすることで、現代言語と古典的実装のギャップを学べる。まずはエミュレータ（SIMH）環境でブートしてみるのが手軽な第一歩。
- レガシー対応の示唆：ハード依存コードを最小化する設計は現代システムにも有効。移植性を高めるための実践（抽象化レイヤ、ビルドシステムの整理、テスト自動化）を見直す契機に。
- 保存・公開の協力：大学や企業に眠る古いメディアの調査・デジタル化は価値ある活動。法的・所有権の確認を行い、可能であればアーカイブに寄贈・公開することを検討する。
- コミュニティ参加：国内外のレトロコンピューティング／コンピュータ歴史コミュニティに参加し、復元ツールや手順、経験を共有すると学びが早い。

