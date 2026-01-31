---
layout: post
title: "Nintendo DS code editor and scriptable game engine - Nintendo DS用コードエディタとスクリプタブルゲームエンンジン"
date: 2026-01-31T23:44:30.576Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://crl.io/ds-game-engine/"
source_title: "DS code editor &amp; scriptable game engine - Carl Enlund"
source_id: 46839215
excerpt: "Nintendo DS上でタッチ操作でコードを書き即遊べる3Dゲームエンジン約100KB・60FPS"
---

# Nintendo DS code editor and scriptable game engine - Nintendo DS用コードエディタとスクリプタブルゲームエンンジン
DS本体だけで「その場で書いて遊べる」――タッチでコードを書く3Dゲームエンジンが生まれた

## 要約
Nintendo DS上で動く小型のスクリプタブル3DゲームエンジンとタッチベースのコードエディタをC（libnds）で実装し、約100KBの.nts ROMで60FPS動作するプロジェクト。

## この記事を読むべき理由
レトロハードを使った実機での開発体験を手軽に再現でき、限られたリソースで動作するシンプルなスクリプト言語やレンダリング手法は教育用途や日本のホームブリュー／ものづくりコミュニティで即応用可能です。

## 詳細解説
- 構成は大きく3つ：上画面はハードウェア3Dレンダリング、下画面はソフトウェア描画のタッチ式コードエディタ、実行系は1フレームにつき1行を実行する簡易インタプリタ。
- 3D描画はlibndsのハードウェア機能を利用し、カメラ位置・角度や各モデルの位置・Y軸回転・カラーを設定。DS本体で60FPSを実現しています。例：
```c
// C
glMatrixMode(GL_MODELVIEW);
glLoadIdentity();
gluLookAt(camX, camY, camZ, camX+lookX, camY+lookY, camZ+lookZ, 0,1,0);
```
- 下画面は256×192ピクセルのビットマップにUIをピクセル描画。トークンピッカーや数値パッド、変数選択、再生制御を備えます。
- スクリプト言語はトークン列ベースで、変数A〜Z（26個）、読み取り専用の入力・状態レジスタ（十字キー、ボタン、経過時間等）を持つ。コマンドはSET/ADD/MULTIPLY、LOOP/END_LOOP、IF_GT/IF_LT/IF_TRUE、MODEL/POSITION/CAM_POSなど。実行はifチェーンによるトークン比較でオーバーヘッドを最小化。
- デフォルトで3Dポングが入っており、ボールとパドルをモデルで表現し、スクリプトだけで衝突判定やサウンド、ゲームオーバー処理を実現しています。例（抜粋）：
```c
// 簡易なスクリプト実行処理（擬似）
if (tokenEquals(script[ip], "add")) {
  int r = scriptReg[ip];
  registers[r] += getNumberParamValue(ip, 0);
  ip++;
}
```
- 技術スタック：言語はC、libnds、devkitProでビルド。ソースは約3,100行、生成ROMは約100KB。制限としては最大128行のスクリプト、最大16モデル、静的配列のみ、文字列や関数呼び出しは未対応。

## 実践ポイント
- 試すには：devkitPro + libndsを入れてソースをビルド（makeで program.nds を生成）、エミュレータ（Desmond等）か実機のフラッシュカートで動作確認。  
- 教育・ワークショップ案：変数・ループ・条件分岐の動作を視覚化する教材として最適。短いスクリプトで即座に3D変化が見えるので入門に向く。  
- 日本のコミュニティ活用：DSホームブリューやレトロゲームイベントでのデモ、ローカルハッカソンのテーマにおすすめ。  
- 拡張アイデア：行数・モデル数の拡張、サブルーチン導入、簡易デバッグ表示の追加で学習性を高められる。

元記事の実装（ビルド手順やROM／実行例）はソース配布ページにまとまっています。興味があればビルド手順や実機での試し方をさらに詳しく案内します。
