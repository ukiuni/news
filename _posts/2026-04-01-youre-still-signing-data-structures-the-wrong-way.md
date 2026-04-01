---
layout: post
title: "You're still signing data structures the wrong way - あなたはまだデータ構造の署名を間違えている"
date: 2026-04-01T20:25:55.964Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.foks.pub/posts/domain-separation-in-idl/"
source_title: "You&#39;re still signing data structures the wrong way | The FOKS Blog"
source_id: 47605677
excerpt: "IDLに不変の64ビットドメイン識別子を埋め込み、署名の型混同攻撃を防ぐ方法"
---

# You're still signing data structures the wrong way - あなたはまだデータ構造の署名を間違えている
魅力的タイトル案: 署名が"別物"を許す危険——IDLに「ドメイン識別子」を埋め込めば防げる

## 要約
同じバイト列でも別の型として解釈されると、署名・検証で誤認が生じ攻撃に使われる。SnowpackはIDLレベルでランダムな64ビットの「ドメインセパレータ」を埋め込み、署名前にその識別子を結合することでこのクラスの問題を防ぐ提案をする。

## この記事を読むべき理由
- 日本でも金融系、ブロックチェーン、クラウド認証、IoTなどで署名やMAC・暗号化が多用される。型混同による署名偽装は実被害につながるため、設計段階での対策が重要。

## 詳細解説
- 問題の本質：TreeRoot型とKeyRevoke型のようにフィールドがバイト列として一致すると、ある型で署名されたバイト列を別型のメッセージに「貼り付け」て有効に見せかけられる（過去にBitcoin、TLS、JWT等で事例あり）。
- 既存の対処（メソッド名ハッシュやコンテキスト文字列）は手作業で忘れやすく監査が困難。
- Snowpackのアイデア：IDLに不変のランダム64ビットドメインセパレータを埋める。署名時は「ドメインセパレータ || シリアライズされたオブジェクト」を署名対象とし、検証側も同様に再構成して検証する。これにより型の混同は検証で弾かれる。
- 実装面：コンパイラが型に対してGetUniqueTypeID()のようなメソッドを出力し、型のない構造体は署名APIに渡せないよう型システムで安全性を強制する。
- エンコーディング：Snowpackは位置ベースの中間表現（配列）＋最小サイズ整数＋限定的なMsgpackで「正準化された」バイト列を生成し、前方互換・後方互換性を確保する。

コード例（簡略、Go風）
```go
func (t TreeRoot) GetUniqueTypeID() uint64 { return 0x92880d38b74de9fb }

func Sign(key Key, obj VerifiableObjecter) ([]byte, error)
func Verify(key Key, sig []byte, obj VerifiableObjecter) error
```

## 実践ポイント
- IDL（プロトコル定義）側でドメイン識別子を付与する仕組みを採用するか検討する。既存プロジェクトは将来の破壊的変更を避けるために導入を検討。
- ドメイン識別子はプロジェクト内でランダム生成・一意保証し、公開仕様に固定しておく（フィールド追加は可能だが識別子は不変）。
- 暗号鍵を第三者プロジェクトに渡す設計は避ける（同一識別子を悪用されるリスク）。CI/IDEツールで識別子重複検査を自動化する。
- 署名・MAC・暗号化の入力に「型情報」を取り込む慣習をチームで標準化する（ライブラリで強制するのが確実）。
- 日本の金融・Web3系プロダクトは早期導入で監査コスト低減と安全性向上が期待できる。
