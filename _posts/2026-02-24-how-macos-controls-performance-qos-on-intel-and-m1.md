---
layout: post
title: "How macOS controls performance: QoS on Intel and M1 processors - macOSが性能を制御する仕組み：IntelとM1プロセッサにおけるQoS"
date: 2026-02-24T20:38:23.932Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://eclecticlight.co/2022/01/07/how-macos-controls-performance-qos-on-intel-and-m1-processors/"
source_title: "How macOS controls performance: QoS on Intel and M1 processors &#8211; The Eclectic Light Company"
source_id: 397533605
excerpt: "M1のP/EコアとQoSで速度とバッテリー配分が劇的に変わる理由と対策"
image: "https://i0.wp.com/eclecticlight.co/wp-content/uploads/2022/01/qosm1pro.jpg?fit=1200%2C1099&#038;ssl=1"
---

# How macOS controls performance: QoS on Intel and M1 processors - macOSが性能を制御する仕組み：IntelとM1プロセッサにおけるQoS
M1世代で効く「優先度スイッチ」——速度かバッテリーかをOSがどう割り振るかを読み解く

## 要約
macOSはプロセスごとにQoS（Quality of Service）を割り当て、Intel機とM1系で挙動が大きく異なる。特にM1のP（Performance）／E（Efficiency）コア設計ではQoSによる高速化／省電力化の差が顕著になる。

## この記事を読むべき理由
M1搭載ラップトップのバッテリー運用や、バックグラウンド処理の振る舞いを理解すると、バッテリー寿命改善やパフォーマンス最適化に直結する判断ができるため。

## 詳細解説
- QoSの仕組み：macOSはプロセスに数値化されたQoSを持たせ（代表的な値は低い方が9、ユーザー反応重視が33）、スケジューラがそれを元に実行優先度やコア割当てを決定する。通常はプロセス起動時に設定され、アプリ側が明示しない限りユーザーから変更できない。  
- Intel機の挙動：従来の同一コア設計ではQoSの影響は限定的。実測でもQoS最高⇄最低で数十％の差に留まることが多い（例：圧縮 1.38→1.04 GB/s程度）。  
- M1系（P/Eコア）の挙動：macOSは低いQoSの処理をEコアへ集約し、高QoSをPコアへ割当てる。結果、低QoSだとPコアの性能を使えないため速度が大幅に低下する一方で消費電力は劇的に下がる（例：M1 Proで圧縮 1.73→0.20 GB/s、展開 5.55→1.26 GB/s）。  
- 意味するところ：バックグラウンド処理を低QoSでEコアに押し込むことで、ユーザー操作は常にPコアの高速性能を得られ、ノートではバッテリー延命にも有利。だが多くのアプリはQoSを積極的に公開していないため、ユーザーが制御しにくい現状がある。  
- 実環境での観察法：Activity MonitorのCPU履歴でEコアだけが動いている時間帯を確認すれば、低QoSスレッドの挙動を推測できる。

## 実践ポイント
- バッテリー優先：Time Machineやバックアップ、インデックスなど長時間のバックグラウンド処理は低QoS（Eコア）で走らせると効果的。  
- 開発者向け：アプリで明示的にQoSを設定すれば、ユーザーに「省電力モード」や「高速モード」を提供できる。Cでの例：  
```c
#include <pthread/qos.h>

int main(void) {
    // 背景にする場合
    int err = pthread_set_qos_class_self_np(QOS_CLASS_BACKGROUND, 0);
    // ユーザー反応重視にする場合
    // int err = pthread_set_qos_class_self_np(QOS_CLASS_USER_INTERACTIVE, 0);
    if (err) return 1;
    // ...処理...
    return 0;
}
```
- 確認方法：Activity Monitorでコア振る舞いを見たり、処理時間を同じファイルでQoSを変えてベンチ比較する。  
- 使えるアプリ：一部（例：Carbon Copy Clonerなど）はQoS設定を公開しているので、ノートPCでの長時間処理時は低QoSへ切替えて節電を試す。

以上を踏まえ、M1系では「QoSを意識した運用」が実用的な節電／パフォーマンス管理手段になります。
