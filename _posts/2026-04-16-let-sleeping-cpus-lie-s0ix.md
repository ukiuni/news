---
layout: post
title: "Let Sleeping CPUs Lie — S0ix - 眠っているCPUはそのままに — S0ix"
date: 2026-04-16T08:36:25.167Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://freebsdfoundation.org/our-work/journal/browser-based-edition/laptop-desktop/let-sleeping-cpus-lie-s0ix"
source_title: "Let Sleeping CPUs Lie — S0ix | FreeBSD Foundation"
source_id: 1737776288
excerpt: "S0ixによるノートPCの常時接続と極低消費電力を実現、復帰高速化やOS/ドライバ対応の重要性を解説"
---

# Let Sleeping CPUs Lie — S0ix - 眠っているCPUはそのままに — S0ix
ふたを閉じても勝手に起きない「スマートな睡眠」――S0ixがもたらすノートPCの省電力革命

## 要約
S0ixは従来の「完全サスペンド（S3）」と異なり、システムを「起きている状態のまま深い低消費電力へ移行」させる仕組みで、常時接続性と極低消費電力を両立する。近年のノートではS3よりS0ixが主流になりつつある。

## この記事を読むべき理由
スマホ的な常時接続や素早い復帰を求める日本のユーザー／開発者にとって、S0ixの理解はバッテリー運用やOS対応（例：FreeBSD）を議論するうえで必須です。

## 詳細解説
- 背景：歴史的にはSMM→APM→ACPIと進化し、ACPIのS状態（S0,S3,S4,S5）で電源管理を扱ってきた。S3はRAMに状態を残すが復帰にコストが高い。
- S0ixとは：2018年頃からIntelが導入したS0内の低消費電力状態群（S0i1 / S0i2 / S0i3）。システムは論理的にはS0（起床）だが、CPUパッケージやデバイスを深く寝かせる。
- エントリ条件：ファームウェア（SPMC / PEP）が示す最小D-state（デバイス電源状態）を満たすことと、全CPUが低消費C-stateでアイドルすること（s2idle）をOSが作ること。
- デバイス側：D0（オン）→D3hot/D3coldのようにデバイスを部分的に切る必要があり、DSM（Device-Specific Method）経由でSPMCとやり取りする。USB4やGPUはS0ixで特別な扱いが必要なことが多い。
- CPU側：スケジューラ時計を止め、割り込みをSCIs（ACPIのSystem Control Interrupt）だけに限定してs2idleループへ入る。割り込みで起きたGPEを見て「本当に復帰すべきか」を判断できる。
- ベンダー差分：AMDはPMFW（SMU/MP1）上でパッケージ電源制御を行い追加要件がある。SMUはS0i3の成否を報告し、FreeBSDでは dev.amdsmu.* のsysctlで確認できる。
- 実運用の例：FrameworkノートではECのGPE頻度をsuspendのヒントで落とし、頻繁な不必要な復帰を抑えている。
- なぜS3が減ったか：ハードウェアとOS両対応が必要で実装が複雑なため。多くの現行機はS0ixを前提に設計されている。

## 実践ポイント
- 自分の環境でs2idle/S0ixが使えるか：FreeBSDでは kern.power.supported_stype を確認。hw.acpi で設定可能。
- AMD機は dev.amdsmu.* sysctl を見てS0i3のログ/理由を確認する（成功/失敗の原因特定）。
- USB4やGPU周りはドライバ側の対応が必要。特にUSB4コントローラはNHIドライバで電源管理されるか確認。
- ラップトップのWakeデバイス設定（lid, power button, RTC）を見直し、不要なGPEを抑えることでS0ix効果が上がる。
- S3非対応機が増えているため、古い“S3で問題無かった”前提は通用しないと考える。

（参考元: FreeBSD Foundation記事「Let Sleeping CPUs Lie — S0ix」）
