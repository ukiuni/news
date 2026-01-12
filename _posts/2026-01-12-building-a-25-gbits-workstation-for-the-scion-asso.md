---
layout: post
title: "Building a 25 Gbit/s workstation for the SCION Association - SCION協会のための25 Gbit/sワークステーション構築"
date: 2026-01-12T18:34:44.834Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/scionassociation/blog-25gbit-workstation"
source_title: "GitHub - scionassociation/blog-25gbit-workstation: Blogpost about building the SCION 25 Gbit/s Workstation"
source_id: 46590541
excerpt: "静音25GワークステーションをAF_XDPで単一スレッド達成へ導く実践ガイド"
image: "https://opengraph.githubassets.com/f5dabcbac5fc1a1918f05ffc14d6ef189982dc3d42a357677161da052c73f1f9/scionassociation/blog-25gbit-workstation"
---

# Building a 25 Gbit/s workstation for the SCION Association - SCION協会のための25 Gbit/sワークステーション構築
驚くほど静かに25 Gbit/sを叩き出す――SCION向け“ゼロコピー”ワークステーションの舞台裏

## 要約
SCIONのオープンソースルータのデータプレーン性能を劇的に向上させるため、AF_XDP（XDP/eBPFベース）のゼロコピー環境を実現する25 Gbit/s対応ワークステーションを自作した記録。必要なハード選定から設定、トレードオフまで詳述する。

## この記事を読むべき理由
- 日本でも25G/100Gの家庭・事業者回線や金融インフラの重要性が高まる中、ソフトウェアルータ性能向上の実践例はすぐに役立つ知見です。  
- AF_XDPを使ったカーネルバイパスの現実的なハード要件と、開発／テスト環境の作り方が分かります。

## 詳細解説
- 背景  
  - SCIONはBGPに代わる次世代のインターASアーキテクチャで、パス認証や明示的経路制御を提供。重要インフラへの適用が進む一方で、オープン実装のデータプレーン性能は改善が必要です。  
- 目標と制約  
  - 目的は「単一スレッドで25 Gbit/sを達成すること」。オフィス設置なので低騒音、かつ予算を抑える必要がありました。  
- カーネル経由の限界とバイパス手法  
  - 標準のLinuxネットワーキング経路ではパケットごとにバッファ割当・コピー・フィルタ・ルーティング等が発生し、ソフトウェアでのスループットに限界あり（例：従来実装で約5–6 Gbit/s相当が上限）。  
  - カーネルをバイパスする選択肢としてはDPDK、AF_XDP、VPP等。今回はGoで保守性と運用性を重視し、LinuxネイティブのAF_XDPを採用。  
- AF_XDPの要点（初心者向け）  
  - AF_XDPはXDP/eBPFを利用し、NICドライバとユーザ空間で共有するUMEM（巨大ページ推奨）へゼロコピーでパケットを渡す仕組み。  
  - 実装手順の概略：UMEM確保 → fill/comp/tx/rxリング初期化 → AF_XDPソケットをNICキューにバインド（XDP_ZEROCOPYが理想） → カーネルに小さなeBPF/XDPプログラムをロードしてパケットをUMEMへリダイレクト。  
  - 注意点：ゼロコピーの多くはベアメタル環境（仮想マシンでは不可または制限あり）。対応NIC/ドライバやカーネルバージョンの影響も大きい。  
- ハードウェア選定と実際の構成  
  - NIC：NVIDIA/Mellanox BlueField-2（Dual-25G）を3枚導入（合計6ポート）。BF-2はDPU/スマートNICでAF_XDPの検証に好適。  
  - マザーボード：PCIe Gen5で多数スロットを持つワークステーション向け（候補としてGigabyte MS03-CE0、ASUS Pro WS W790E-SAGE SE）。最終的にSAGE SEを選択し、64レーン以上を確保。  
  - CPU/プラットフォーム：LGA4677ソケットのSapphire Rapids系などを選び、PCIeレーンとDDIOなどネットワーク性能に寄与する機能を重視。  
  - コスト感：パーツ合計でCHF約3,741（約USD 4,700）程度。  
- ベンチマーク上の課題  
  - ソフトウェアルータの並列化はパケット順序の乱れ（reordering）を招きやすく、単一スレッドで高帯域を達成することが重要。AF_XDPはそのための現実的な方法。

## 実践ポイント
- AF_XDPを学ぶ順序（初級者向け）  
  1. 最新のLinuxカーネル（またはAF_XDPパッチ）とeBPFの基礎を学ぶ。  
  2. UMEM/リング、XDPプログラムの最小例を動かしてパケットの流れを把握する。  
  3. 対応NIC（Mellanox/IntelのAF_XDPサポート）でゼロコピーモードを確認する。  
- ハード選定のチェックリスト  
  - 必要PCIeレーン数と世代（Gen4/Gen5）を確認。複数25G/100G NIC運用ならワークステーション向けマザーボードが現実的。  
  - 静音性が必要ならタワー系か静音ラックを検討。ファン制御やケース選定は意外と重要。  
- テスト環境の現実的制約  
  - クラウドVMではAF_XDPのゼロコピーは使えないことが多い。ベアメタルや物理NICが必須。  
- 日本市場への示唆  
  - 日本でも25G/100G帯サービスが広がりつつあり、ローカルIXや事業者向けルータ/テストベッドのニーズが増加。研究・開発用の安価なワークステーション自作は現実的な選択肢。  
- 参考リンク（原典）  
  - SCION公式や元記事の詳細を参照して、実際の部品リストや設定手順を確認してください（元記事のリポジトリに詳細あり）。

短く言えば、「ソフトウェアルータのボトルネックはカーネル経由のオーバーヘッド。AF_XDP＋対応ハードでゼロコピー環境を構築すれば、単一スレッドで25 Gbit/sを目指せる」。実際の導入はNIC/マザーボード/カーネル互換性の確認が肝です。
