---
layout: post
title: "Modifying FileZilla to Workaround Bambu 3D Printer's FTP Issue - Bambu 3DプリンタのFTP問題を回避するためのFileZilla改造"
date: 2026-04-14T18:07:21.032Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://lantian.pub/en/article/modify-computer/modify-filezilla-workaround-bambu-3d-printer-ftp-issue.lantian/"
source_title: "Modifying FileZilla to Workaround Bambu 3D Printer&#39;s FTP Issue - Lan Tian @ Blog"
source_id: 47768306
excerpt: "LinuxでBambuプリンタのPASV 0.0.0.0問題をFileZillaパッチで即修正"
image: "https://lantian.pub/apple-touch-icon.png"
---

# Modifying FileZilla to Workaround Bambu 3D Printer's FTP Issue - Bambu 3DプリンタのFTP問題を回避するためのFileZilla改造
LinuxでBambu A1系プリンタのFTPにログインできるのにファイル一覧が取れない？原因はプリンタのPASV応答が返す「0.0.0.0」—FileZillaのソースを少し直して解決できます。

## 要約
BambuプリンタのFTPサーバがPASV応答でIPを0.0.0.0と返すため、FileZillaが正しくデータ接続できない。WinSCPは設定で回避できるが、Linux利用者向けにFileZillaのソースに小さなパッチを当てる方法を示す。

## この記事を読むべき理由
- Linux環境でBambuプリンタのFTPを使いたい開発者・ホビイスト向けに、原因と実践的な修正法（簡単なパッチと再ビルド手順）を端的に示す。

## 詳細解説
- FTPは制御コネクション（通常ポート21）とデータコネクションを分ける古典的プロトコル。データ接続方式はActive（PORT）とPassive（PASV）がある。クライアントが接続を開始するPassiveが一般的。
- PASV応答はサーバ側のIP:portを返すが、BambuのファームウェアはIP部分を0.0.0.0で返すことがある。0.0.0.0は宛先として無効で、OSによって挙動が異なる（Windowsは接続不可、Linux/macOSは127.0.0.1にリダイレクトされる）。
- FileZillaはPASV応答のIPが「private（非ルーティング）」かどうかを判定してフォールバックするロジックを持つが、現行実装だと0.0.0.0を「ルーティング可能（public）」扱いしてしまい、置換処理が実行されない。
- 解決は簡単：rawtransfer.cppの処理に「host_ が 0.0.0.0 の場合も置換（peerIPを使う）」という条件を追加するパッチを当てる。

例：該当部分の修正（抜粋）

```cpp
cpp
std::wstring const peerIP = fz::to_wstring(controlSocket_.socket_->peer_ip());
std::wstring const zeroIP = fz::to_wstring(std::string("0.0.0.0"));
if (
    std::wcscmp(host_.c_str(), zeroIP.c_str()) == 0
    || (!fz::is_routable_address(host_) && fz::is_routable_address(peerIP))
) {
    // 既存のフォールバック処理（peerIPを使う等）
    host_ = peerIP;
    ...
}
```

- この変更後にFileZillaを再コンパイル・インストールすれば、Linux上でもBambuプリンタのFTPでファイル一覧取得・アップロードが可能になる。

## 実践ポイント
- 手順（要約）：
  1. FileZillaのソースを入手（公式リポジトリ）。
  2. src/engine/ftp/rawtransfer.cpp に上記の条件を追加するパッチを適用。
  3. ビルドしてインストール（配布ディストリ向けビルド手順に従う）。
- Windowsの代替：WinSCPの「Force IP address for passive connections」を有効にすると同様の回避が可能。
- Bambu接続情報（例）：
  - ホスト: ftps://<プリンタのIP>（例: ftps://192.168.12.34）
  - ユーザー: bblp
  - パスワード: プリンタの設定 → LAN にある8桁のアクセスコード
  - ポート: 990（暗黙のFTPSを選択）
  - 備考: LANモードを有効にするとクラウド機能を止める挙動があるため注意。
- リスク：公式ビルドを上書きするため、アップデート時に差分が戻る可能性あり。自己責任で管理すること。

以上。必要なら、ビルドコマンドやパッチファイルの完全版を添えて案内できます。
