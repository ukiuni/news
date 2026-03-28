---
layout: post
title: "Building a guitar trainer with embedded Rust - ギター練習機をembedded Rustで作る"
date: 2026-03-28T11:54:29.607Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.orhun.dev/introducing-tuitar/"
source_title: "Building a guitar trainer with embedded Rust - Orhun&#x27;s Blog"
source_id: 710103109
excerpt: "ESP32とembedded Rustで携帯ギター練習機を実装、メモリ制約やFFT回避法まで解説"
image: "https://blog.orhun.dev/crow.png"
---

# Building a guitar trainer with embedded Rust - ギター練習機をembedded Rustで作る
ESP32とRustで作る“持ち歩けるギター先生” — Tuitarが示す小さなハード×ソフトの学び方

## 要約
作者はPC上のターミナルアプリから始め、端末UIをESP32上で動かすMousefood＋Ratatuiを使って小型ギター練習機「Tuitar」を作った。限られたメモリや電源・回路の制約を工夫で乗り越え、チューナー／フレットボード表示／曲練習機能を実装している。

## この記事を読むべき理由
日本のものづくりコミュニティや組込みRustに関心のあるエンジニア／音楽好きにとって、実際のハード／ツールチェーン／資材選定やメモリ制約の対処法が具体的に学べる。ESP32や小型SPIディスプレイを使ったDIY楽器周辺機器は国内でも応用しやすい題材だ。

## 詳細解説
- 開発の流れ：PCでまずチューナーMVP（cpal→rustfft→pitchy→ratatui）を実装し、端末UIのロジックをそのままembeddedへ持っていく戦略。
- Mousefood/Ratatui：端末セルをembedded-graphicsの描画命令に翻訳する仕組みで、TUIを小型SPIディスプレイで表示可能にする。
- ツールチェーンの選択：ESP-IDF-HAL（std、周辺機器充実だが重い）とESP-HAL（no_stdで軽量）のトレードオフ。プロトタイプではESP-IDFを採用したが、依存やビルドの地雷（古いsonameの対処など）に遭遇した。
- 音声入力とFFT：MAX4466マイク→ADCでサンプルを取る際、固定サンプリング周波数が得られない問題を、512サンプルをできるだけ速く集めて経過時間から実測サンプルレートを算出する方法で回避。メモリ節約のためrustfft→microfftへ切替。
- フレットボード表示：RatatuiでUnicodeを用いたフレット表現を作成し、リアルタイムに検出ノートをハイライト。
- ギター直接入力：電気ギターはそのままADCでは信号が弱いので、LM358などの低電力オペアンプで増幅。電源は9Vを昇圧/降圧してESP32の3.3Vへ、AMS1117は熱問題で効率の良いMP1584（バックコンバータ）を採用する選択を検討。
- 回路・基板：ブレッドボードでのノイズや接触不良を避けるためPCB化（JLCで発注）して安定化。
- 曲データ処理：MIDI/GuitarProは実行時にパースするとRAM不足なので、ビルド時にパースして静的コード（build.rsでnotes配列を生成）としてファームに埋め込む戦術を採用。
- デバッグ地雷：特定のCargoターゲットディレクトリでしか正しく動かないクラッシュや起動ループ（LoadProhibited等）のような異常が発生し、環境依存のビルドキャッシュが原因になることがある。

簡潔なサンプリングループ（要旨）：
```rust
// Rust
let mut samples = Vec::<i16>::with_capacity(512);
loop {
    let t0 = Instant::now();
    while samples.len() < 512 {
        let s = mic_adc_channel.read().unwrap_or(0);
        samples.push(s);
    }
    transform.process(&samples);
    let elapsed = t0.elapsed();
    let sample_rate = samples.len() as f64 / elapsed.as_secs_f64();
    samples.clear();
    // UIレンダリング等
}
```

ビルド時に曲データを埋め込む（概念）：
```rust
// Rust (build.rs の生成結果の一例)
pub struct Song { pub name: &'static str, pub notes: &'static [&'static str] }
pub const DEMO: Song = Song {
    name: "Demo Song",
    notes: &["E4", "G4", "A4", /* ... */],
};
```

## 実践ポイント
- まずPC上でTUI版を作る（ロジック検証が早い）。動いたらMousefoodでembeddedに移植する。
- ESP-IDFは周辺機器が楽だが重い。小さいプロダクトはesp-hal＋no_std検討。
- メモリが厳しい場合はmicrofftなど軽量ライブラリを選ぶ／FFTサイズを小さくする。
- ADCでのサンプリングは「実測サンプルレート」を使うと機材差を吸収できる。
- エレキ直入力は必ずアンプ（オペアンプ）で適切に増幅し、電源安定化を行う（熱が出る線形レギュレータは注意）。
- MIDI等はビルド時にパースして静的データとして埋め込むとRAM問題を回避できる。
- ブレッドボードで動かない・不安定なら早めにPCB化して配線ノイズを排除する。
- ビルド環境／キャッシュ依存のクラッシュに注意。別環境で再現する・キャッシュクリアを試す。

Tuitarは「小さな画面・限られた資源であっても、ソフトと回路の工夫で実用的な学習ツールを作れる」ことを示す好例。ESP32×Rustで遊びたい人にとって具体的なヒントが満載なので、実装やPCB制作に踏み出す価値がある。
