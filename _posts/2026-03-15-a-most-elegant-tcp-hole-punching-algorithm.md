---
layout: post
title: "A most elegant TCP hole punching algorithm - 最もエレガントなTCPホールパンチングアルゴリズム"
date: 2026-03-15T06:30:13.222Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://robertsdotpm.github.io/cryptography/tcp_hole_punching.html"
source_title: "A most elegant TCP hole punching algorithm &mdash; Aul Ma&#39;s research facility"
source_id: 47384032
excerpt: "時刻同期だけでインフラ不要、SYN連射でNAT越えを試せる実験的TCPホールパンチ法"
---

# A most elegant TCP hole punching algorithm - 最もエレガントなTCPホールパンチングアルゴリズム
NAT越えを“インフラ無し”で試せる──時刻だけで同期するシンプルなTCPホールパンチ術

## 要約
時刻ベースの決定論的シードからポートとタイミングを導出し、インフラを用意せずにTCPホールパンチを実験できるアルゴリズムを紹介する。非同期ではなく非ブロッキングソケット＋selectで正確なタイミングを取るのが肝。

## この記事を読むべき理由
NAT越えはP2Pサービス・リモートデバッグ・IoTで頻出する問題。複雑なSTUNやサーバ同期を組まず、最小限の実装で挙動を確かめたい日本の開発者／実験者に有用な「テスト可能な」手法だから。

## 詳細解説
- 全体アイデア：両端が通信で何も交換せずとも一致する「バケツ(bucket)」を時刻から算出し、これを擬似乱数の種にして共有ポート列を決定する。後は同時に相手へSYNを連射して接続を作る。
- バケツ算出：各端は時計誤差を許容して同じバケツ番号に収束させる。例えば
  $$
  window = (max\_clock\_error \times 2) + 2
  $$
  $$
  bucket = \left\lfloor \frac{now - max\_clock\_error}{window} \right\rfloor
  $$
  として、$now$ は現地のUNIXタイムスタンプ、$max\_clock\_error$ は許容ずれ（例：20秒）。
- ポート選定：バケツをPRNGのシードにして複数のポートを生成。元記事では大きな素数を掛けて境界を作る：
  $$
  stable\_boundary = (bucket \times 2654435761) \bmod 0xFFFFFFFF
  $$
  そこから randrange で16個程度の候補ポートを作り、実際にbindできるものだけを採用する。
- ソケット周り：重要なのは「アドレス再利用」を積極的に行うことと、socketをcloseしてしまうとRSTやTIME_WAITで壊れる点。必須設定例（Python）：
  ```python
  import socket
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
  ```
  実装は非ブロッキングソケット＋selectで行い、短い間隔でconnect_exを投げ続ける（例：0.01秒スリープでSYNを連射）。
- 勝者選定：複数接続が成功するため、同じ接続を両端で特定する工夫が必要。WAN IPを比較してリーダ／フォロワを決め、リーダが1バイトだけ送信してその接続を「勝者」にする。1バイトにするのはTCPがストリームであるため簡潔に判定するため。
- 制約と現実性：多くの家庭ルータは"equal delta mapping"（内部ポートと外部ポートに差が一定）を採るが万能ではない。NTPで時刻同期しておくこと、OSや仮想環境の時計精度、既存プロセスとのポート競合などが成功率に影響する。

## 実践ポイント
- まず同一LANや自宅ルータ環境でテストして成功率を確認する。ルータによって成功確率が大きく変わる。
- NTPで時刻を合わせ、$max\_clock\_error$ と $min\_run\_window$（例：10秒）を運用ポリシーに応じて調整する。
- 実装は非ブロッキング＋selectで。短い間隔（例：0.01s）でconnect_exを投げるがCPU負荷に注意する。
- ポート生成はバケツを種にしたPRNGで複数を試す。bindできないポートは除外してリトライする設計にする。
- 期待値：すべてのルータで動くわけではない。あくまで「インフラ無しでアルゴリズムを検証するための簡潔な実験手法」として活用すること。

参考実装は元記事のtcp_punch.pyがあるので、まずはローカルで相手を複数端末で立ち上げて挙動を確認してみてください。
