---
  layout: post
  title: "A 30B Qwen Model Walks into a Raspberry Pi and Runs in Real Time - 30BのQwenモデルがRaspberry Piで“リアルタイム”動作する話"
  date: 2026-01-06T23:12:58.125Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://byteshape.com/blogs/Qwen3-30B-A3B-Instruct-2507/"
  source_title: "A 30B Qwen Model Walks Into a Raspberry Pi… and Runs in Real Time"
  source_id: 46518573
  excerpt: "Qwen3-30BをShapeLearnで量子化しRaspberry Pi 5で8TPSの実用対話を達成"
  image: "https://byteshape.com/images/logo.svg"
---

# A 30B Qwen Model Walks into a Raspberry Pi and Runs in Real Time - 30BのQwenモデルがRaspberry Piで“リアルタイム”動作する話

魅惑のエッジAI：30BモデルがRaspberry Piで対話的に動く時代が来た理由

## 要約
ByteShapeのShapeLearnで最適化したQwen3-30Bの量子化モデルが、Raspberry Pi 5（16GB）で「実用的なリアルタイム感」を出せることを示した検証。デバイスごとに最適なビット長を選ぶことで、速度（TPS）と出力品質の最良トレードオフを達成している。

## この記事を読むべき理由
- 日本でも「手元で動く大規模言語モデル（LLM）」は、プライバシーやコスト低減、オフライン利用で注目度が高い。
- Raspberry PiやミドルレンジGPUでの現実的な性能目安（8TPSで実用的な対話感など）と最適化方針が具体的に示されているため、実装・導入判断に直結する知見が得られる。

## 詳細解説
- 目的と手法  
  ByteShapeは「メモリの枠を満たすことをまず目標にし、その上でTPS（tokens per second）と品質を最適化する」方針を採る。ShapeLearnという「ビット長学習」で、層ごと（あるいはテンソルごと）に最適な重みのデータ型を選び、速度と品質の実用的なトレードオフを作る。

- Raspberry Pi 5（16GB）の結果  
  特に注目すべきは、Q3_K_S-2.70bpw（2.70 BPW）で8.03 TPS、BF16比94.18%の品質を出し「体感上リアルタイム」に到達している点。一般的な読書速度やインタラクティブ用途では、8TPS前後が実用ラインだと示している。ByteShapeは同条件でUnslothやMagicQuantより高TPS／高品質を実現している。

- CPUとメモリの振る舞い  
  CPU（RAM制約下）では、モデルがRAMに入ることが最初のボトルネック。モデルが収まれば、ビット長を下げることでほぼ予測可能にTPSが増える。ただし、ビット長選択が適切でないと品質が予期せず落ちる。

- GPU（RTX 5090 / RTX 4080）の挙動  
  GPUでは「より少ないビット＝高速」にならないケースが多い。RTX 5090では約4ビット付近にスイートスポットがあり、ここでTPSが最大化されるモデル群が存在。RTX 4080（16GB）はVRAM制約のため4-bit群が使えず、別の最適点が生じる。実測では、4-bit系カーネルが帯域効率やデコードコストで有利になることが多く、3-bitにするとかえって遅くなる例もある。

- 背後の理由（ハードウェア／ソフト設計）  
  GPUはwarpやアラインメント（例：32バイト境界）、固定ブロック（llama.cppは256要素ブロック）などの実装制約で最適化パスが限定される。したがって「ビット削減＝帯域削減＝高速化」が成立しない。ShapeLearnはこうした振る舞いを踏まえ、各テンソルに最も有利なビット長を割り当てる点が差別化要因。

## 実践ポイント
- デバイスをまず予算（メモリ）で考える：メモリに収まることが前提。そこからTPSと品質を最適化する。  
- 手元で「対話的」な速度を狙うなら目安は約8 TPS（Raspberry Piクラス）。この値を基準に量子化レベルを選ぶ。  
- GPUでは4-bit付近の「スイートスポット」を試す：VRAMが十分なら4bpw系をデフォルトで評価。16GB級なら別のBPWで最適点を探る。  
- 実機計測が必須：llama.cpp等の実装やGPU世代で最適BPWは変わるため、TPSとベンチマーク品質（MMLUやGSM8Kなどの合成スコア）で比較すること。  
- もし精度重視ならByteShape系の高BPWモデル、速度重視ならShapeLearnで低BPWに寄せつつ品質許容範囲を確かめる。  
- 日本の現場での応用例：社内データを外に出せないチャットボット、オフラインで動く実証実験、エッジデバイスを活用したコスト効率の良い導入などに直結する。

短くまとめると、重要なのは「どれだけ小さくするか」ではなく「与えられたメモリ予算の中でTPSと品質をどう最適化するか」。Raspberry Piで30Bモデルが“実用的に”動くという事実は、手元で使えるLLMのユースケースを大きく広げます。
