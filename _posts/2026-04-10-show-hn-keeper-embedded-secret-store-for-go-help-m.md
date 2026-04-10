---
layout: post
title: "Show HN: Keeper – embedded secret store for Go (help me break it) - Keeper — Go向け組み込みシークレットストア（壊してみて）"
date: 2026-04-10T10:22:23.406Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/agberohq/keeper"
source_title: "GitHub - agberohq/keeper: Simple Secure Keeper for Secrets · GitHub"
source_id: 47715339
excerpt: "Keeper：Go組込のArgon2＋XChaCha20監査付き秘密庫をすぐ試して壊してみよう"
image: "https://opengraph.githubassets.com/b9dbe0825de8eaa7b26b3bd4e2f5880d9d055be882a031759a5c7ea0d42f19ef/agberohq/keeper"
---

# Show HN: Keeper – embedded secret store for Go (help me break it) - Keeper — Go向け組み込みシークレットストア（壊してみて）

魅惑のタイトル: 「オンプレで安心を作るGoライブラリ：Argon2 + XChaCha20で守る『Keeper』入門 — 今すぐ試して“壊して”みよう」

## 要約
KeeperはGoプロセス内に組み込める軽量なシークレットストアで、Argon2id＋XChaCha20-Poly1305を用いた強力な暗号化、bboltベースの埋め込みストレージ、バケット単位の鍵分離、改ざん検知付き監査チェーンを提供します。HTTPハンドラとCLIも付属し、用途に応じて単体で利用できます。

## この記事を読むべき理由
日本の企業でもオンプレ・閉域環境や厳しいデータガバナンスが求められる場面は多く、外部KMSに頼らずにプロセス内でシークレットを安全に扱える選択肢は重要です。Keeperはシンプルに組み込み可能で、秘匿性・監査性・運用性のバランスが取れている点が特徴です。

## 詳細解説
- 基本設計  
  - 暗号化：シークレットはバケットごとのDEK（データ暗号鍵）で XChaCha20-Poly1305 により暗号化。鍵導出は Argon2id（高コストKDF）でマスターキーを生成。  
  - ストレージ：bbolt（単一ファイル）に格納。メタデータやポリシーはマスター由来の鍵でさらに暗号化・HMACで整合性保護。  
  - 監査チェーン：イベントに対してHMAC署名＋暗号化を行い、履歴を追えるが改ざんは検知可能（履歴は上書きされず追記）。  

- バケットのセキュリティレベル（4種）  
  1. LevelPasswordOnly：DEKをマスターキーからHKDFで導出。起動時にマスターパスフレーズで自動アンロック。  
  2. LevelAdminWrapped：ランダムDEKを生成し、管理者毎にKEKをHKDF(masterKey‖adminCred)で導出してラップ。管理者単位でアンロックが必要。  
  3. LevelHSM：DEKはHSMプロバイダでラップ。Keeperは生DEKを保持しない（SoftHSMはテスト用、実運用不可）。  
  4. LevelRemote：HSMと同様だがネットワーク越しのKMS（Vault/AWS/GCP等）に委任。相互TLSなどで強固に接続する想定。  

- 鍵管理の工夫  
  - マスターのsaltは平文で保存（KDFのユニーク性のため）。マスター自身は決してディスクに残らない。  
  - KEK導出はHKDF（高速）で行い、二重Argon2は回避して性能と実用性を確保。  
  - メタデータ（アクセス時間等）もバケット鍵で暗号化するため、DBの読み取りだけではアクセスパターンが分からない。  

- 付属ツール  
  - ライブラリ：アプリに直接組み込む。  
  - x/keephandler：net/httpにワンコールでマウント可能なHTTPハンドラ（フックやガード追加可）。  
  - cmd/keeper：REPL風CLIで、入力のエコー無効や履歴流出防止など運用便利機能あり。

## 実践ポイント
- 選定基準：スタート時は LevelPasswordOnly を使い、運用で管理者分離が必要なら LevelAdminWrapped、HSM環境があれば LevelHSM/Remote を検討する。  
- 本番注意点：SoftHSMはテスト限定。Remoteを使う場合は相互TLS（クライアント証明書）を必ず設定する。  
- 運用ルール：マスターパスフレーズの保護と定期的なキー回転、監査ログの定期検査を実施する。  
- テスト・導入：まずローカルでCLI/HTTPハンドラを試し、監査チェーンやアンロックフローを壊して（検証して）挙動を把握すること。  
- 日本市場への応用：オンプレや閉域K8s、レガシーシステムのミニマムなシークレット管理レイヤーとして有効。既存のVault/KMSと併用する設計も現実的。

Keeperは「組み込みで使える安全な土台」を目指したツールです。まずはローカルで動かしてアンロック・ラップ・監査の流れを確認し、運用要件に合わせてセキュリティレベルを選んでください。
