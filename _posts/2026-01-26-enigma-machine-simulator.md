---
layout: post
title: "Enigma Machine Simulator - エニグマ機シミュレータ"
date: 2026-01-26T02:29:29.818Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://andrewthecoder.com/blog/javascript-enigma-machine"
source_title: "Simulating the Enigma Machine"
source_id: 418685324
excerpt: "JavaScriptで回るエニグマを実装し、ロータ移動やダブルステップの仕組みを学べる解説。"
image: "https://andrewthecoder.com/assets/blog/enigma.webp"
---

# Enigma Machine Simulator - エニグマ機シミュレータ
魅せる暗号機の再現：JavaScriptで「回る」エニグマを手元で動かして学ぶ

## 要約
歴史的な暗号機エニグマをJavaScriptで再現し、ロータの置換と踏み動作（ステッピング）による多相式暗号の仕組みをコードで学べる内容です。

## この記事を読むべき理由
エニグマは「置換」の連鎖とロータの動きで成立するため、暗号やアルゴリズムの基本概念（写像・逆写像・状態遷移）を実践的に理解できます。日本の学生・エンジニアが暗号史と実装スキルを同時に身につける良い教材です。

## 詳細解説
- 基本概念：エニグマは26文字の集合に対する置換（permutation）の合成で表せます。各部品が1対1の写像を行い、1文字の暗号化はそれらの合成です。
- 主要構成要素：
  - プラグボード（P）：最大13組の文字を入れ替える2-cycleの集合。$P=P^{-1}$（自己逆）です。
  - ロータ（$R_i$）：固定の文字置換を行い、回転により写像が変化します。
  - 反射器（U）：13組の転置で自己逆。反射のために文字が自身に写らない設計になっているのが暗号学的な欠陥でもあります。
- 暗号化の道筋は次の式で表されます：
$$E(L)=P\cdot R_1\cdot R_2\cdot R_3\cdot U\cdot R_3^{-1}\cdot R_2^{-1}\cdot R_1^{-1}\cdot P(L)$$
- ステッピング（ロータの進み）：
  - 右端ロータが毎打鍵で1ステップ進む。特定位置のノッチで隣のロータを進めるため、オドメータ的に状態が変化します。
  - 「ダブルステップ」現象に注意。中央ロータが二回続けて進むタイミングがあり、周期性と複雑さを増します。
- 組み合わせ数（鍵空間）は非常に大きく、例えば典型的な軍用エニグマは
$$N=\binom{5}{3}\times 3!\times 26^3\times\frac{26!}{2^{10}\cdot10!\cdot6!}\approx1.58\times10^{20}$$
 となります。

- JavaScriptでの再現方針（要点）：
  - 各部品を文字→文字のマップで表す（配列やオブジェクト）。
  - ロータは位置に応じて写像を「シフト」して扱う（forward/backwardを実装）。
  - 暗号化前にロータ位置を更新するロジック（advanceRotors）が最も難しい。特にダブルステップを正確に再現すること。

簡潔な実装例（抜粋）：

```javascript
// javascript
const rotors = {
  I:  { wiring: "EKMFLGDQVZNTOWYHXUSPAIBRCJ", turnover: "Q" },
  II: { wiring: "AJDKSIRUXBLHWTMCQGZNPYFVOE", turnover: "E" }
};
const reflectorB = { wiring: "YRUHQSLDPXNGOKMIEBFZCWVJAT" };

function encrypt(letter, rotor1, rotor2, rotor3, plugboard, reflector) {
  // rotor positions must be advanced before calling
  let c = plugboard.process(letter);
  c = rotor3.forward(c); c = rotor2.forward(c); c = rotor1.forward(c);
  c = reflector.process(c);
  c = rotor1.backward(c); c = rotor2.backward(c); c = rotor3.backward(c);
  return plugboard.process(c);
}
```

## 実践ポイント
- GitHubの実装（元記事のリポジトリ）をクローンしてブラウザ/Nodeで動かし、ロータ位置やプラグ配線をいじって挙動を観察する。
- ロータの写像は配列で実装し、forward/backwardをユニットテストで検証する（VS Codeのテスト機能が便利）。
- advanceRotors()を実装する際はダブルステップ条件を明示的にテストすること。
- 教材として、暗号史や組合せ数学（上の$N$の式）を合わせて学ぶと理解が深まる。
