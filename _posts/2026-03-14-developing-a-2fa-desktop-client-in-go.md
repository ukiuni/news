---
layout: post
title: "Developing a 2FA Desktop Client in Go - Goで作る2FAデスクトップクライアント"
date: 2026-03-14T18:43:22.749Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.youtube.com/watch?v=HFu3CUtrOQ8"
source_title: "Developing a 2FA Desktop Client in Go - YouTube"
source_id: 1437663176
excerpt: "GoでQR/キーチェーン対応の安全な2FAデスクトップクライアントを実装解説"
image: "https://i.ytimg.com/vi/HFu3CUtrOQ8/maxresdefault.jpg"
---

# Developing a 2FA Desktop Client in Go - Goで作る2FAデスクトップクライアント
Goで自分だけの2要素認証クライアントを作って、秘密鍵の管理と利便性を両立する方法

## 要約
YouTube動画「Developing a 2FA Desktop Client in Go」を基に、TOTPベースのデスクトップ2FAクライアントをGoで実装する際の設計ポイントと実践的な注意点を初心者向けに解説します。

## この記事を読むべき理由
2要素認証は国内外で標準化が進む中、社内ツールや個人ユーティリティを安全に自作できれば運用コスト削減やセキュリティ向上に直結します。Goはクロスコンパイル性と軽量ランタイムでデスクトップユーティリティに向いており、日本の開発者にも実践価値が高いです。

## 詳細解説
- 基本プロトコル：一般的な2FAはTOTP（RFC 6238）を使用。共有秘密（base32）＋時刻（通常30秒）＋HMAC-SHA1でワンタイムコードを生成します。実装では公式ライブラリや定番パッケージ（例：github.com/pquerna/otp/totp）を使うと安全かつ短時間で動きます。
- 秘密の取り扱い：秘密鍵は平文で残さないこと。OSのキーチェーン（macOS Keychain、Windows Credential Manager、LinuxのSecret Service）を使うか、ローカルでAES-GCM＋パスフレーズで暗号化して保存します。Goなら go-keyring や golang.org/x/crypto を検討。
- QRコード / プロビジョニング：既存サービスからのQR読み取り（ユーザー登録）と、エクスポート用QR生成（バックアップ）を実装。qrライブラリで生成・表示し、読み取りは外部ライブラリやカメラ入力を使う。
- UI選択肢：軽量GUIは Fyne や Gio がGoでの選択肢。シンプルなトレイ常駐アプリでワンタイムコードをコピーするUXが好まれます。
- 同期と時計ずれ：NTPで時刻同期を確認、検証時に±1ウィンドウ程度を許容してユーザーの時計ずれに対応。
- セキュリティ設計：スレッドセーフなシークレット管理、クリップボード自動クリア（数秒後）、ローカルエクスポートは暗号化のみ許可。ネットワーク送信は避けるか、厳格に監査・暗号化する。
- ビルドと配布：GoのクロスコンパイルでWindows/macOS/Linuxバイナリを作成。goreleaserで署名・パッケージ化。社内配布ならMDMや社内リポジトリを利用。

簡単なコード例（TOTP生成）
```go
package main

import (
	"fmt"
	"time"

	"github.com/pquerna/otp/totp"
)

func main() {
	secret := "JBSWY3DPEHPK3PXP" // base32
	code, err := totp.GenerateCode(secret, time.Now())
	if err != nil {
		panic(err)
	}
	fmt.Println("TOTP:", code)
}
```

## 実践ポイント
- まずはTOTP生成だけのCLIを作って挙動を確認する（ライブラリ利用でOK）。
- 秘密は最初からOSキーチェーンに格納する設計にする（平文保存禁止）。
- QRの読み取り／生成、クリップボード管理、UIは段階的に追加。
- NTPチェックとクリップボード自動クリアは必須レベルの実装項目。
- 配布は署名＋リリースノートで透明性を確保。社内導入なら運用ポリシーを整備すること。

元動画を参考に、まずは小さなプロトタイプを作って挙動とリスクを体感することをおすすめします。
