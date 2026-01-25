---
layout: post
title: "A macOS app that blurs your screen when you slouch - 猫背すると画面をぼかす macOS アプリ"
date: 2026-01-25T16:44:05.793Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/tldev/posturr"
source_title: "GitHub - tldev/posturr: A macOS app that blurs your screen when you slouch. Uses Vision framework for real-time posture detection."
source_id: 46754944
excerpt: "カメラで姿勢を検出し猫背で画面を段階的にぼかすMacアプリ、今すぐ姿勢改善"
image: "https://opengraph.githubassets.com/34656cee579870c3020136bcbda4a829149957341bad2cf874e809328c399036/tldev/posturr"
---

# A macOS app that blurs your screen when you slouch - 猫背すると画面をぼかす macOS アプリ
猫背になると画面が徐々にぼやけて「姿勢を直す」ことを促す、シンプルかつプライバシー配慮のMacアプリ

## 要約
PosturrはMacのカメラとAppleのVisionフレームワークで姿勢をリアルタイム検出し、猫背になると画面を段階的にぼかして注意喚起するローカル実行アプリです。

## この記事を読むべき理由
リモートワークや長時間コーディングが当たり前になった日本で、無理なく姿勢改善を促すツールは健康生産性に直結します。個人情報を外部に送らない点は企業利用でも安心です。

## 詳細解説
- 姿勢検出: AppleのVisionフレームワークで体のランドマーク（鼻、肩など）をトラッキング。上半身が見えない場合は顔の位置をフォールバックして検出します。  
- ぼかしの仕組み: 姿勢のズレ量に応じて段階的にぼかしを強める。全ウィンドウ・複数ディスプレイに対応するため、macOSの低レイヤー（private）なCoreGraphics APIを利用してシステムレベルで効率的にぼかします。  
- 操作性: メニューバーから有効/無効、再キャリブレーション、感度（Low〜Very High）、デッドゾーン（None〜Large）を調整可能。メニューで現在の状態（Monitoring / Slouching / Good Posture）を確認できます。  
- プライバシーと軽さ: すべてローカルで処理し画像は保存・送信しない。常駐しても軽量に動作します。  
- 開発・配布上の注意: リポジトリはMITライセンス。署名されていないため初回はGatekeeperで「右クリック→開く」して許可する必要があります。カメラ許可も必須。  
- コマンド操作: /tmp/posturr-command にコマンドを書き込むことで外部制御（capture, blur <0-64>, quit）が可能。  
- 制限: サインなし（初回手動許可が必要）、カメラ・照明条件に依存、完全な精度保証なし。private API利用は将来の互換性リスクがあります。

## 実践ポイント
- インストール手順（簡易）
  1. Releasesから最新のPosturr-vX.X.X.zipをダウンロードしてApplicationsへコピー  
  2. 初回はアプリを右クリック→「開く」でGatekeeperを回避、カメラ許可を与える  
- 使い方のコツ
  - カメラを目の高さに設置し、肩まで映る距離を確保する  
  - 部屋は顔がはっきり見える照明を確保する（暗すぎると検出精度低下）  
  - 初回に「Recalibrate」で正しい基準姿勢を登録、感度とデッドゾーンを調整して誤検知を減らす  
- ソースからビルド（macOS 13+ が必要）
```bash
# bash
git clone https://github.com/tldev/posturr.git
cd posturr
./build.sh
```
- 企業での検討ポイント: 画像を外部に送らないため社内利用のハードルは低いが、署名・配布ポリシーや将来の互換性（private API使用）を事前確認すること。

興味があれば、実機で試してみる価値あり。長時間作業するエンジニアほど恩恵が大きいツールです。
