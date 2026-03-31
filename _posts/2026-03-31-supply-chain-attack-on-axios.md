---
layout: post
title: "Supply Chain Attack on Axios - Axiosのサプライチェーン攻撃"
date: 2026-03-31T09:19:04.929Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://socket.dev/blog/axios-npm-package-compromised"
source_title: "Supply Chain Attack on Axios Pulls Malicious Dependency from..."
source_id: 1152315785
excerpt: "Axiosの特定npmにRAT仕掛け、広範囲感染と難読化で痕跡を隠す攻撃"
image: "https://cdn.sanity.io/images/cgdhsj6q/production/2efbe38b13a32e7aa357175bca47b51465cf6b3e-1035x708.png?w=1000&amp;q=95&amp;fit=max&amp;auto=format"
---

# Supply Chain Attack on Axios - Axiosのサプライチェーン攻撃
人気ライブラリAxiosに潜む仕掛け──npm経由でRATを落とすマルウェアが混入、あなたのプロジェクトは無傷か？

## 要約
Axiosの特定npmリリース（axios@1.14.1 / axios@0.30.4）に悪意ある依存 plain-crypto-js@4.2.1 が混入。postinstallで多段のペイロードを展開し、プラットフォーム別にRATやスクリプトを取得・実行、自己改竄と痕跡消去を行います。

## この記事を読むべき理由
Axiosは日本のフロント/バックエンドプロジェクトでも広く使われており、caret指定（^）で自動的に脆弱版が入ると瞬時に大量のプロジェクトが巻き込まれます。サプライチェーン侵害は検出が遅れやすく影響が広範です。

## 詳細解説
- 発行経路の異常：影響版はGitHubの通常タグに存在せず、公開ワークフロー外でnpmに直接公開された可能性が高い。  
- 悪性パッケージの振る舞い：plain-crypto-jsのpostinstallで setup.js が実行され、OS判定→プラットフォーム別ドロッパーを取得・実行。実行後に setup.js を削除し package.json を差し替えるなど痕跡を隠蔽。  
- 難読化：逆順Base64＋XOR鍵（"OrDeR_7077" と定数333）という二層のカスタム難読化で文字列（C2、コマンド、モジュール名等）を隠蔽し、静的検出を回避。  
- プラットフォーム別ペイロード（要点）：
  - macOS：AppleScript→curlでMach-Oバイナリを/Library/Caches配下に配置、Mach-OはRAT（システムフィンガープリント、コマンド実行、追加バイナリ注入等）を備える。  
  - Windows：powershell.exeを%PROGRAMDATA%\wt.exeとして偽装し、VBScript→PowerShellで.ps1を実行。  
  - Linux：/tmp/ld.py をcurlで取得して nohup python3 で実行。  
- トランジティブ感染：他パッケージのvendored依存や改竄済みaxiosを通じても拡散。  
- 主なIOC（簡潔）：
  - 悪性パッケージ：axios@1.14.1, axios@0.30.4, plain-crypto-js@4.2.1  
  - C2ドメイン：sfrclak[.]com（142.11.206.73）  
  - ファイル：/tmp/ld.py, /Library/Caches/com.apple.act.mond, %PROGRAMDATA%\wt.exe など

## 実践ポイント
- まず確認（リポジトリ／CI／ローカル）:
  ```bash
  # 該当依存を検索
  npm ls plain-crypto-js
  grep -R "plain-crypto-js" package-lock.json yarn.lock || true
  grep -R "axios@1.14.1\|axios@0.30.4" package-lock.json yarn.lock || true
  ```
- 検出時の対処:
  - 直ちに該当バージョンを除去または既知安全なバージョンにピン（例：v1.14.0など）し、lockfileを再生成して再インストール。  
  - node_modules を削除し、lockfile固定後にクリーンインストール（npm ci / yarn install --frozen-lockfile）。  
- パイプラインと公開権限の見直し:
  - 長期有効なnpmトークンを廃止し、最小権限・短命トークン／署名付きリリースを導入。CIのpublish権限を限定。  
- 検知・防御の強化:
  - ネットワークで C2 ドメイン/IP の通信をブロックまたは検出ルール追加。  
  - インストール時のpostinstall等ライフサイクルフックの監査、npmパッケージのサンドボックス検査導入。  
- 監査とログ確認:
  - ビルドログ、CIジョブ、開発環境の端末で suspicious ファイル（例：/tmp/ld.py、%TEMP%\6202033.ps1、/Library/Caches/...）や不審なUser-Agent/接続を確認。  

短期的には依存のバージョン固定とトークン権限の即時見直し、中長期的には供給側のサプライチェーン防御（署名、公開プロセス監査、自動スキャン）を推進してください。
