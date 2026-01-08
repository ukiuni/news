---
  layout: post
  title: "Quick And Easy GPU Random Numbers In D3D11 - D3D11で手早くGPU乱数を作る方法"
  date: 2026-01-04T15:15:28.354Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://www.reedbeta.com/blog/quick-and-easy-gpu-random-numbers-in-d3d11/"
  source_title: "Quick And Easy GPU Random Numbers In D3D11 – Nathan Reed’s coding blog"
  source_id: 1041561143
  excerpt: "D3D11でWangハッシュ＋軽量PRNGにより高速並列乱数を低コストで生成する実践ガイド"
---

# Quick And Easy GPU Random Numbers In D3D11 - D3D11で手早くGPU乱数を作る方法
GPU上で「見た目ランダム」にする最短ルート — 低コストで並列生成するための実践テクニック

## 要約
D3D11（HLSL）で高速に乱数を作る現実的な方法を解説。軽量PRNG（LCG / Xorshift）をスレッドごとに走らせ、初期シードをWangハッシュで混ぜると「横に広げた」並列生成でも目に見えるアーティファクトを防げる、という主張と実例が得られる。

## この記事を読むべき理由
ゲームやレンダリングで数十〜数百億の乱数をリアルタイムに必要とする場合、暗号級のPRNGは過剰。D3D11のシェーダ上で安価に、かつ見た目に十分な乱数を得る実践的な手法は、日本のゲーム／グラフィックス開発現場でも即戦力になる。

## 詳細解説
- 問題設定  
  GPUは大量のスレッドで「横に（wide）」並列に乱数を必要とする。多くの古典PRNGは「深く（deep）」同一インスタンスから連続して値を取る用途向けに設計されているため、スレッドごとに異なるシードで並列に走らせるとスレッド間に相関が出て、画素として可視化すると縞模様やタイル状のアーティファクトが生じる。

- 軽量PRNG候補  
  ・LCG（線形合同法）: 更新は1命令（乗算+加算）で非常に高速。ただし品質は低めで長周期・高次元の統計性は期待できない。  
  ・Xorshift: ビット操作中心で高速、LCGより統計性能は良好で「深く」した場合には十分使える。ただし「横に」展開した場合はそのままだと相関の問題が出ることがある。

- シードの乱れを解消するハッシュ  
  スレッドID等をそのままシードにすると隣接スレッドのシードが近く、PRNGの初期列が相関しやすい。そこで、Wangハッシュのような軽量な32→32ビットハッシュでシードを事前に混ぜると、スレッド間の相関が大幅に低減される。Wangハッシュは短くてシェーダ向けに速い（HLSLで数命令）。

- 実運用の勧め  
  シードをWangハッシュで混ぜた上で、性能重視ならLCG、品質を少し重視するならXorshiftを各スレッドで数回回して使うのがバランス良し。注：記事の更新（2021）ではPCGが総合的に優れると指摘されているので、新規導入ではPCGの採用も検討すること。

- 浮動小数点生成  
  32ビット符号なし整数を[0,1)に変換するには $2^{32}$ で割るのが定石：
  $$
  f = \frac{\text{uint\_rand}}{2^{32}}
  $$

- 可視化チェック  
  目視はGPUランダムの初期調査に有効。1ビットを画素にしてビットマップ化するとパターンが直感的に判るため、初期検証に推奨。

コード例（HLSL）
```hlsl
// hlsl
uint rng_state;
uint rand_lcg() {
    // Numerical Recipes の定数
    rng_state = 1664525u * rng_state + 1013904223u;
    return rng_state;
}
uint rand_xorshift() {
    rng_state ^= (rng_state << 13);
    rng_state ^= (rng_state >> 17);
    rng_state ^= (rng_state << 5);
    return rng_state;
}
// Wang hash for seeding
uint wang_hash(uint seed) {
    seed = (seed ^ 61u) ^ (seed >> 16);
    seed *= 9u;
    seed = seed ^ (seed >> 4);
    seed *= 0x27d4eb2du;
    seed = seed ^ (seed >> 15);
    return seed;
}
[numthreads(256,1,1)]
void cs_main(uint3 threadId : SV_DispatchThreadID) {
    rng_state = wang_hash(threadId.x);
    uint r = rand_xorshift();
    float f = (float)rand_xorshift() * (1.0 / 4294967296.0); // ≈ rand / 2^32
    // ...
}
```

## 実践ポイント
- まずは目視検査：1ビット/画素のテクスチャに各スレッドの出力を書き出して、パターンを確認する。  
- スレッドごとのシードは必ずハッシュで混ぜる（Wangやその他の軽量混合関数）。隣接スレッドのシードが近いとアーティファクトが出る。  
- 性能/品質のトレードオフを明確に：高速が最優先ならLCG、少し品質が欲しいならXorshiftかPCG。最新の知見ではPCGが優れる。  
- モバイルや古いGLSL環境では整数演算のサポート状況が異なるため、ターゲットGPUの算術サポートを確認する。  
- 必要ならハッシュだけで直接PRNG代わりに繰り返し使う（ハッシュを何度も適用する）ことも可能だが、命令数が増えるためコストと相談。

最後に一言：GPU上の乱数は「深さ（deep）」向けPRNGと「横幅（wide）」向けハッシュを組み合わせることで現実的・実用的に解決できる。ゲームやレンダリングの現場では、この素朴で高速な組み合わせが最初の選択肢として非常に有効だ。
