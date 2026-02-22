---
layout: post
title: "Show HN: Local-First Linux MicroVMs for macOS - macOS向けローカル優先MicroVM「shuru」"
date: 2026-02-22T20:42:49.365Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://shuru.run"
source_title: "shuru - Local-first microVM sandbox for AI agents"
source_id: 47113567
excerpt: "Apple Siliconで瞬時起動、使い捨てLinux MicroVMで安全にAI実行"
image: "https://shuru.run/og.png"
---

# Show HN: Local-First Linux MicroVMs for macOS - macOS向けローカル優先MicroVM「shuru」
Apple Siliconで軽量・使い捨てのLinuxサンドボックスを即起動──AIエージェントや安全なコード実行に最適なツール

## 要約
shuruはmacOS上で動くローカル優先（local-first）なMicroVMランタイム。AppleのVirtualization.frameworkを使い、Docker不要でほぼネイティブ速度の一時的なLinux環境を素早く作れるのが特徴です。

## この記事を読むべき理由
日本でもMac（特にApple Silicon）を使う開発者が増加中。AIエージェントの実行や安全なコード実験、検証環境の使い捨て化はすぐに役立つため、手軽に試せる選択肢として注目に値します。

## 詳細解説
- アーキテクチャ：Apple Virtualization.framework上にRustで実装。エミュレーション不要でARM64ネイティブ動作、Docker依存なし。  
- エフェメラル（デフォルト）：各実行はクリーンなrootfsから起動。終了時に変更は破棄されるため「壊しても問題ない」実験が可能。  
- チェックポイント：ディスク状態を名前付きスナップショットとして保存・復元。環境の「コミット／ブランチ」を実現し、再現性の高いワークフローに使える。  
- ネットワーク：デフォルトはオフライン。必要時に --allow-net でNAT有効。ポートフォワーディングはvsock経由でホストと接続でき、ネットワーク不要でもサービス公開可能。  
- リソース設定：起動毎にCPU数、メモリ、ディスクサイズを指定可能（--cpus, --memory, --disk-size）。  
- CLI操作感：run / checkpoint create / run --from といったシンプルなコマンドで使える。AIエージェントがライブラリやツールをインストールしてもサンドボックス内に限定できる。  
- ユースケース：AI生成コードの安全実行、エージェントのツール使用、並列評価（reproducible evals）、開発用の使い捨て環境。

簡単な例：
```bash
# インストール
curl -fsSL https://shuru.run/install.sh | sh

# 一回限りの実行（終了で破棄）
shuru run -- echo "hello from the sandbox"

# ネット有効でパッケージを入れる
shuru run --allow-net -- apk add python3

# チェックポイント作成
shuru checkpoint create myenv --allow-net -- sh -c 'apk add nodejs npm'

# チェックポイントから起動してポートフォワード
shuru run --from myenv -p 8080:8000 -- python3 -m http.server 8000
```

## 実践ポイント
- まずはローカルでインストールして1回実行（shuru run）で挙動確認。  
- 重要な実験はチェックポイントを作っておく（復元・分岐が楽）。  
- デフォルトでネットワーク遮断になる点を利用して、エージェントに外部アクセスを許可するか明示的に制御する。  
- CIや評価環境では「同じチェックポイント」を使えば再現性が高くなる。  
- 日本の企業環境では、Mac＋Apple Siliconでの検証や社内AI実験の安全対策として導入検討しやすい。

興味があるならまず一度インストールして、短時間のサンドボックス起動→チェックポイント保存→復元を試してみてください。
