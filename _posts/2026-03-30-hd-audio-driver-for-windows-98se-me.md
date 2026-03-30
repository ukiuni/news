---
layout: post
title: "HD Audio Driver for Windows 98SE / Me - Windows 98SE / ME 向け HD オーディオ ドライバ"
date: 2026-03-30T05:52:13.350Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/andrew-hoffman/wdmhda"
source_title: "GitHub - andrew-hoffman/WDMHDA: HD Audio driver for Windows 98SE / ME · GitHub"
source_id: 47570547
excerpt: "98SE/Meで現代Azaliaを再生する実験的HDドライバ、仮想環境での検証推奨"
image: "https://opengraph.githubassets.com/fbac765c15547bc238125e54a4110527507a47fa2fd389083749ac20ce60fc6b/andrew-hoffman/WDMHDA"
---

# HD Audio Driver for Windows 98SE / Me - Windows 98SE / ME 向け HD オーディオ ドライバ
Win98/MEで現代のAzalia(HD Audio)を動かす――レトロPC愛好者と現場の救世主になり得るアルファ版ドライバ

## 要約
Intel 915以降のチップセット向けに作られた、Windows 98SE / Me 用のWDMベースHD Audio（Azalia）ドライバのオープンソース実装。VMや一部の実機で再生が可能だが、現状はアルファで多くの制約・リスクあり。

## この記事を読むべき理由
古い業務アプリやレトロ環境を維持する日本の現場や趣味のコミュニティでは、サウンド互換性が途切れると大きな障害になります。本プロジェクトは「98系OSでHD Audioを動かす」数少ない実践的アプローチで、試してみる価値がある情報と手順を提供します。

## 詳細解説
- 背景と対象: WDM（Windows Driver Model）で書かれたAzalia/HD Audioドライバ。公式サポートはWindows 98SE / Me。Windows 2000/XPは別途KB888111で対応済みのため対象外。
- 対応ハード: Intel 915以降のオンボードHD Audio（主にRealtekコーデック）で動作確認。NVIDIA/AMDチップセットや一部コーデック（IDT、Analog Devices、Cirrus Logic、VIA）は未成熟。
- 技術制約:
  - 再生のみ（録音非対応）
  - サンプルレートは通常22–48 kHz、16bit（理論上96kHz/32bitは追加可能だが9xのリサンプリングが問題）
  - 単一オーディオストリーム、ハードウェアミキシングなし
  - レイテンシ約40ms（カーネル側の限界）
  - ボリュームはメインミックスだけ実装、ジャック検出／リタスキング未対応
  - BIOSのピン構成に依存しており、BIOSのバグで出力が乱れる可能性が高い
- リスク: 音が乱れる、ノイズ、フリーズ、起動失敗などの致命的不具合が発生する可能性あり。実運用は非推奨。実機デバッグ可能な人向け。
- ビルドとインストール: リリースは buildfre\i386 、デバッグは objchk\i386 にある HDA.sys。Device ManagerでHDA.infを指定し、デバイス（PCI Card class 0403）にインストール。DirectX 8.1以降を推奨。
- デバッグ手順: Sysinternals DebugView を使い、デバッグビルドの HDA.sys を C:\Windows\System32\Drivers に置いてデバイスの無効→有効でログ取得。得られたログはGitHubのIssueへ。
- ライセンスと現状: ソースはMITライセンス。開発はアルファ段階で、VMware/VirtualBoxでの動作確認が豊富。AI支援で一部コードが使われている旨の告知あり。

## 実践ポイント
- すぐ試すなら：仮想環境（VMware/VirtualBox）でまず検証。実機はBIOS依存のため事前バックアップ必須。
- インストール手順（簡易）：
  1. GitHubリポジトリから該当リリースを取得
  2. Device ManagerでHD Audioコントローラを選び、HDA.infを指定してインストール
  3. HDA.sys（buildfre/objchk）を適切なフォルダに配置
  4. 再生設定でAudio AccelerationをStandard、Sample Rate Conversion QualityをBestに
- トラブル時：DebugViewでログを取り、GitHubのIssueへ投稿。ログなしでの問合せは対応困難。
- 代替案：業務用途や安定が第一なら、Sound Blaster LiveやCMI8738、あるいは安価なUSBオーディオ（USB Audio class 1.0）を使うのが現実的。
- 追補情報：Win98系を現代ハードで動かすには JHRobotics の Patcher9x や Oerg866 の Windows 98 QuickInstall などのパッチ／プリパッチ環境が有効。

最後に：このプロジェクトは「遊び／実験」やレガシー環境の復元に強く刺さる一方、実運用には慎重さが必要です。興味があるならまず仮想環境で動作確認を。
