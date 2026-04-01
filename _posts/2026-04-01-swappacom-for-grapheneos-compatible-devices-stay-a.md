---
layout: post
title: "Swappa.com for GrapheneOS compatible devices – Stay Away - Swappa.com（GrapheneOS対応端末）— 近寄るな"
date: 2026-04-01T22:36:59.660Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discuss.grapheneos.org/d/33727-swappacom-for-grapheneos-compatible-devices-stay-away"
source_title: "Swappa.com for GrapheneOS compatible devices - STAY AWAY - GrapheneOS Discussion Forum"
source_id: 47607067
excerpt: "SwappaのUnlocked表記Pixelが解除不可で返金損、購入前確認と回避策を紹介"
image: "https://discuss.grapheneos.org/opengraph.png"
---

# Swappa.com for GrapheneOS compatible devices – Stay Away - Swappa.com（GrapheneOS対応端末）— 近寄るな
Swappaで掘り出し物のPixelを買う前に読むべき「待った！」記事

## 要約
海外フォーラム投稿者がSwappaで「Unlocked」と表記されたPixelを複数回購入したが、いずれもブートローダーが解除できずGrapheneOS導入に失敗、返金手続きや手数料で損失が出たという警告。

## この記事を読むべき理由
GrapheneOSのようにブートローダー解除が必須なOSを導入したい人にとって、販売サイトの表記ミスや出品者の誤表記は致命的。日本から買う場合のリスクと回避策を知っておくと無駄な時間・金銭を節約できます。

## 詳細解説
- 問題の本質：GrapheneOSはデバイスのブートローダーをアンロックしてカスタムOSを書き込む必要がある。Swappaでは「Unlocked」表記がある販売が多いが、投稿者は3回連続で実際はOEM/bootloaderが解除できない端末を掴まされた。
- 何が原因か：出品者が「工場出荷時にアンロック可能なGoogle版」を正しく識別できていない、またはマーケット側のモデレーション不足で誤ったカテゴリに上がってしまうケース。さらに返金でPayPal手数料や送料などの損失が発生。
- 技術的背景：ブートローダー解除（OEM unlocking）は設定→開発者向けオプションの有効化や、fastboot経由での操作が必要。端末が「キャリアロック」やGoogleのデバイス保護（Find My Device/FRP）に紐づいていると解除ができないことがある。出荷国・モデル違いでブートローダー挙動が異なる場合もある。
- フォーラムでの工夫：購入前にセラーにブートローダー解除を確認してもらう、発送前に返金対応をしてもらうなど試みたが、供給側が大量在庫をチェックできないため確実性は低い。

## 実践ポイント
- 購入前チェックリスト（最低限）
  1. モデル名とハードウェアSKUを確認（例：Pixel 9 Pro 型番）。
  2. 出品者にfastbootでの確認結果を提示してもらう（例：以下コマンドを実行しスクショを要求）。
```bash
# 出品者に確認してもらうコマンド例
fastboot oem device-info
```
  3. 「Factory unlocked Google edition」か明示的に確認。単に"Unlocked"表記だけを信用しない。
  4. 購入は返金保証と購入者保護がある支払い手段を利用する（クレジットカード、PayPal等）。
  5. 到着後すぐにブートローダー状態を確認し、問題あれば即返送手続き。
- 国内での代替案：日本国内の信頼できる中古販売店や公式認定リファービッシュ業者、あるいはGrapheneOS対応端末の公式互換リストを参照して購入する（リージョン違い・保証の有無に注意）。
- 最後に：マーケットの表記ミスは誰にでも起きる。GrapheneOS導入を最優先するなら、「出品者が実際にブートローダー解除できることを証明できるか」が最重要です。
