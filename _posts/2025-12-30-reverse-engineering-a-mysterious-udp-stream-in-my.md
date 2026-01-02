---
layout: post
title: "Reverse Engineering a Mysterious UDP Stream in My Hotel - ホテルで遭遇した不可解なUDPストリームをリバースエンジニアリング"
date: 2025-12-30T17:36:59.055Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.gkbrk.com/hotel-music"
source_title: "Reverse Engineering a Mysterious UDP Stream in My Hotel (2016)"
source_id: 46366010
excerpt: "ホテルWi‑Fiの謎UDPを解析→実はマルチキャストMP3（エレベーター音楽）と判明、手順も解説"
---

# Reverse Engineering a Mysterious UDP Stream in My Hotel - ホテルで遭遇した不可解なUDPストリームをリバースエンジニアリング
ホテルのWi‑Fiで見つけた“謎のUDP”をWiresharkで追跡したら、結末はまさかのエレベーター・ミュージックだった話

## 要約
ホテルのネットワークで大量に流れていたUDPパケット（ポート2046）をキャプチャして解析すると、マルチキャスト経由で配信されるMP3オーディオで、先頭8バイトをスキップすると再生可能なエレベーター音楽だった。

## この記事を読むべき理由
ネットワークで見慣れないポートやトラフィックを見つけたときに、短時間で原因を切り分けるリバースエンジニアリングの実践手順が学べる。Wireshark／Pythonでの解析パターンは運用やセキュリティ調査、IoT機器のトラブルシューティングで役立つ。

## 詳細解説
- 発見と仮説立て  
  Wiresharkで大量のUDPトラフィック（ポート2046）を発見。宛先が自分のIPではなく、多数端末に届いていたため「マルチキャスト」であると判明。パケット長が一定（634バイト）で、最初の数十バイトが毎回同じだったことからプロトコルヘッダ＋ペイロードという構成を推察。

- データ取得（Pythonでマルチキャスト加入）  
  マルチキャストグループ（例: 234.0.0.2）に参加してUDPを受信する最小コード。受信バッファをファイルに保存して中身を確認する。

  ```python
  # python
  import socket, struct
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('', 2046))
  mreq = struct.pack("4sl", socket.inet_aton("234.0.0.2"), socket.INADDR_ANY)
  s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
  while True:
      data = s.recv(2048)
      print(data)  # まずは中身を覗く
  ```

- ペイロード解析のコツ  
  バイナリを16進で眺め、繰り返し部分や文字列（例: "LAME3.91"）を探す。ツールはfile/xxd/binwalkなどが有効。今回は" LAME3.91UUUUUUU"の痕跡があり、MP3（MPEG Audio）である可能性が高いと判断。

- オフセット探索（簡単なトリック）  
  ペイロード先頭に余分なヘッダが付いている場合、Nバイトずつずらして保存→fileコマンドで判定する。著者は先頭8バイトをスキップするとADTS/MP3として認識されることを確認し、連結して再生可能にした。

  ```python
  # python
  data = s.recv(2048)
  for i in range(25):
      with open(f"test{i}.bin","wb+") as f:
          f.write(data[i:])
  # file test* でどのオフセットが有効か確認
  ```

- 結果と示唆  
  連続パケットの先頭8バイトを取り除いた連結ファイルを再生すると、ホテルの廊下で流れているエレベーター音楽だった。技術的には「マルチキャストで配信される音源を配信機器やPAに流す」典型的な仕組みだが、こうした機器がゲストネットワークと同一セグメントに置かれている点は運用上の懸念となる。

## 実践ポイント
- 見慣れないUDPトラフィックを見つけたらまずWiresharkで宛先（ユニキャスト／マルチキャスト）とパケット長の一貫性を確認する。
- マルチキャスト解析は上記のようなPythonスクリプトで簡単に受信できる。受信したバイナリはfile/binwalk/xxdで痕跡（MPEGヘッダ、LAMEタグなど）を探す。
- ヘッダが付いているケースでは「オフセットずらし」でフォーマット開始点を探索するのが手っ取り早い（ただし再送や同期の仕組みがある場合は別途処理が必要）。
- セキュリティ面：BSSIDやネットワーク分離が不十分だと、音声配信や監視機器がゲストと同一ネットワークに露出するリスクがある。企業や施設ではネットワークセグメント分離とACLの実装を推奨。
- 注意：他者のネットワークに対するパケット注入や配信の改変は不正行為にあたる可能性があるため実験は必ず管理者の許可を得て行う。

