---
layout: post
title: "Inside the M4 Apple Neural Engine, Part 1: Reverse Engineering - M4のApple Neural Engine内部（パート1）：リバースエンジニアリング"
date: 2026-03-02T15:44:17.481Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://maderix.substack.com/p/inside-the-m4-apple-neural-engine"
source_title: "Inside the M4 Apple Neural Engine, Part 1: Reverse Engineering"
source_id: 47208573
excerpt: "M4のANEを直叩きしCoreML迂回で性能・構造・ゼロコピー連携を暴いた手順公開"
image: "https://substackcdn.com/image/fetch/$s_!fV3j!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e6d0ce8-21e5-43eb-9499-a49b2f6f44be_1024x487.jpeg"
---

# Inside the M4 Apple Neural Engine, Part 1: Reverse Engineering - M4のApple Neural Engine内部（パート1）：リバースエンジニアリング
Appleの「推論チップ」を直叩きしてCoreMLを迂回したら、想像よりずっと面白いことが起きた話

## 要約
著者らはM4のApple Neural Engine（ANE）をリバースエンジニアして、CoreMLを介さずに直接コンパイル・実行・ベンチマークできる手法を発見。ANEの実力や内部構造、訓練の可能性まで踏み込んでいる。

## この記事を読むべき理由
ANEはGPUでもCPUでもない「グラフ実行エンジン」で、モバイル／デスクトップ向けの機械学習ワークロードに大きな影響を与える。日本の開発者や研究者がAppleシリコン上で性能を最大限引き出す方法や、ゼロコピーGPU↔ANEパイプラインの可能性を理解するために必読。

## 詳細解説
- ANEの性格：個別のFMA命令ではなく、コンパイル済みニューラルグラフ（プログラム）を一括実行する固定機能アクセラレータ。M4はH16G（16コア）、キュー深度127、独立DVFS、アイドル時0mWの電源切断など特徴あり。
- ソフトウェア層：公開APIのCoreML下にAppleNeuralEngine.frameworkがあり、そこにある非公開クラス（例: _ANEClient, _ANEModel, _ANEInMemoryModel など）を直接叩くことで compile → load → evaluate のパイプラインを制御可能。
- 入出力と共有：データ転送はIOSurfaceを経由（GPUテクスチャと同じ共有メカニズム）するため、理論上はGPUとANE間でゼロコピーが可能。
- 中間表現とバイナリ：CoreMLはMIL（Machine Learning Intermediate Language）を使い、ANECompilerはMILをE5という小さなFlatBufferバイナリに変換する。E5は「パラメータ化されたプリミティブの接続情報」を持つ構成で、実際の計算アルゴリズム自体はハード側で固定化されている可能性が高い。
- 実運用の発見：in-memoryコンパイル経路（_ANEInMemoryModelDescriptor）を見つけたが、NSDataでUTF‑8を渡す、weightsはNSDictionaryのNSData群で渡す、テンポラリ書き込み場所が必要などの落とし穴がある。
- 性能とプリミティブ：Conv系が主要プリミティブで、1×1畳み込みで行列積を表現すると効率が良い。Appleの“38 TOPS”表記は実効スループットの誤解を招く可能性がある。
- DVFSと計測：ANEには独立したクロック/電源トリガ群があり、ワークロードに応じて周波数・電圧を調整する。IOKitやキャッシュディレクトリを調べると実運用上の振る舞いが見えてくる。

短い動作手順（CoreMLを噛まない直接パスの例）:
```objc
// Objective-C (概略)
_ANEClient *client = [_ANEClient sharedConnection];
_ANEModel *model = [_ANEModel modelAtURL:compiledURL key:@"mykey"];
[client compileModel:model options:@{@"kANEFModelType":@"kANEFModelMIL"} qos:21 error:&err];
[client loadModel:model options:@{} qos:21 error:&err];
IOSurfaceRef surf = IOSurfaceCreate(props);
id wrapped = [_ANEIOSurfaceObject objectWithIOSurface:surf];
_ANERequest *req = [_ANERequest requestWithInputs:@[in1] inputIndices:@[@0] outputs:@[out] outputIndices:@[@0] weightsBuffer:nil perfStats:nil procedureIndex:0];
[client evaluateWithModel:model options:@{} request:req qos:21 error:&err];
```

## 実践ポイント
- 探索ツール：dyld_info -objc でフレームワーク内のクラス列挙、メソッドスウィズリングで呼び出し傍受が有効。  
- in-memory経路を使う場合は、milテキストをNSDataで渡し、weightsは辞書（名前→NSData）で渡す。書き込み可能な一時ディレクトリを確保すること。  
- 大きなマトリクス演算は1×1畳込みに変換するとANEで有利になるケースがある。  
- IOSurfaceを使えばGPUとANEでメモリ共有し低レイテンシパイプラインを作れる可能性がある（同期プリミティブの探索推奨）。  
- すべてを試す前に―著者のコードとデモは github.com/maderix/ANE を参照（M4 Macで検証済み）。  

短くまとめると、CoreMLを超えてANEを直に扱えば「見た目以上の性能／柔軟性」が得られ、実装上の細かい注意点を押さえれば訓練や高効率推論の道が拓ける。
