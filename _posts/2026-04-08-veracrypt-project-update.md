---
layout: post
title: "Veracrypt Project Update - VeraCrypt プロジェクトの更新"
date: 2026-04-08T09:07:58.282Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://sourceforge.net/p/veracrypt/discussion/general/thread/9620d7a4b3/"
source_title: "VeraCrypt / Forums /   General Discussion: Project Update"
source_id: 47686549
excerpt: "VeraCryptのWindows署名が停止、Secure Bootでインストール不可になる恐れあり"
---

# Veracrypt Project Update - VeraCrypt プロジェクトの更新
VeraCrypt開発に緊急事態：Windows署名が停止され、ユーザーの安全性と配布に直撃

## 要約
VeraCryptの開発者がMicrosoftのドライバー署名用アカウントを一方的に停止され、Windows向けの正式リリース（署名付きドライバーとブートローダー）を発行できなくなった。Linux/macOS側は影響が小さいが、Windowsユーザーへの影響は大きい。

## この記事を読むべき理由
Windowsが主流の日本市場では、Windows向けドライバーの署名喪失はインストール不能、Secure Bootとの互換性問題、ポータブル利用の制約など実用面で直接影響するため、企業・個人問わず知っておくべき重要事象です。

## 詳細解説
- 何が起きたか：開発者が長年使用してきたMicrosoftのPartner/署名アカウントが通知なしで停止され、異議申し立て不可とされている。結果としてWindows用の公式署名付きビルドを公開できない状況。
- なぜ深刻か：Windowsのカーネルモードドライバーやブートローダーは署名要件が厳しく、署名が無ければOSが読み込まない／インストールできないケースがある。特にSecure Boot環境では古いCAの有効期限切れや署名の不整合が問題になる（例：現行バージョンは古いCAで署名されており、期限切れが影響する懸念あり）。
- 影響範囲：Linux/macOSは通常通り更新可能。だがWindowsユーザーは（1）公式アップデートを受け取れない、（2）サードパーティや自前ビルドの未署名ドライバーを使う場合にSecure Bootの無効化が必要になる可能性、（3）ポータブル版やマウント動作が制限される可能性がある。
- コミュニティの対応案：Microsoftへの再接触、ソーシャルでの状況周知、別アカウントでの再登録／EV証明書・アテステーション署名の取得、署名独立の「アーカイブ型」機能追加で当面の代替とする提案など。

## 実践ポイント
- 公式アナウンスを注視：プロジェクトのフォーラム/リポジトリをフォローして正式対応を待つ。  
- 署名を確認：Windows版を使う際は配布元の署名状態を確認し、疑わしいビルドは避ける。  
- バックアップと検証：重要データのバックアップを取った上で、署名問題が解決するまで不要な再インストールは控える。  
- 回避策の検討：Linux/macOS環境で更新を続けるか、自己ビルドやポータブル運用を検討する（ただしセキュリティ・互換性のリスクを理解すること）。  
- 貢献/支援：プロジェクトに技術支援や資金援助、署名に詳しい協力者の紹介などで支援できる場合は協力を検討する。

（出典：SourceForgeフォーラム「Veracrypt Project Update」掲示の開発者投稿およびスレッドの要約）
