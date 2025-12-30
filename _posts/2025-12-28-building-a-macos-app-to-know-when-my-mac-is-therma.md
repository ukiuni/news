---
layout: "post"
title: "Building a macOS app to know when my Mac is thermal throttling - Macがサーマルスロットリングを起こしているか知るためのmacOSアプリの構築"
date: "2025-12-28 14:58:03.259000+00:00"
categories:
- tech
- world-news
tags:
- tech-news
- japan
source_url: "https://stanislas.blog/2025/12/macos-thermal-throttling-app/"
source_title: "Building a macOS app to know when my Mac is thermal throttling · Stan's blog"
source_id: "46410402"
excerpt: "ファンレスMacでRoot不要に熱状態を監視しサーマルスロットリングを即検知する方法"
---
# Building a macOS app to know when my Mac is thermal throttling - Macがサーマルスロットリングを起こしているか知るためのmacOSアプリの構築

## 要約
M2系などファンレスMacでは熱による性能低下（サーマルスロットリング）が体感でしか分からないことが多い。powermetricsは詳細を出すがrootが必要。一方で thermald が Darwin 通知に書き出す情報を監視すれば、root不要でより細かい熱状態が取れる — これを利用したのが MacThrottle の肝だ。

## この記事を読むべき理由
- 日本では外部ディスプレイや高負荷作業（動画編集、コンパイル、機械学習等）でファンレスMacが熱を持つ場面が増えている。  
- 開発者やパワーユーザーは「性能は高いのに突然遅くなる」問題を観察・自動検知して対策できるようになる。

## 詳細解説
- 何が問題か：Foundation の ProcessInfo.thermalState は手軽に使えるが状態が粗く、実機での観測では「fair」に多くの熱状況が詰め込まれ、実際のスロットリング開始を判別できないことがある。  
- powermetrics：より細かい熱圧（thermal pressure）レベルを出力するが、sudo が必要で常時実行には向かない。出力例では nominal / moderate / heavy といった段階が得られる。heavy が実際のスロットリングと相関することが多い。  
- thermald と Darwin 通知：powermetrics が参照している thermald は現在の熱圧を Darwin の通知システム（notifyd）に書き出す。キーは com.apple.system.thermalpressurelevel。notify 系で購読すれば root 権限不要でリアルタイムに近い検知が可能。  
- 実装のポイント：notify_register_check / notify_get_state を使って通知トークンを取得し、定期チェックかイベントベースで状態を読み取る。返る数値を powermetrics のレベルにマップし、しきい値で macOS 通知やメニューバー表示、ログ出力を行う。

サンプル（Swift／簡易観測ループ）：

```swift
swift
import Foundation

@_silgen_name("notify_register_check") private func notify_register_check(_ name: UnsafePointer<CChar>, _ token: UnsafeMutablePointer<Int32>) -> UInt32
@_silgen_name("notify_get_state") private func notify_get_state(_ token: Int32, _ state: UnsafeMutablePointer<UInt64>) -> UInt32
@_silgen_name("notify_cancel") private func notify_cancel(_ token: Int32) -> UInt32

let key = "com.apple.system.thermalpressurelevel"
var token: Int32 = 0
let rc = key.withCString { ptr in notify_register_check(ptr, &token) }
guard rc == 0 else { fatalError("notify_register_check failed: \(rc)") }

let queue = DispatchQueue(label: "thermal.poll")
queue.async {
    var last: UInt64 = UInt64.max
    while true {
        var state: UInt64 = 0
        if notify_get_state(token, &state) == 0 {
            if state != last {
                last = state
                // 値の意味は観測で確認する（例: 0=nominal,1=moderate,2=heavy）
                print("thermalpressurelevel = \(state)")
                // ここで通知やUI更新を行う
            }
        }
        Thread.sleep(forTimeInterval: 1.0)
    }
}

// 終了時に
// notify_cancel(token)
```

注意点：
- com.apple.system.thermalpressurelevel の数値がシステムや世代で変わる可能性があるため、自分の機種で観測してマッピングを作ること。
- powermetrics の結果と突き合わせて挙動を確認する（例えば heavy 相当の値を検出したら「スロットリング」扱い）。

## 実践ポイント
- まずは自身のMacで notifyutil -g com.apple.system.thermalpressurelevel を使って値の傾向を掴む。sudo は不要。
- 簡易アプリを作るなら上の Swift コードで polling → 値が大きく変わったら macOS通知を投げる。外部ディスプレイ接続や長時間ビルド時にログを取って閾値を調整する。  
- 高精度に監視したければ powermetrics を sudo で定期実行して比較ログを取り、notify の値と powermetrics のレベルを対応づける。  
- UX案：メニューバーに現在の熱レベルを小さなグラフで表示し、heavy 検出時に通知＋自動で高負荷タスクを一時停止するスクリプトを呼ぶと実用的。

