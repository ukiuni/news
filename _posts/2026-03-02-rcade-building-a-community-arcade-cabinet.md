---
layout: post
title: "RCade: Building a Community Arcade Cabinet - コミュニティ筐体「RCade」を作る"
date: 2026-03-02T23:20:42.416Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.frankchiarulli.com/blog/building-the-rcade/"
source_title: "RCade: Building a Community Arcade Cabinet — frankchiarulli.com"
source_id: 47170599
excerpt: "GitHub連携で即デプロイ、CRT実機で遊べるコミュニティ筐体RCadeの全貌"
image: "https://frankchiarulli.com/blog/building-the-rcade/opengraph-image?2a7b637ea0cacf29"
---

# RCade: Building a Community Arcade Cabinet - コミュニティ筐体「RCade」を作る
コミュニティが作る実機レトロ筐体――GitHubで誰でも数分で実機にゲームをデプロイできる仕組み

## 要約
Recurse Center の RCade は、本物のCRT、カスタム表示/操作系、GitHub→OIDCベースの自動デプロイ、ブラウザサンドボックスでコミュニティ製ゲームを実機で動かすプロジェクトです。

## この記事を読むべき理由
レトロハードの制約を逆手に取ったコミュニティ開発、低レイヤな映像入出力の工夫、CI/OIDCを使ったパスワードレスデプロイ、そして安全なブラウザ実行環境――日本のメイカースペース、大学研究室、インディーゲーム開発者にとって学びが多い実例です。

## 詳細解説
- ハードウェアの核：オリジナルCRTを残した理由は「制約が創造性を刺激する」ため。アーケードCRTは水平同期が約15.7kHzで、一般的なVGA（31.5kHz）とは物理的に異なるため、専用タイミングが必要。
- 信号解析：筐体のネックボードからRGB、H/V syncをオシロスコープでトレースし、JAMMAコネクタを実装。JAMMAは古典アーケードの標準で、映像・音声・電源・操作を1つで扱えます。
- vga666（Raspberry Pi）での暫定対応：GPIO抵抗DACでアナログRGBを出力。18bitカラーの制約はあるが、正しいタイミングを与えれば15kHzモニタで動作する。例：/boot/config.txt の主要パラメータ例：
```bash
dtoverlay=vc4-kms-dpi-generic
dtparam=clock-frequency=5700000,hactive=320,hfp=9,hsync=16,hbp=18
dtparam=vactive=240,vfp=2,vsync=3,vbp=17
dtparam=hsync-invert,vsync-invert
```
これで 320×240、約60fps（15.7kHz水平）を実現。

- カスタム表示アダプタ：PiのGPIO依存を脱するため、STM32H750＋精密DACで24bit/60fpsを実装。WebGPUが動くPCを使えるようになり色バンディングが解消。
- 入力系：RP2040ベースのコントローラ。8方向レバー、2ボタン、スピナー（ロータリエンコーダ）をUSB HIDとして報告。スピナーはA/B位相を1kHzでサンプリングして回転量を軸値に変換。
- マーキー＆筐体表現：HUB75 LED行列＋チョークボードラップでコミュニティアート化。
- ソフトウェアと開発体験：npm create rcade でゲーム雛形＋GitHub Actionsワークフローを生成。ワークフローは GitHub OIDC（id-token: write）で短時間JWTを取得し、RCade APIがそれを検証してデプロイ許可を与える。秘密鍵を置かない「パスワードレス」なCI認証。
- セキュリティ：ユーザーゲームは別オリジンの iframe +厳格な CSP でサンドボックス化。fetch/Storage/WebSocket/親フレームアクセス等をブロック。筐体操作はプラグイン（Trusted code）経由で postMessage する仕組み。

サンプル：ゲーム側からの入力利用例（プラグイン経由）
```js
import { PLAYER_1, SYSTEM } from "@rcade/plugin-input-classic";

function loop() {
  if (PLAYER_1.DPAD.up) moveUp();
  if (PLAYER_1.A) fire();
  if (SYSTEM.ONE_PLAYER) startGame();
  requestAnimationFrame(loop);
}
```

## 実践ポイント
- レトロ筐体を使うならまずJAMMAコネクタとモニタの水平周波数（約15.7kHz）を理解する。タイミングはconfig.txtで細かく調整可能。
- 試作はvga666＋Raspberry Piで始め、色が重要なら専用DAC/STM32等でアップグレードする。
- インディー向けに公開するなら、GitHub Actions＋OIDCで秘密管理コストを下げる設計を検討する。
- 共用ハードで実行する場合は iframe+CSP+プラグイン方式で入出力とネットワークを厳しく制限すること。
- 日本のメイカースペースや大学、ゲームコミュニティでは「物理的な交流＋リモート開発」をつなぐ教材として導入価値が高い。興味があれば筐体再現や小型版（HUB75/Piベース）から始めると良い。

---
