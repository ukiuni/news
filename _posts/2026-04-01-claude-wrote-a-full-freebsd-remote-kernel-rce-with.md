---
layout: post
title: "Claude Wrote a Full FreeBSD Remote Kernel RCE with Root Shell (CVE-2026-4747) - Claudeが書いたFreeBSDリモートカーネルRCE（CVE-2026-4747）"
date: 2026-04-01T11:02:31.326Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/califio/publications/blob/main/MADBugs/CVE-2026-4747/write-up.md"
source_title: "publications/MADBugs/CVE-2026-4747/write-up.md at main · califio/publications · GitHub"
source_id: 47597119
excerpt: "FreeBSDのNFSで遠隔カーネルRCE（root取得）発見、緊急対策を"
image: "https://opengraph.githubassets.com/2c80e0186d687165950b98c707069460ecb741b4873a2d8ce30ccd51afff07fd/califio/publications"
---

# Claude Wrote a Full FreeBSD Remote Kernel RCE with Root Shell (CVE-2026-4747) - Claudeが書いたFreeBSDリモートカーネルRCE（CVE-2026-4747）
FreeBSDのNFS（RPCSEC_GSS）で発見された「リモートでカーネルを乗っ取る可能性のある」脆弱性を、初心者にも分かりやすく解説します。

## 要約
FreeBSDのkgssapi（RPCSEC_GSS）実装にスタック境界チェック漏れがあり、NFSを介してリモートでカーネル実行（root権限取得）される可能性がある（CVE-2026-4747）。パッチが公開済みです。

## この記事を読むべき理由
- FreeBSDはNAS、ネットワーク機器、インフラで使われるため、日本の企業や公共機関のシステムにも影響し得ます。
- カーネルレベルのRCEは最悪の場合全システム乗っ取りにつながるため、迅速な対応が必要です。

## 詳細解説
- 問題箇所はカーネル側のRPCSEC_GSS検証処理（svc_rpc_gss_validate）。RPCヘッダを作るスタック上の固定長バッファに、認証情報（credential body）を長さチェックなしでコピーする実装になっており、これがオーバーフローを引き起こします。  
- オーバーフローが発生すると、スタック上の保存レジスタやリターンアドレスを書き換えられ、カーネルコンテキストで任意コード実行が可能になります。つまりroot権限での実行に直結します。  
- このコードパスはNFS（ポート2049）で使われるRPCSEC_GSS認証に関連しており、攻撃はネットワーク越しに到達可能。ただし、脆弱箇所に到達するには有効なGSS/Kerberosコンテキスト（正当なチケット）が必要になるため、通常はKerberosを使う環境（ADやFreeIPAなど）でリスクが高まります。  
- 影響バージョンと公開情報はFreeBSDのアドバイザリ（FreeBSD-SA-26:08.rpcsec_gss）およびCVE-2026-4747で確認できます。ベンダーは境界チェックを追加するパッチを提供済みです。

## 実践ポイント
- まずは公式パッチを適用する（OSアップデート／パッチ適用が最優先）。  
- すぐにアップデートできない場合は、影響モジュール（kgssapi）をロードしない、あるいはNFSのRPCSEC_GSS認証を無効化／NFSサービスを停止してネットワークから隔離する。  
- NFS/Kerberosサービスへのアクセスをファイアウォールで制限し、KDC（ポート88）やNFS（ポート2049）を公開ネットワークに直接置かない。  
- ログ監視とインシデント対応準備：不審なKerberosチケット使用やNFSエラー、クラッシュを監視し、疑わしければ速やかに接続元の遮断とフォレンジックを実施。  
- 組織でFreeBSDを使っている場合は、該当バージョンのリストアップとパッチ計画を速やかに策定すること。

参考：FreeBSDのセキュリティアドバイザリ（FreeBSD-SA-26:08.rpcsec_gss）およびCVE-2026-4747の公式情報を確認してください。
