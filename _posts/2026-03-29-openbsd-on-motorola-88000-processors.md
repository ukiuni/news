---
layout: post
title: "OpenBSD on Motorola 88000 Processors - Motorola 88000プロセッサ上のOpenBSD"
date: 2026-03-29T00:26:31.624Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://miod.online.fr/software/openbsd/stories/m88k1.html"
source_title: "OpenBSD on Motorola 88000 processors"
source_id: 47543186
excerpt: "忘れられたRISC「m88k」でのOpenBSD移植史と産業用途の実機事情"
---

# OpenBSD on Motorola 88000 Processors - Motorola 88000プロセッサ上のOpenBSD
忘れ去られたRISC「m88k」とOpenBSDのドラマティックな出会い — レトロ／組込みファン必見の歴史と技術

## 要約
Motorolaの短命なRISCアーキテクチャ m88k（88100/88110）は、独特なCMMU構成やVMEプラットフォーム上で使われ、CMU Mach経由でOpenBSDが移植されたことで歴史に名を残した。ハードの珍しさとソフトの移植史が交差する興味深い物語。

## この記事を読むべき理由
日本企業（例：Omron）が実機を出しており、産業用途のレガシー保守やレトロコンピューティング、組込みOSの学びとして価値が高い。OpenBSD移植の経緯はOSS文化や実装ノウハウの好教材になる。

## 詳細解説
- m88kの成り立ち：Motorolaの68000系の後継を目指したRISC。初代88100は演算コアと外付けCMMU（88200）を分ける設計で、CMMUがキャッシュ＋MMU機能を提供。P-Bus上で複数CMMUが結合され、プロセッサ間のキャッシュ整合や他プロセッサのMMU操作を可能にしていた（これがマルチプロセッサ実装を容易にした）。
- 世代差：88100世代はクロック16–33MHz（多くは25MHz）。次世代88110はキャッシュ/ MMU統合、簡単な例外モデルを導入し50MHzを目標にしたが初期は不具合で40MHz扱いに。設計の一部は初期PowerPCに流用された。
- ハードウェアとVME：利用は主に産業/ワークステーション向けで、MVMEシリーズ（MVME180/181/187/188/197など）が代表。VMEバスは複数ボードで32ビットアドレス空間を共有する標準で、日本の産業機器や研究用途でも使われた。
- 採用例：MotorolaのMVME、OmronのLuna-88K（日本製デスクトップ/ワークステーション）、Data GeneralのAViiONなど。Omron機は日本で実機が存在した点で特に興味深い。
- OSとOpenBSD移植：Motorola系はSystem III/V派生、Data GeneralはDG/UX、OmronはBSD派のUniOSがあった。CMU Machのソースが入手できたことが契機となり、Nivas Madhurが1995年にMVME187向けにOpenBSDを移植。その後1996年にカーネルとユーランドがリポジトリに入れられ、保守者の交代や1998年の改善を経てプロジェクトが継続した。

## 実践ポイント
- 情報収集：m88k資料は散逸しているため m88k.com や Internet Archive のミラーを探すと良い（レガシー資料の掘り起こしに有効）。
- ハード保存：MVMEボードやLuna-88K等を見つけたら電源/電解コンデンサの点検・保護を優先する。VMEは物理スペースと電源要件が大きい点に注意。
- ソフトで遊ぶ：OpenBSDのm88k移植史を学び、可能ならリポジトリや当時のコミットログを読んで移植作業の流れを学ぶ（OSS移植の教材になる）。
- コミュニティ参加：レトロコンピューティング／組込みのフォーラムに参加して、ドキュメントやROMイメージ、回路図の共有を促す。

元記事の詳細は元URL（参考）で。保存と共有が未来の研究資源を作る。
