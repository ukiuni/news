---
  layout: post
  title: "TinyTinyTPU: 2×2 systolic-array TPU-style matrix-multiply unit deployed on FPGA - TinyTinyTPU：FPGA上に展開された2×2シストリック配列のTPU風MMU"
  date: 2026-01-02T20:07:05.688Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://github.com/Alanma23/tinytinyTPU-co"
  source_title: "GitHub - Alanma23/tinytinyTPU-co"
  source_id: 46468237
  excerpt: "Basys3で動く2×2シストリックTPUを手元で動かし学べる低コスト実践ガイド"
  image: "https://opengraph.githubassets.com/628354f9bd8409185ae06c4f72d7f349f2cd62f8dc473d270c4118ccb53e3669/Alanma23/tinytinyTPU-co"
---

# TinyTinyTPU: 2×2 systolic-array TPU-style matrix-multiply unit deployed on FPGA - TinyTinyTPU：FPGA上に展開された2×2シストリック配列のTPU風MMU
わずか数千ゲートでTPUの骨格を体験する — Basys3で動く教育向け2×2 TinyTinyTPU入門

## 要約
TinyTinyTPUはSystemVerilogで書かれた教育用のTPU実装で、2×2シストリック配列＋ポストMACパイプライン（蓄積・活性化・正規化・量子化）をBasys3 FPGA上で動かせます。ホストはUART経由のPythonドライバで、MLP推論やジェスチャ認識デモ付き。

## この記事を読むべき理由
FPGAでの機械学習アクセラレータ設計を学びたい日本の学生・エンジニアにとって、実際に動く「最小限のTPU」を手元で動かしながらアーキテクチャ、データフロー、パイプライン設計、FPGAツールチェーン（Vivado／Yosys+nextpnr）まで一通り学べる稀有な教材だからです。低コストなハードで学習→プロトタイプ→拡張の流れが取りやすい点も魅力です。

## 詳細解説
- アーキテクチャ概要  
  - 2×2シストリック配列（PE×4）で行列乗算を実現。活性化は行方向に、部分和は列方向に流れます。重みは「斜めのウェーブフロント」で読み込み、シストリックのタイミングを確保します。  
  - 完全なポスト-MACパイプライン：Accumulator（列アライメント・ダブルバッファ）→Activation（ReLU/ReLU6）→Normalizer（gain/bias/shift）→Quantization（int8飽和）→出力FIFO。  
  - マルチレイヤMLP制御：レイヤ間はアクティベーションのダブルバッファでピンポン、重みはUARTで逐次ロード、計算とロードのオーバーラップをサポートします。

- 実装・ツールチェーン  
  - 言語：SystemVerilog。テストベンチはcocotb（Python）＋Verilator推奨。波形はGTKWaveで確認可能。  
  - FPGA：Digilent Basys3（Xilinx Artix‑7）での実装例が付属。Vivado向けのTCLスクリプトと、オープンソース代替のYosys + nextpnr用の手順も用意。  
  - リソース（Basys3 実測・目安）：LUT ≈ 1,000、FF ≈ 1,000、DSP48E1 = 8、BRAM ≈ 10–15、推定ゲート数 ≈ 25k — 小規模ボードで余裕を持って動きます。

- ホストとプロトコル  
  - Pythonドライバ（pyserial）でUART経由により重み・入力送信、推論開始、結果取得を行う。付属デモとして単純なinference_demoとマウス動作から学習するジェスチャ認識デモあり。  
  - シミュレーション用の豊富なテスト群（PE, MMU, FIFO, Accumulator, Activation 等）が用意され、設計変更の回帰テストに便利。

## 実践ポイント
- まず手を動かす（最速で動かす手順）  
  - リポジトリをクローンしてsimディレクトリで仮想環境を作成、requirementsを入れてテストを実行。  
  - FPGA接続後、hostディレクトリのinference_demo.pyを走らせてUARTポート（例: /dev/ttyUSB0 または COM3）を指定すれば即座に動作確認できます。

```bash
# bash
git clone <repo-url>
cd tinytinyTPU-co
cd sim
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
make test
```

```python
# python
from tpu_driver import TPUDriver
tpu = TPUDriver('/dev/ttyUSB0')
tpu.write_weights([[1,2],[3,4]])
tpu.write_activations([[5,6],[7,8]])
tpu.execute()
print(tpu.read_result())
```

- 教育・ワークショップでの使い方アイデア  
  - 「シストリック配列のデータ流れ」を可視化する実習：波形（VCD）を生成して各PE間のデータタイミングを確認させる。  
  - 量子化や正規化の影響を段階的に変えて精度変化を測る演習（FPGAで実計算→Pythonで評価）。  
  - Basys3以外のボード（Arty等）へ移植して資源や周辺回路の影響を比較する実験。

- 拡張・研究の出発点  
  - 2×2を足掛かりに配列サイズを拡大、またはポスト処理（バッチ正規化やより複雑な活性化）を追加して「TPUらしさ」を段階的に再現できます。  
  - Yosys/nextpnr のフローを使えば完全オープンスタックでの検証・自動化が可能。日本の大学やコミュニティでの勉強会題材に最適です。

短時間で「動くTPU」を手元に置き、設計の各要素（シストリックデータフロー、パイプライン、量子化、FPGAツールチェーン）を実地で学べるリポジトリです。まずはシミュレーション→デモ実行の流れで動かしてみてください。
