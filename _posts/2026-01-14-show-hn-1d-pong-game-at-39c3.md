---
layout: post
title: "Show HN: 1D-Pong Game at 39C3 - 1D-Pongゲーム（39C3で公開）"
date: 2026-01-14T07:42:02.126Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/ogermer/1d-pong"
source_title: "GitHub - ogermer/1d-pong: A simple 1D-Pong game built with an ESP32 (WEMOS D1), a WS2812B LED strip, and two buttons"
source_id: 46579612
excerpt: "LED一列で遊べるESP32×WS2812の1D-Pong、展示向け13種アニメと拡張性が魅力"
image: "https://opengraph.githubassets.com/08dd994c094ed37ba30a3cdd0a532e2bb40c91aa00fb5a1ed027bad4e1f19ab4/ogermer/1d-pong"
---

# Show HN: 1D-Pong Game at 39C3 - 1D-Pongゲーム（39C3で公開）
LED一列で対戦が熱くなる！ESP32とWS2812で作る「1D-Pong」— ワークショップや展示でウケるオープンソース・ゲーム

## 要約
ESP32（WEMOS D1）＋WS2812B LEDストリップ＋2つのボタンで動く1次元のPongゲーム。高速な対戦、可変難易度、13種類のアトラクトアニメーションを備え、PlatformIO/FastLEDで拡張しやすい設計です。

## この記事を読むべき理由
ハードウェア工作やマイクロコントローラ入門、デモ展示を考えている日本のメーカ／ハッカー／教育者にとって、短時間で見栄えの良いインタラクティブ作品を作れる実装例と拡張ポイントが詰まっています。イベント出展や社内ハッカソンの題材にも最適です。

## 詳細解説
- ハードウェア構成  
  - マイコン: WEMOS D1 Mini（ESP32）  
  - LED: WS2812B（例：55個）  
  - 入力: モーメンタリボタン ×2（GPIOでGNDに接続、内部プルアップ使用）  
  - 電源: 5V、推奨3A（LED数に依存）  
  - 追加: ボタンに内蔵LED（PWM出力で点灯）、ボタンLEDはレベルシフタやドライバを推奨

- ソフトウェア構成  
  - PlatformIO + Arduino-ESP32環境、FastLEDライブラリでLED制御  
  - メインは状態機械（IDLE → SERVE → BALL_MOVING → CHECK_GAME_OVER → GAME_OVER）で管理  
  - ゲームルール：ボール（白）を自分の「ゾーン」内でボタンを押して返す。早押しや外押しはペナルティ。ポイントでゾーンが縮小し難度上昇。最初に指定得点（デフォルト5点）で勝利。  
  - アニメーション拡張：src/animations に新しい .cpp を置くだけで自動登録されるモジュール方式。アニメーションは非ブロッキング（delay禁止）で FastLED.show() を使うこと。

- 主要設定（include/config.h）  
  - LED個数、データピン、ボタンピン、ゾーン初期サイズ、最小サイズ、得点目標、球速度（BALL_INITIAL_DELAY_MS）などがマクロで設定可能。  
  - 例：球速度を遅くしたければ BALL_INITIAL_DELAY_MS を増やす（推奨40–80ms）。

- 実装の注意点  
  - 電源容量不足で色飛び・点灯不良になるため5V供給とGND共通接続を確認。  
  - WS2812はデータライン電圧が3.3V–5Vの互換性問題がある場合があるため長配線や電圧差には注意。  
  - アニメーション作成時は millis() ベースで非同期処理にすること。reset() と update(CRGB*, numLeds) を実装する形。

- ビルド／書き込み（VS Code + PlatformIO）  
  - PlatformIO拡張でビルド・書き込みを管理。USB接続、適切なボード選択、ブート押しながらアップロードが必要な場合あり。

コンフィグの抜粋例（編集して試す）:

```cpp
// cpp
#define NUM_LEDS 55
#define LED_PIN 5
#define BUTTON_LEFT_PIN 17
#define BUTTON_RIGHT_PIN 18
#define ZONE_SIZE_START 10
#define ZONE_SIZE_MIN 5
#define SCORE_TO_WIN 5
#define BALL_INITIAL_DELAY_MS 60
```

アニメーション追加の骨子（テンプレート）:

```cpp
// cpp
class MyAnimation : public Animation {
public:
  MyAnimation() : Animation("My Animation") {}
  void reset() override { _last = 0; }
  void update(CRGB* leds, uint8_t numLeds) override {
    if (millis() - _last < 50) return;
    _last = millis();
    fill_solid(leds, numLeds, CRGB::Black);
    // 表示更新
    FastLED.show();
  }
private:
  uint32_t _last = 0;
};
REGISTER_ANIMATION(MyAnimation, "My Animation");
```

## 実践ポイント
- まず試す：リポジトリをクローンしてVS Code + PlatformIOでビルド→ESP32へ書き込み。簡単な改変（LED数や BALL_INITIAL_DELAY_MS）で挙動を確認する。
  - コマンド例:

```bash
# bash
git clone https://github.com/ogermer/1d-pong.git
cd 1d-pong
code .
# PlatformIOでビルド・アップロード（UIか Ctrl+Alt+B / Ctrl+Alt+U）
```

- 電源管理：LED数×最大輝度で消費電流が増えるため、5V/3A以上の安定した電源を用意する。長い配線には電圧降下対策を。  
- ワークショップ化：参加者ごとにゾーンサイズや速度を変えたトーナメントを企画すると盛り上がる。小中学生向けにはルール説明と簡単な「アニメーション作成」ワークショップを組むと学習効果大。  
- 拡張案（すぐできるアイデア）  
  - ブザーで効果音を付ける（GPIO＋トランジスタ）  
  - Bluetooth/Webで設定を変えられるUIを追加（ESP32の強み）  
  - スコア保存（EEPROM）やシングルプレイヤーAI（反射速度ベース）を実装して教育用途に拡張  
- コントリビュート：アニメーション追加やサウンド対応、Web設定UIなどは歓迎されているのでFork→PRで参加可能。

このプロジェクトは「ハードとソフトの両方を触れる」良いサンプルです。短時間で動くデモを作りたい場合や、LED制御／ESP32入門の教材として非常に実用的なので、まずは1台組んで動かしてみてください。
