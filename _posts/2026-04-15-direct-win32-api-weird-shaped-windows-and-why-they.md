---
layout: post
title: "Direct Win32 API, Weird-Shaped Windows, and Why They Mostly Disappeared - 直接Win32 APIと変形ウィンドウ、なぜほとんど消えたのか"
date: 2026-04-15T12:11:21.914Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://warped3.substack.com/p/direct-win32-api-weird-shaped-windows"
source_title: "Direct Win32 API, Weird-Shaped Windows, and Why They Mostly Disappeared"
source_id: 47776667
excerpt: "Win32で独創的な変形ウィンドウを作れるが、保守と互換性の問題でほぼ消えた理由と実践法を解説"
image: "https://substackcdn.com/image/fetch/$s_!Ogvq!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8583506a-b1b6-4ca3-9eb9-8e7f674b05b7_1130x362.gif"
---

# Direct Win32 API, Weird-Shaped Windows, and Why They Mostly Disappeared - 直接Win32 APIと変形ウィンドウ、なぜほとんど消えたのか

「角丸だけじゃ物足りない」──Windowsの“個性ある”ウィンドウが消えた理由と、今でもできること

## 要約
Win32 APIを直接使えば、ウィンドウを楕円やビットマップ形状、さらにはアニメーションするマスコットにすることができる。一方で、フレームを自前で置き換えるとドラッグ、ヒットテスト、DPI対応など全て自分で担う必要があり、保守性の低さからこうした表現はほぼ姿を消した。

## この記事を読むべき理由
日本でもElectronなどのWebラップアプリが増え、メモリやパフォーマンスの問題が話題になる中、Win32の「軽さ」と「自由度」はニッチだが有用。UIに個性を出したいツール系やデスクトップの小物作りに直接役立つ知識だから。

## 詳細解説
- コアモデル：Win32はイベント（メッセージ）駆動。自分でループを受け取り、WM_*メッセージごとに挙動を作る設計が基本。  
  例（簡略）:
  ```C
  while (GetMessage(&msg, NULL, 0, 0) > 0) {
      TranslateMessage(&msg);
      DispatchMessage(&msg);
  }
  ```
- 形状変更の方法：
  - HRGN（領域）を用いる。CreateEllipticRgnで楕円領域を作り、SetWindowRgnでウィンドウに適用すると実際のHWNDがその形になる。
  - ビットマップ由来：GetDIBitsでピクセルを読み、透明色（例：マゼンタ）を除外して水平ランで小さな矩形領域を組み合わせ、複雑なシルエットを作る。これが昔のスキンアプリによく使われた。
  - レイヤードウィンドウ：透過やソフトエッジ、アニメーションが欲しい場合は WS_EX_LAYERED と UpdateLayeredWindow を使い、32-bitアルファ付きビットマップを毎フレームアップロードする。これでピクセル単位の透過と滑らかな表示が得られる。
- 現代的に消えた理由：
  - フレームを捨てると、ドラッグ（WM_NCLBUTTONDOWNでHTCAPTIONを送る小ワザなど）、リサイズ、ヒットテスト、キーボード操作、DPI対応、再描画の整合性など全て自前になる。手間とバグが増え、企業やユーザーは「確実に動くこと」を選んだ。
  - WebベースのUIは開発工数やクロスプラットフォーム性を優先し、結果として見た目は均一化。変形ウィンドウは“ギミック”や広告ツールの印象もあり敬遠された。

## 実践ポイント
- 小さな実験から：まずは楕円ウィンドウ（CreateEllipticRgn + SetWindowRgn）で挙動を学ぶ。タイトルバーを消したらWM_LBUTTONDOWN→WM_NCLBUTTONDOWN(HTCAPTION)でドラッグを再現するのを忘れずに。  
- 透過やアニメーションが必要なら WS_EX_LAYERED + UpdateLayeredWindow を採用する（毎フレームの描画コストを意識）。  
- 本格採用は慎重に：ユーザー体験と保守コストを天秤に。ツールやデスクトップアクセサリの「個性演出」なら効果的だが、業務系UIでは四角の信頼性が優先される。  
- 参考：元記事のGitHubサンプルを読むと具体実装が学べるので、手を動かして理解するのが早い。

短くまとめると、Win32はいまでも「ウィンドウ自体をデザインする自由」を与えてくれるが、それを選ぶかは手間とUXの天秤次第。興味があれば、まず小さなプロトタイプを作ってみてください。
