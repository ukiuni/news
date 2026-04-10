---
layout: post
title: "You can't trust macOS Privacy and Security settings - macOSの「プライバシーとセキュリティ」は信頼できない"
date: 2026-04-10T16:01:11.345Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eclecticlight.co/2026/04/10/why-you-cant-trust-privacy-security/"
source_title: "Why you can&#8217;t trust Privacy &amp; Security &#8211; The Eclectic Light Company"
source_id: 47719602
excerpt: "macOS設定が「アクセス無効」でもOpenパネル経由でDocumentsを永続的に読み取られる危険"
image: "https://eclecticlight.co/wp-content/uploads/2026/04/insenticon.jpg"
---

# You can't trust macOS Privacy and Security settings - macOSの「プライバシーとセキュリティ」は信頼できない
「設定が『ブロック』を示していても、アプリはあなたの Documents を覗ける」――見た目に騙されるmacOSの権限挙動

## 要約
macOSのFiles & Folders欄に「アクセス無効」と表示されていても、ユーザー操作（Openパネル等）で一度与えられたフォルダアクセスが恒久的に有効化され、設定画面が実際のアクセス状態を正確に反映しないことがある、というデモと解析。

## この記事を読むべき理由
日本でも個人・社内でMacを使う場面は多く、知らないうちに重要フォルダがアプリに読み取られるリスクがあるため、誤解しやすい権限表示と対処法を短く押さえておくべきです。

## 詳細解説
- 検証に使われたのはInsent（署名済みの普通のアプリ）。作者はmacOS Tahoe（26.4）で検証しており、macOS13.5以降で同様に見える可能性が高い。  
- Insentの2つの操作が鍵：  
  1. 「Open by consent」：アプリ側からDocumentsの一覧取得を試み、TCC（Transparency, Consent, and Control）が介入してユーザー同意を要求 → 同意でアクセス許可される（ログにsandboxd→TCCのやり取りが残る）。  
  2. 「Open from folder」：ユーザーがOpenパネルでフォルダを選択する「ユーザー意図」によるアクセス。ここではsandboxdが介入しないためTCCの承認プロセスを経ずにファイル操作でき、その結果として以後アプリが同フォルダへ継続してアクセス可能になるケースがある。  
- 重要点：Files & Foldersのトグルで「無効」にしても、Openパネルを経由して与えられたアクセスは残り、表示と実際のアクセス制御が一致しない。ログや検証から、フォルダに付与される拡張属性（com.apple.macl）など低レイヤーの仕組みが関与していると考えられる。  
- リセット方法はやや専門的：TCCのリセットコマンドで直る場合があるが、com.apple.maclのxattrを削除するにはリカバリ環境での操作が必要になることもある。

## 実践ポイント
- 確認の手順（再現・検査用）: Insentのような挙動を試すことで自分の環境を確認する。  
- 表示を鵜呑みにしない：System Settings → Privacy & Security → Files & Folders の表示は必ずしも「現行のアクセス権限状態」を正確に示さない。  
- アクセスを取り消す（例）:
```bash
bash
# アプリ固有のTCCをリセット（bundle id を置き換えて使用）
tccutil reset All co.eclecticlight.Insent
# 特定フォルダのcom.apple.maclを削除する（リカバリ環境で実行する可能性あり）
xattr -d com.apple.macl /Users/yourname/Documents
```
- 管理運用での対策：社内MacではプロファイルやMDMでの権限制御、アプリの配布元／署名確認、ユーザーに対する「Openダイアログで保護フォルダを安易に選ばない」教育が現実的対策。  
- 万一の疑いがある場合は、該当アプリをアンインストールしてTCCリセットと再起動、必要ならMDM/管理者に相談する。

以上。
