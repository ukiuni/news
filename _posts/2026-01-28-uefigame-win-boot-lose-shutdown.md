---
layout: post
title: "UEFIGame: \"Win -> Boot, Lose -> Shutdown\" - 「勝てば起動、負ければシャットダウン」"
date: 2026-01-28T17:11:03.004Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/mycroftsnm/UEFIGame"
source_title: "GitHub - mycroftsnm/UEFIGame: UefiGamePkg: Collection of UEFI games"
source_id: 1508692970
excerpt: "勝てば起動、負ければシャットダウンするUEFI学習用ミニゲーム集（UTF-16注意）"
image: "https://opengraph.githubassets.com/ad9d382588d0398edeb2aa9b3d9df9cab39d71f1897eb6b057057b482d3efb12/mycroftsnm/UEFIGame"
---

# UEFIGame: "Win -> Boot, Lose -> Shutdown" - 「勝てば起動、負ければシャットダウン」
UEFI上で遊べる“命がけ”ミニゲーム集 — 起動処理を賭けたレトロ感のあるハッカブルなプロジェクト

## 要約
UEFIファームウェア環境で動くミニゲーム群（Insult Sword Fighting、Age Verification、数学クイズ、Simon系など）。勝てば通常にブート、負ければシャットダウンするという遊び心あふれる実験的なパッケージ（GPL-3.0）。

## この記事を読むべき理由
UEFI/EDK IIの実践的な学習素材として使える上、ファームウェア領域でのアプリ実行・ブート管理・QEMUでの検証フローを実例で学べる。日本語化の際に注意すべきUTF-16要件もあるため、日本の組込み/ファームウェア開発者や趣味のPC改造層に有用。

## 詳細解説
- 構成と趣旨: UefiGamePkgは複数の独立モジュール（User Evaluation For Ineptness＝簡単な足し算、Insult Sword Fighting＝Monkey Island風の返し選択、Fall To Boot＝垂直スクロール、Age Verification＝80sトリビア、UEFI Says＝Simon系メモリゲーム）を含むEFIアプリ集。各モジュールは「勝つとBoot、負けるとShutdown」を挟んで動作。
- 実行環境: EDK IIベースのEFIアプリとしてコンパイルし、ESP（EFI System Partition）に配置して起動エントリを作るか、QEMU+OVMFで仮想環境で検証する。ビルドはedksetup.sh→buildコマンドで行う（例は下記）。
- ファイルとロケーション: 追加リソース（insults.txt, phrases.txt, questions.txt, failmessages.txt）はEFIアプリと同じディレクトリに置く。重要：これらのテキストはUTF-16で保存する必要がある（多言語化／日本語化時に要注意）。フォーマットは空行で区切るなど決まりがある。
- 内部実装ノート: 乱択で選択肢やフレーズを取る際にReservoir Samplingを使っている箇所があり、軽量でメモリ効率の良い実装がなされている。
- ライセンス: GPL-3.0。派生や配布には注意。

## 実践ポイント
- QEMUで先に試す（安全に何度でもテスト可能）。
  ```bash
  # QEMU起動例
  qemu-system-x86_64 \
    -drive if=pflash,format=raw,readonly=on,file=/usr/share/edk2/x64/OVMF_CODE.fd \
    -drive file=fat:rw:./uefi_disk,format=raw,if=virtio \
    -cpu qemu64,+rdrand
  ```
- 実機で試す手順（ESPへ配置 → efibootmgrでエントリ作成）
  ```bash
  # 例: EFIアプリとテキストをESPへコピー
  sudo mkdir -p /boot/EFI/UEFIGame
  sudo cp InsultSwordFighting.efi /boot/EFI/UEFIGame/
  sudo cp insults.txt /boot/EFI/UEFIGame/
  sudo efibootmgr --create --disk /dev/nvme0n1 --part 1 --loader '\EFI\UEFIGame\InsultSwordFighting.efi' --label "UEFIGame"
  ```
- 日本語化の注意: テキストファイルは必ずUTF-16で保存。日本語の回答やフレーズを入れるときは改行・空行区切りルールを守る。
- ビルドの基本コマンド例:
  ```bash
  source edksetup.sh
  build -p UefiGamePkg/UefiGamePkg.dsc -a X64 -t GCC5 -b DEBUG -m UefiGamePkg/InsultSwordFighting.inf
  ```
- セーフティ: 実機でテストするときはデータを残さない環境か、まずはQEMUで動作確認すること。  

このリポジトリはUEFIの学習、デモ、ちょっとしたジョーク用途に最適。日本語でコンテンツを追加する際はUTF-16とファイルフォーマットに気をつけるとスムーズに動作する。
