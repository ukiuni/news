---
layout: post
title: "Sleeper Shells: Attackers Are Planting Dormant Backdoors in Ivanti EPMM - Ivanti EPMMに眠るバックドア「スリーパーシェル」"
date: 2026-02-09T15:43:07.906Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://defusedcyber.com/ivanti-epmm-sleeper-shells-403jsp"
source_title: "Sleeper Shells: How Attackers Are Planting Dormant Backdoors in Ivanti EPMM"
source_id: 46946062
excerpt: "Ivanti EPMMにメモリ待機型バックドア多数、即パッチ必須"
image: "https://defusedcyber.com/images/posts/ivantishells.jpg"
---

# Sleeper Shells: Attackers Are Planting Dormant Backdoors in Ivanti EPMM - Ivanti EPMMに眠るバックドア「スリーパーシェル」
Ivanti EPMMに「置いて確認して去る」巧妙なバックドアが広範に展開されている—今すぐ検査と対策を。

## 要約
攻撃者はIvanti Endpoint Manager Mobile（EPMM）の脆弱性を突き、/mifs/403.jsp に「メモリ内で待機する」Javaクラスローダーを置いて確認だけして去る手口を多数観測。即時の悪用は見られないが、初期アクセスの売買（IAB）を想定した危険な準備活動です。

## この記事を読むべき理由
日本の企業・官公庁でもEPMMや類似モバイル管理基盤を使う現場があり、被害が出る可能性が高い点。被害が「静か」で検知しにくいため、早めの対策とログ確認で未然防止できるからです。

## 詳細解説
- 脆弱性：IvantiはCVE-2026-1281／CVE-2026-1340（認証バイパス／RCE）を公表。未適用環境は誰でもアプリケーションレベルのエンドポイントにアクセス可能に。
- 攻撃の特徴：
  - 侵入者は従来の対話型webshellではなく、Base64化したJavaバイトコード（CAFEBABEヘッダ）をパラメータ経由で送り、/mifs/403.jsp に配置。
  - 配置されたのは base.Info というコンパイル済みJavaクラス（Info.java）で、単体ではコマンド実行しない「ステージローダー」。後段のクラスを受け取るまで何もしない。
- 動作の要点：
  - エントリは equals(Object) を悪用し、doGet/doPostより検知を避ける設計。
  - リクエスト引数から HttpServletRequest/Response を取り出し、特定パラメータ k0f53cf964d387 があれば先頭2文字を除いた残りをBase64デコードして ClassLoader#defineClass でメモリ上に読み込む（ファイルは一切書き込まれない）。
  - Java 8以降のBase64や古い JVM の sun.misc.BASE64Decoder へ対応、コンテナやJVM差分に強い作り。
  - 調査用に user.dir、ファイルシステムルート、OS名、実行ユーザ名などホスト情報を二段目クラスへ渡す。
- 戦術的意義：
  - ローダー設置後に追跡可能な追加リクエストは観測されず、アクセスを確保して「販売」や別勢力への引き渡しを想定する典型的IABトレードクラフト。

## 実践ポイント
- まずやること：
  - Ivantiの公式パッチを直ちに適用。
  - 該当アプリケーションサーバを再起動してメモリ上のインプラントを除去（ペイロードはディスクに残らないため再起動が重要）。
- ログ/検出で見るべき痕跡：
  - リクエストパス： /mifs/403.jsp
  - パラメータ名： k0f53cf964d387
  - Base64の先頭シグネチャ： yv66vg （CAFEBABEのBase64）
  - レスポンス内マーカー： 3cd3d または e60537
  - エラーフォーマット： ERROR:// を含むレスポンス
  - 既知のファイルハッシュ（監査用）： SHA-256 097b051c9c9138ada0d2a9fb4dfe463d358299d4bd0e81a1db2f69f32578747a
- ハンティングのヒント：
  - WebサーバアクセスログとWAFログで該当パス＋大きめのBase64パラメータを抽出。
  - 監視ツールがメモリのみのローダーを検出しにくいので、サーバ再起動と設定差分（最近のデプロイ／ファイル変更）もチェック。
- 組織向け対策：
  - EPMMなど管理基盤は外部公開を最小化、アクセス制限（IP制限・VPN）を強化。
  - インシデントレスポンスで「静かな」初期アクセスを想定したトレーニングとプロセス整備を。

この手口は「何もしないこと」が狙いであり、沈黙している間に次の悪用者へ渡る可能性があります。パッチと再起動、ログの重点チェックを今すぐ実行してください。
