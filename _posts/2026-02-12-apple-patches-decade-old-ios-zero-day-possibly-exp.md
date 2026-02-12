---
layout: post
title: "Apple patches decade-old iOS zero-day, possibly exploited by commercial spyware - Apple、10年以上続くiOSゼロデイを修正──商用スパイウェアが悪用の可能性"
date: 2026-02-12T15:18:08.287Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.theregister.com/2026/02/12/apple_ios_263/"
source_title: "Apple patches decade-old iOS zero-day exploited in the wild • The Register"
source_id: 46989107
excerpt: "Appleが10年以上のdyldゼロデイを修正、ゼロクリックで端末乗っ取りの恐れ"
image: "https://regmedia.co.uk/2023/12/01/apple_shutterstock.jpg"
---

# Apple patches decade-old iOS zero-day, possibly exploited by commercial spyware - Apple、10年以上続くiOSゼロデイを修正──商用スパイウェアが悪用の可能性

驚きの「玄関の鍵」を直すアップデート：Appleがダイナミックリンカ(dyld)の重大なゼロデイを修正し、過去10年以上のiOSが影響を受けていた可能性があります。

## 要約
GoogleのThreat Analysis Groupが報告したCVE-2026-20700は、dyld（iOSの動的リンカ）に存在する脆弱性で、メモリ書き込み権限が得られると任意コード実行を許すもので、AppleはiOS 26.3で修正し「実際に悪用された可能性」があると発表しました。

## この記事を読むべき理由
日本は世界でも高いiPhone普及率を持ち、経営者やジャーナリスト、公共の立場にある人物が標的になりやすい点から、ゼロクリックに繋がるような高度な攻撃が国内にも直接的な脅威になります。個人や組織の端末防御の優先度を再確認すべきです。

## 詳細解説
- 問題の本質：CVE-2026-20700はdyld（dynamic linker）に関する脆弱性で、dyldはアプリ実行前にコードを読み込み・配置する「玄関の門番」に相当します。ここを壊されると、アプリ単位のサンドボックスを迂回して任意のコードを実行できます。  
- 悪用シナリオ：単体では「メモリを書き込める」状況を要求しますが、WebKitなどのブラウザ系の脆弱性（例：CVE-2025-14174、CVE-2025-43529、どちらも高いCVSS）と組み合わせることで、ユーザー操作不要の「ゼロクリック」やワンクリックで端末全体を制御するチェーンが成立します。  
- 発見と対応：Googleの調査で確認され、AppleはiOS/iPadOS 26.3で修正を配布。Appleの説明ではこの脆弱性のみが「実際に悪用された可能性あり」とされています。セキュリティ研究者は、こうしたチェーンが商用スパイウェア業界（Pegasusなど）で使われる攻撃に類似すると指摘しています。  
- なぜ重大か：dyldは全てのアプリ起動で関与する低レイヤーのコンポーネントのため、ここを掌握されると個別アプリの制限を超えた深刻な侵害が発生します。

## 実践ポイント
- 今すぐ：iPhone/iPadをiOS/iPadOS 26.3にアップデートする（自動更新を有効化）。  
- 運用面：企業はMDMで端末を一斉更新し、管理下デバイスのOSバージョンを監視する。  
- 検出と対応：標的型の可能性がある場合は専門ベンダーやインシデント対応チームに相談し、疑わしい端末はネットワーク切断・バックアップ作成後にクリーンOS再導入を検討。  
- 予防策：不審な構成プロファイルや検証されていないアプリを避け、Apple IDの2要素認証を有効にする。ゼロクリック攻撃の性質上「リンクを踏まない」だけでは不十分なので、OSパッチの適用が最重要です。
