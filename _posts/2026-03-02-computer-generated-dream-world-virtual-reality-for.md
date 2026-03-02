---
layout: post
title: "Computer-generated dream world: Virtual reality for a 286 processor - コンピュータが生む夢の世界：286プロセッサ向けの仮想現実"
date: 2026-03-02T04:47:29.903Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://deadlime.hu/en/2026/02/22/computer-generated-dream-world/"
source_title: "Computer-generated dream world &middot; deadlime"
source_id: 47213866
excerpt: "286実CPUをPico＋MCP23S17で擬似メモリ化し実際にブート＆命令実行させる挑戦"
image: "https://deadlime.hu/uploads/2026/286.jpg"
---

# Computer-generated dream world: Virtual reality for a 286 processor - コンピュータが生む夢の世界：286プロセッサ向けの仮想現実
286でよみがえるレトロCPUの“VR化” — Raspberry Pi/PicoとIOエクスパンダで286を擬似メモリ＆周辺機器に繋ぎ、実際に命令を実行させる挑戦

## 要約
古いIntel 80286（286）CPUを実物のプロセッサとして使い、周辺・メモリをRaspberry Pi系（Pico）＋MCP23S17 IOエクスパンダでソフト的にエミュレートし、実際にブート→命令実行→メモリ演算（加算）まで動かしたプロジェクトの解説。

## この記事を読むべき理由
ハード寄りのソフト／組み込みエンジニア、レトロPCファン、教育用途のハードウェア実験として、低レイヤでのバス制御・SPIによるIO拡張、クロック／リセット同期、メモリマップの扱いを実機で学べる実践例だから。

## 詳細解説
- 目標：286を「脳」とし、残り（メモリ、割り込み、各種信号）をソフトで定義してCPUを動かす。実機CPUに恒久的な改造は不要で、外部から信号を供給して命令フェッチ〜実行を制御する。
- ハード構成：PLCC-68ソケットに挿した80C286-12（手でクロックを刻める型）を、MCP23S17（SPI接続の16bit IOエクスパンダ）×4で約57ピン分をカバー。Raspberry Pi Pico（MicroPython）をSPIマスタにして制御する。
- MCP23S17のクセ：デフォルトアドレス000に対してIOCONのHAENを設定→さらに実際に割り当てたハードアドレスにも同じIOCONを書き込む必要があった（2回設定するトリック）。これを忘れると別チップに信号が混在して変な挙動になる。
- ピン分配：各MCP23S17のGPIOA/Bをアドレス上位/下位、データバス上位/下位、制御フラグ群（CLK, RESET, COD/INTA, M/IO, S0,S1, BHE, HLDA 等）に割り当て、1バイト＝8ビットとして扱う。
- リセットとクロック：RESETは少なくとも16クロック分アサートし、クロック立ち下がりや立ち上がりと同期させる。クロックは遅く（ms単位）して問題ないが、フェーズやタイミングを守ることが重要。
- フラグ監視とバスサイクル判定：COD/INTA, M/IO, S0, S1の組み合わせでCPUの「バスサイクル種別」を判定（例：メモリ命令読み出し、メモリデータ読み/書き、I/O等）。これに応じて外部がデータを供給したり受け取ったりする。
- データ幅制御（BHE/A0）：BHEとA0の組み合わせでワード転送／上位バイト／下位バイト転送を判定し、データバスのどちらの半分を操作するかを決める必要がある。
- ソフト側：MicroPythonでMCP23S17を制御するクラスを書き、各チップのIODIRを設定して読み書きを切替。メモリはPythonの辞書で実装して任意アドレスにバイナリをロード（nasmで生成したバイナリを16進配列に変換して読み込む）。例えばリセットルーチン（org 0xFFF0）→ジャンプ→加算ルーチン（メモリ上の2つのワードを読み加算して書き戻す）を動かす例を示す。
- 実運用上の工夫：配線ミスやアドレス混線のデバッグにはLEDや読み書きのログ、チップ差し替えが有効。IOエクスパンダのハードアドレス設定忘れが最大の落とし穴。

簡潔なMicroPython制御の例（IOCONを2回書く初期化）：

```python
# python
class MCP23S17:
    IOCON = 0x0B
    def __init__(self, addr, spi, cs): ...
    def init(self):
        # HAEN をまずデフォルトアドレス(0)で有効化、次に実デバイスアドレスでも設定
        self.__writeRegister(0b01000000, self.IOCON, 0b00001000)
        self.__writeRegister(self.__address, self.IOCON, 0b00001000)
```

## 実践ポイント
- 必要部品：80C286-12（PLCC-68）、PLCC→ピンアダプタ、MCP23S17×4、Raspberry Pi Pico（またはPi Zero）、ジャンパーワイヤ多数、ロジックレベル（5V↔3.3V）に注意。  
- 最初のチェックリスト：ピンマッピング表を作る→MCP23S17のハードアドレス設定（IOCONを書き直す）→IODIRで読み/書きを正しく設定→RESETを規定クロックで実施→フラグを監視してバスサイクル到来を確認。  
- ソフトTips：nasmでバイナリ生成→小スクリプトでPython配列化してMemoryへロード。メモリは辞書実装で十分。BHE/A0の扱いを忘れずに。  
- 日本での活かしどころ：電子工作／組み込み教育、レトロPCイベント、ハードウェア制御入門のワークショップ教材として最適。少人数のコミュニティプロジェクトや大学の実験課題にも向く。

以上を踏まえれば、単なる「懐古趣味」を超え、実機CPUのバスプロトコルを手で触って理解できる貴重な実践教材になります。興味があれば部品リストや配線図、簡易デバッグ手順も提供できます。
