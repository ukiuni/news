---
layout: post
title: "How I ported Doom to a 20-year-old VoIP phone - 20年前のVoIP電話にDoomを移植した話"
date: 2026-02-23T20:28:01.387Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://0x19.co/post/snom360_doom/"
source_title: "Running Doom on a 20-Year-Old Snom 360 Office Phone | 0x19"
source_id: 398299506
excerpt: "ファーム解析からシェル取得・表示ドライバ作成でSnom360にDoom移植"
---

# How I ported Doom to a 20-year-old VoIP phone - 20年前のVoIP電話にDoomを移植した話
Snom 360でDoomを動かすまでの、レガシー機器ハック入門

## 要約
2005年のSnom 360（MIPS＋Linux 2.4）にファーム解析→シェル取得→ディスプレイ/入力ドライバを書いてDoomを移植した実況記。古いVoIP機器でも「読み解く力」とツールがあればゲームが動くことを示す実例。

## この記事を読むべき理由
- レガシー組込み機器の解析手順が分かる（binwalk→抽出→カーネル判定→GPL入手→クロス環境→u‑boot経由でフラッシュ）。
- 日本の企業や中小でまだ使われている古いIP電話の解析・保守や趣味ハックに直結するノウハウが得られる。

## 詳細解説
- 対象機種：Snom 360（2005）。ファームはV07/V08系を利用。webアップデート用の.binイメージを取得。
- 解析手順：binwalkで確認するとJFFS2ルートファイルシステムが含まれており、抽出でrootfsやboot/uImage（Linux 2.4.31、MIPS）を得られた。/mntのバイナリはELF MIPS32で静的リンク。
- GPL資源：SnomのGPL配布からv7のrootfs、BusyBox、カーネル/UBoot、クロスコンパイラ等を入手。これによりビルド環境とmkfs.jffs2が手に入る。
- カスタムイメージ作成：rootfsを編集してmkfs.jffs2でイメージを作成。古い機種はフラッシュが4MBなど容量制約がある点に注意。
- シリアルコンソール取得：筐体のテストポイントを探してGND/Tx/Rxを特定し、Serial→U‑Bootコンソールに接続（115200や9600などのボーレートを試す）。U‑BootでTFTPを使いイメージをロードしてフラッシュ。
- 起動後環境：BusyBox v1.2.2と限定的なユーティリティでシェルが得られる。標準のユーザランドが小さく、追加ツールやライブラリが必要なケースが多い。
- Doom移植の核心：ディスプレイ・入力・LED・バックライトなどハード固有部分を逆解析して独自ドライバを作成。既存のヘッドレスDoom移植実装に合わせてDG_Init／DG_SleepMs／DG_GetTicksMs／DG_SetWindowTitle／DG_GetKey／DG_DrawFrameといった抽象化層を実装し、フレームバッファ描画とキー処理を紐付けることで動作させた。
- ビルドと最適化：MIPS向けクロスコンパイル、バイナリの圧縮やサイズ調整（UPX等）でフラッシュ容量に収める工夫が必要。

## 実践ポイント
- 必携ツール：binwalk、Ghidra/逆コンパイラ、串刺しシリアルアダプタ、TFTPサーバ、mkfs.jffs2、クロスコンパイラ、BusyBoxソース。
- 流れ（初心者向け簡易版）：
  1. ファームイメージを取得してbinwalkで解析 → JFFS2抽出
  2. boot/uImageでアーキテクチャ（MIPSなど）とカーネルを確認
  3. SnomのGPL配布からrootfs/kernel/ツールを取得
  4. クロス環境で必要バイナリをビルド、mkfs.jffs2でイメージ作成
  5. 筐体のテストポイントからシリアルを探しU‑Bootへ接続、TFTPでフラッシュ
  6. シェル取得後、ハード周り（表示・キー）を解析して移植層を実装
- 注意点：フラッシュ書き換えは機器を壊す可能性あり。会社保有機器や商用機は許可を得て行うこと。GPLソースの利用条件を遵守すること。
- 学び：古い組込み機器ほど「解析→抽象化（デバイス層）→移植」のパターンが効く。日本の社内で眠る旧IP電話が格好の学習対象になり得る。

（元記事: "How I ported Doom to a 20-year-old VoIP phone" — 0x19）
