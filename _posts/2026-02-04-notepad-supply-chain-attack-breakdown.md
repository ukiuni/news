---
layout: post
title: "Notepad++ supply chain attack breakdown - Notepad++ 供給連鎖（サプライチェーン）攻撃の解析"
date: 2026-02-04T00:00:42.149Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://securelist.com/notepad-supply-chain-attack/118708/"
source_title: "Notepad++ supply chain attack breakdown | Securelist"
source_id: 46878338
excerpt: "Notepad++更新を悪用した巧妙な供給連鎖攻撃でCobalt Strikeが配布"
image: "https://media.kasperskycontenthub.com/wp-content/uploads/sites/43/2026/02/03072543/notepad-supply-chain-attack-featured-image.jpg"
---

# Notepad++ supply chain attack breakdown - Notepad++ 供給連鎖（サプライチェーン）攻撃の解析
魅了タイトル: 「人気エディタが攻撃経路に——Notepad++更新を狙った巧妙なサプライチェーン攻撃の全貌」

## 要約
Notepad++ の更新インフラが乗っ取られ、2025年7月〜10月にかけて複数の手口（NSISインストーラ、ProShow脆弱性悪用、Luaローダーなど）で悪意あるペイロード（Metasploit→Cobalt Strike）を配布していた。攻撃者はC2や配布URLを頻繁に切り替えていた。

## この記事を読むべき理由
国内でも広く使われる軽量エディタが供給連鎖で狙われた事例は、自社ツールチェーンとソフト配布の信頼性を再点検する好機。初心者でも取れる防御策が明確になるため必読。

## 詳細解説
- 期間と対象: 2025年7月〜10月に活動。被害想定は個人（ベトナム、エルサルバドル、オーストラリア）、フィリピンの政府機関、エルサルバドルの金融機関、ベトナムのIT事業者など。
- 侵害の基本流れ: 正規のアップデータ（GUP.exe）を悪用して改竄された update.exe を実行→初期情報を外部に送信→次段を展開してリモート制御（Cobalt Strike Beacon）を取得。
- 使われた技術（チェーン別の要点）:
  - Chain #1（7月〜8月）: %appdata%\ProShow 経由。NSISインストーラがsystem情報を curl + temp.sh に送信し、ProShow の古い脆弱性を悪用して Metasploit ダウンローダで Cobalt Strike を取得。通信先に 45.77.31.210 と cdncheck.it[.]com などを使用。
  - Chain #2（9月）: %APPDATA%\Adobe\Scripts に Lua 実行環境を展開し、compiled Lua スクリプトでメモリ実行（EnumWindowStationsW 経由）→同様に Metasploit→Cobalt Strike。temp.sh を使った情報送信は継続。safe-dns / self-dns 等へ切替あり。
  - Chain #3（10月）: 配布IPや落とし先ディレクトリを更に変更（例: %appdata%\Bluetooth）、システム情報送信を省略するバージョンも確認。
- 共通点: C2やダウンロードURLを頻繁に変更、正規ソフトやライブラリ（ProShow 実行ファイルや Lua ランタイム）を“正規のまま”悪用して実行経路を隠蔽。
- 検知と被害防止: Kaspersky のテレメトリで検出・ブロックされた事例が報告されているが、少数マシンには侵入が成功している可能性あり。

## 実践ポイント
- Notepad++ の自動更新を一時停止し、公式配布元（公式サイトまたは信頼できるミラー）からのみ手動で更新する。
- GUP.exe や updater 実行時の外向き通信をネットワークで監視・制限（特に不審な IP: 45.76.155.202 / 45.77.31.210 / 45.32.144.255 やドメイン cdncheck.it[.]com / safe-dns.it[.]com / self-dns.it[.]com、及び temp.sh への POST）。
- エンドポイントでのファイル整合性チェック（NSIS インストーラや更新ファイルのハッシュ確認）とアプリケーション許可リスト（AppLocker 等）を導入。
- %APPDATA% 内の不審フォルダ（ProShow, Adobe\Scripts, Bluetooth 等）を定期スキャンし、未知の実行ファイルや DLL を調査。
- 社内開発・運用者はサプライチェーンリスクを意識し、ソフト配布経路の多層防御（コード署名検証、TLS pinning、配布サーバの監査）を検討する。

（参考として、攻撃で確認された手口は Metasploit ダウンローダ → Cobalt Strike Beacon の連鎖、temp.sh を使ったメタデータ抜き取り、正規バイナリの悪用など。）
