---
layout: post
title: "axios 1.14.1 and 0.30.4 on npm are compromised - axios 1.14.1 と 0.30.4 が npm で侵害されました"
date: 2026-04-01T00:52:58.191Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://safedep.io/axios-npm-supply-chain-compromise/"
source_title: "axios Compromised: npm Supply Chain Attack via Dependency Injection - Real-time Open Source Software Supply Chain Security"
source_id: 409827689
excerpt: "axiosがnpmで改竄、乗っ取られた維持者からpostinstallで自動マルウェア注入される危険"
---

# axios 1.14.1 and 0.30.4 on npm are compromised - axios 1.14.1 と 0.30.4 が npm で侵害されました
あなたのプロジェクトに潜む「自動で動く」マルウェア — axios npm パッケージ供給網攻撃の全貌

## 要約
npm に公開された axios の 1.14.1 と 0.30.4 がメンテナアカウントの乗っ取りにより改竄され、package.json に悪意ある依存（plain-crypto-js）が注入され、postinstall でプラットフォーム別の二次ペイロードを自動取得・実行します。

## この記事を読むべき理由
axios は多くの日本のウェブ・Node.js プロジェクトで使われており、バージョン範囲指定（^1.14.0 など）で自動的に脆弱版へ上がる可能性があります。サプライチェーン攻撃は気づかずに内部ネットワークや開発環境を汚染するため、即座の確認と対策が必要です。

## 詳細解説
- 被害概要  
  - 影響バージョン: axios@1.14.1 と axios@0.30.4（それぞれ 1.x / 0.x 系）  
  - 公開方法: 正規の CI/SLSA を経ない「手動公開」で、メンテナの Proton Mail アドレスを使うなど通常と異なるメタ情報を持つ公開が行われた（アカウント乗っ取りの疑い）。  
  - 差分: JavaScript ソースは変更されず、package.json に plain-crypto-js という依存が追加され、prepare スクリプトが削除されたのみ。つまりインストール時の仕込み（postinstall）が狙われた。  

- Trojan パッケージ（plain-crypto-js）  
  - 初出: 2026-03-30 公開。正規ライブラリ crypto-js を装ったほぼ同一パッケージに setup.js（1行の難読化済みペイロード）を追加。postinstall で node setup.js を実行。実行後は痕跡（setup.js や悪い package.json）を消してカモフラージュする仕様。  

- 第一段階の挙動（setup.js）  
  - カスタム復号 → C2 へ POST（例: hxxp://sfrclak[.]com:8000/6202033）し、OS ごとに別の二次ペイロードを取得。  
  - macOS: /Library/Caches/com.apple.act.mond にネイティブバイナリを保存して実行（osascript 経由）。  
  - Windows: PowerShell を %PROGRAMDATA%\wt.exe としてコピーし、一時 .ps1 を取得して隠れて実行（VBScript + cscript）。  
  - Linux: /tmp/ld.py（Python RAT）を落として nohup python3 で実行。  
  - ペイロードはユーザー操作不要で postinstall 時に自動実行される。  

- 第二段階（Linux で取得された例）  
  - 取得された ld.py は Python の RAT（リモート操作型マルウェア）で、ビーコン（60秒毎の POST）やバイナリ展開コマンドなどをサポート。永続化は確認されないが、実行中は侵害したマシンを遠隔操作できる。  

- 証拠と検出可能な指標（抜粋）  
  - 悪意ある publisher メール: ifstap@proton.me（乗っ取り疑い）、nrwise@proton.me（trojan）  
  - C2: hxxp://sfrclak[.]com:8000/ → IP 142.11.206.73（Express.js）  
  - 重要ハッシュ: setup.js SHA256 e10b1fa84f1d6481625f741b69892780140d4e0e7769e7491e5f4d894c2e0e09  
    Linux second-stage SHA256: fcb81618bb15edfdedfb638b4c08a2af9cac9ecfa551af135a8402bf980375cf  
  - 特徴的なファイルパス: /Library/Caches/com.apple.act.mond, %PROGRAMDATA%\wt.exe, /tmp/ld.py, /tmp/.<ランダム> など

## 実践ポイント
- まず影響範囲を確認（ワークスペース／CI／ビルド環境すべて）:
  - 依存として axios を使っている場所を列挙: package.json / package-lock.json / yarn.lock / pnpm-lock.yaml を確認。  
  - ローカル・CI 上でインストール済みか確認:
```bash
# プロジェクト内での確認例
bash
npm ls axios
# npm レジストリ上の publisher/attestations を見る
bash
curl -s https://registry.npmjs.org/axios/1.14.1 | jq '._npmUser, .dist.attestations'
```
- マシン上の痕跡探索と除去（管理者権限で実行）:
```bash
bash
# setup.js を検索してハッシュ確認
find / -type f -name "setup.js" -exec shasum -a 256 {} \; 2>/dev/null | grep e10b1fa84f1d6481625f741b69892780140d4e0e7769e7491e5f4d894c2e0e09

# 目立つ悪性ファイルの候補
# macOS: /Library/Caches/com.apple.act.mond
# Windows: %PROGRAMDATA%\wt.exe
# Linux: /tmp/ld.py, /tmp/.*
```
- 即時対応（優先度高）:
  - axios を 1.14.0（或いは自チームで検証済みの既知安全版）へ固定してロックファイルを再生成（npm ci / yarn install --frozen-lockfile）。  
  - 既にインストール済みのビルド環境や CI ワーカーはクリーン再構築（イメージ再作成）、秘密鍵/トークンのローテーション。  
  - 被害調査: ビルドログ、ネットワーク接続ログに該当 C2 宛の通信（142.11.206.73:8000）や 60 秒毎の POST を調査。  
  - npm パッケージ発行に使うアカウント・キーの保護と、組織側での publish ポリシー（OIDC/CICD のみ許可）を徹底。  
- 長期対策:
  - 依存性の自動更新をそのまま信用せず、SBOM/ソース由来のプロビナンス（SLSA）や署名を検証。  
  - install-time の postinstall 実行をログ化／ブロックするポリシー導入（CI/ビルド専用のサンドボックスで実行）。  
  - 依存のスキャン（署名・ハッシュ・作者）と PR ベースの vetting を組織的に導入。

短時間でできる一歩は「lockfile を復元して再インストール」「CI ワーカーを再構築」「該当ファイルの検索と削除」「トークンのローテーション」です。まずは影響範囲把握と被害拡大防止を優先してください。
