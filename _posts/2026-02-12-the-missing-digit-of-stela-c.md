---
layout: post
title: "The missing digit of Stela C - ステラCの欠けた桁"
date: 2026-02-12T10:09:43.916Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://johncarlosbaez.wordpress.com/2026/02/12/stela-c/"
source_title: "Stela C | Azimuth"
source_id: 46986248
excerpt: "ツォルキンと合同算で解明、欠けたStela Cの先頭桁が「7」と断定された経緯"
image: "https://johncarlosbaez.wordpress.com/wp-content/uploads/2026/02/a-colossal-stone-head-from-the-olmec-civilization.jpg"
---

# The missing digit of Stela C - ステラCの欠けた桁
古代の石碑が「7」を告げた瞬間――カレンダーと合同式で読み解くStela Cの真相

## 要約
石碑「Stela C」に刻まれた長期暦（Long Count）の先頭桁が欠けていたが、別の暦（ツォルキン）の刻みが手がかりになり、欠けた桁が確実に「7」であると当初の発見者が正しく推定できた話。

## この記事を読むべき理由
暦の表記と簡単な数論（合同算）で歴史年の特定が可能になる実例は、ソフトウェアやデータ変換に親しむ日本の技術者にも学びが多い。カレンダー換算や周期性の扱いは実務でも役立つ基礎知識だ。

## 詳細解説
長期暦（Mesoamerican Long Count）は位置表記で日数を表す仕組みで、主な単位は
- baktun = 144000日
- katun = 7200日
- tun = 360日
- uinal = 20日
- kin = 1日

石碑に読み取れた下位5桁は $7.16.6.16.18$（実際は先頭桁が欠けて見えた場合は $(B).16.6.16.18$）で、これは日数に直すと次のようになる：

$$
7\times144000 + 16\times7200 + 6\times360 + 16\times20 + 18 = 1{,}125{,}698
$$

この Long Count を西暦暦日と結びつけるために「Mayan correlation（GMT 相関）」という定数 $C=584\,283$ を足すとユリウス日（Julian Date）になり、得られる日付は紀元前32年9月（暦の扱いによっては9月1日=proleptic Gregorian、9月3日=proleptic Julian）になります。

ここで Stirlings（発見者夫妻）がどうして最上位桁を「7」と断定できたか――鍵はツォルキン（Tzolkʼin）暦です。ツォルキンは260日周期で、13の番号（数）と20の名前（語）が組み合わさります。石碑の下半部には Long Count の下位桁に加え、ツォルキンの日付「6 Etzʼnab」が読めました。

重要な合同算の観点：
- 20種類の名前は baktun の増減に影響しない（$144000\equiv0\pmod{20}$）。
- しかし13種類の番号には影響がある。$144000 \bmod 13 = 12 \equiv -1$ なので、baktun を 1 増やすとツォルキンの番号は $-1$（つまり1減る）向きに変わる。

したがって、下位桁が固定された状態で「番号が6で名前がEtzʼnab」になるようにする baktun の値は、ある特定の合同類に一意に限定され、次に同じ組が現れるのは $13$ baktun（約5094年）後です。つまり欠けた桁は当時の文化的・年代的事情を勘案しても「7」以外あり得ないと結論できたのです。発見から30年後、下半分の残片が発見され実際に「7」であることが確認されました。

※暦変換や「proleptic（仮想的延長）」の扱いで1–2日の差が出る古典的な議論はあるが、論理の肝は周期と合同式の一致にある。

## 実践ポイント
- Long Count ⇄ 西暦変換は日数化→定数 $C$ を足す→暦変換、という手順で実装できる。式は上記参照。
- ツォルキンのような周期の組合せ問題は合同算（mod 演算）で素早く判定できる。$144000\equiv-1\pmod{13}$ のように単位ごとの剰余を計算してみると直感がつく。
- 実際に試すなら Emacs のカレンダー（M-x calendar, ‘p m’ で Mayan 表示）は手軽なツール。自前で確認するならユリウス日変換ライブラリやスクリプトを用意すると良い。
- 考古と数理は相性が良い：欠損データの補完や矛盾検出に、プログラミングと数論の基本がすぐ役立つ。

（元記事：The missing digit of Stela C — John Baez）
