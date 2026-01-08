---
  layout: post
  title: "embassy: Modern embedded framework, using Rust and async - embassy：Rustとasyncを使ったモダンな組込みフレームワーク"
  date: 2026-01-08T07:20:39.204Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/embassy-rs/embassy"
  source_title: "GitHub - embassy-rs/embassy: Modern embedded framework, using Rust and async."
  source_id: 1088123895
  excerpt: "RTOS不要で省電力・安全な組込み開発をRustのasyncで実現するEmbassy入門"
  image: "https://opengraph.githubassets.com/942b2dee0104a62162415183d53fe24172e760eaba104f88fd82b01ae4837dde/embassy-rs/embassy"
---

# embassy: Modern embedded framework, using Rust and async - embassy：Rustとasyncを使ったモダンな組込みフレームワーク
組込み開発の常識を変える！Rustの安全性とasyncで省電力・並行処理をシンプルに実現する「Embassy」を試してみたくなる導入ガイド

## 要約
EmbassyはRustのasync/awaitを組込み向けに最適化したフレームワークで、RTOS不要の協調的タスク実行、低消費電力設計、豊富なHALやネットワーク／USB／BLE周辺機能を提供する。高速・安全・省メモリでモダンなデバイス開発を支援するツール群だ。

## この記事を読むべき理由
日本でもIoT機器やバッテリー駆動デバイスの需要が増える中、低消費電力かつ安全な実装方式の選択肢は重要。EmbassyはRTOSを置き換えうる設計で、特にメモリや電力制約の厳しい製品開発に有利になるため、組込みやファームウェアに関わる技術者は知っておくべき技術だ。

## 詳細解説
- コア思想  
  - Rustの利点（ゼロコスト抽象、メモリ安全、型システム）を活かし、async/awaitを組込みで実用化。  
  - asyncタスクはコンパイル時に状態機械に変換され、動的メモリ割当てを使わず単一スタックで動作するため、タスクごとのスタック調整が不要。

- 実行モデルと省電力  
  - 協調型のasync実行（executor）により、アイドル時はコアをスリープ。割込みでタスクを起こす設計で無駄なポーリングを排除し、長いバッテリー寿命を実現しやすい。  
  - 複数のexecutorを優先度付で作れるため、高優先度タスクの事実上のプリエンプションが可能（リアルタイム要件にも対応）。

- 周辺機能（バッテリー）  
  - embassy_time：グローバルなTimer/Instant/Durationを提供し、ハードウェアタイマー周りの面倒を軽減。  
  - ネットワーク：embassy-netでEthernet/IP/TCP/UDP/ICMP/DHCPなどをサポート。asyncでタイムアウトや複数接続処理が簡単。  
  - Bluetooth/LoRa/USB/Bootloader：BLEスタック（trouble, nrf-softdevice 等）、LoRa/LoRaWAN、embassy-usb（CDC/HIDなど）、embassy-boot（安全なファーム更新）など豊富。

- ハードウェア対応（主なHAL）  
  - STM32（embassy-stm32）、Nordic nRFシリーズ（embassy-nrf）、RP2040（embassy-rp）、MSPM0、Espressif（esp-rs/esp-hal 連携中）、ほか多数。日本の開発現場でよく使うSTM32やRP2040、nRF系がサポートされている点は大きい。

- 開発運用のポイント  
  - 例は examples/ 配下にチップ別で整理。実機実行は probe-rs をインストール後、該当例のディレクトリで cargo run --release --bin <例名>。  
  - VS Code 等で Rust Analyzer を使う場合はワークスペース指定（rust-analyzer.linkedProjects）に注意。Embassyは多ターゲットのため単一workspaceがない。  
  - 最低サポートRustバージョン（MSRV）は 1.75 以上。ライセンスは Apache-2.0 / MIT の選択可。

- 短いサンプル（点滅タスクのイメージ）  
```rust
use embassy_executor::Spawner;
use embassy_time::{Duration, Timer};
use embassy_nrf::gpio::{AnyPin, Output, Level};

#[embassy_executor::task]
async fn blink(pin: embassy_nrf::Peri<'static, AnyPin>) {
    let mut led = Output::new(pin, Level::Low);
    loop {
        led.set_high();
        Timer::after(Duration::from_millis(150)).await;
        led.set_low();
        Timer::after(Duration::from_millis(150)).await;
    }
}

#[embassy_executor::main]
async fn main(spawner: Spawner) {
    let p = embassy_nrf::init(Default::default());
    spawner.spawn(blink(p.P0_13.into()).unwrap()).unwrap();
    // 他のasync処理...
}
```

## 実践ポイント
- まずは手元のボード用例（examples/）を実行して感触を掴む。probe-rs とターゲットのCargo機能（feature）設定を忘れずに。  
- VS Codeで開発するなら rust-analyzer の linkedProjects をプロジェクトごとに設定。複数ターゲットを切り替える運用を整えると効率的。  
- 電力・メモリ制約が厳しい製品ではRTOSを使う前にEmbassyでの実装が有効か検討する（実行サイズ、レイテンシ、割込み設計をチェック）。  
- 対応HALがあるかを確認し、必要なら既存のHALと組み合わせて使う。ネットワークやBLEが必要なら embassy-net や trouble/nrf-softdevice の成熟度を確認。  
- ライセンスはApache/MITのデュアルライセンス。商用利用や公開時の扱いを事前に確認しておく。

Embassyは「安全性」と「低消費電力」を両立しつつ、従来のRTOS的設計を簡潔に置き換えられる選択肢。国内のIoT/組込みプロジェクトで早めに触っておく価値が高いフレームワークだ。
