---
layout: post
title: "Celeste & TowerFall Physics - Celeste と TowerFall の物理挙動"
date: 2026-01-09T16:53:22.257Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.maddymakesgames.com/articles/celeste_and_towerfall_physics/index.html"
source_title: "Celeste & TowerFall Physics"
source_id: 1564294177
excerpt: "CelesteとTowerFallのピクセル単位物理を盗んで、滑らかな動きを再現する実践ガイド"
image: "https://maddymakesgames.com/images/preview.png"
---

# Celeste & TowerFall Physics - Celeste と TowerFall の物理挙動
ピクセル単位で「気持ちよく動く」秘密を盗む：インディー2Dプラットフォーマーのための実践ガイド

## 要約
Celeste と TowerFall の物理は「タイル／ピクセル単位の整数座標」と「残余（remainder）による少数移動の蓄積」、そして「移動する地形（Solids）がプレイヤーなど（Actors）を押す／運ぶ」仕組みで成り立っている。シンプルだがゲームフィールに直結する設計が鍵。

## この記事を読むべき理由
- インディー開発や2Dプラットフォーマー制作で「動きの良さ」は重要。日本の小規模チームや個人開発者が短時間で実装可能な実用設計だから学ぶ価値が高い。  
- Unity/C#やGameMakerなどで再現しやすく、バグになりやすい移動床や潰し（squish）の振る舞いを安定して作るヒントが得られる。

## 詳細解説
基本概念（用語）
- Solids：当たり判定のあるレベルのジオメトリ（不動または動くブロック）。  
- Actors：プレイヤー、矢、モンスターなどの「動く」オブジェクト。

主要な約束事
- 衝突形状は軸平行な長方形（AABB）。  
- 位置・幅・高さは整数値（ピクセル単位）。  
- 基本的に Actor と Solid は重ならない（Overlap を許さない）。

小数移動の扱い（remainder）
- 表示位置は整数のみなので、微小な速度は蓄積しておき、丸めてから整数ピクセル分だけ動かす。
- フローはおおむね次のとおり：
$$
x\_remainder \mathrel{+}= \Delta x \\
move = \mathrm{round}(x\_remainder) \\
x\_remainder \mathrel{-}= move
$$
- その後、1ピクセルずつ先行判定して移動を適用する（1ピクセルずつの衝突解決で滑らかなフィール）。

Actor の移動（MoveX / MoveY）
- Actor 自体は速度や重力の概念を持たず、派生クラスが速度を管理して MoveX/MoveY に渡す。  
- MoveX は余りを使い、1ピクセルずつ衝突判定を行い、壁に当たったらコールバック（onCollide）を呼ぶ。実装例（要点）：

```csharp
public void MoveX(float amount, Action onCollide) {
    xRemainder += amount;
    int move = Round(xRemainder);
    if (move != 0) {
        xRemainder -= move;
        int sign = Sign(move);
        while (move != 0) {
            if (!collideAt(solids, Position + new Vector2(sign, 0))) {
                Position.X += sign;
                move -= sign;
            } else {
                onCollide?.Invoke();
                break;
            }
        }
    }
}
```

動く Solids（移動床）の扱い
- Solids は他の Solids と押し合わない（強制的に移動する）。そのため、移動中に出会うすべての Actors を「運ぶ（carry）」か「押す（push）」か判定して解決する必要がある。  
- Actor 側に追加する API：
  - IsRiding(Solid s)：その Actor がその Solid の上に乗っているか（運ばれる候補か）を判定。  
  - Squish()：潰されたときの挙動（デフォルトは削除）。

押す vs 運ぶ（優先度）
- 「押す（push）」は、Solid の動きによって Actor と重なった場合（移動後にピクセルが重なる）に発生。押す挙動が優先される。  
- 「運ぶ（carry）」は、移動前に IsRiding が true だった Actor に対して行う。運ぶ場合は Solid の移動量を丸ごと与えるが、押す場合は重なりを解消する最小差分だけ移動させる（Actor がブロックの縁に密着するように）。

実装上の工夫
- Solid が Actor を自分の影響で移動させる際、一時的にその Solid 自身を Actor 判定から除外（collidable = false）にする。そうしないと、Actor が Solid によって動かされた際に自己参照的な衝突でスタックする。  
- 事前に IsRiding を確認して「運ぶべき」リストを作る（移動前に収集するのが重要）。移動後に押し判定を行う。

## 実践ポイント
- 整数座標設計を採る：レンダリングも物理もピクセル単位で扱うと、動きが明確でバグも追いやすい。  
- remainder パターンを使う：速度が小数でも滑らかに表現できる。  
- 1ピクセル単位で先行判定を行うことで「詰まる」挙動を回避しやすい。  
- 動く床は「運ぶ」前に乗っている Actor を先に記録し、移動中は自分を一時的に衝突判定から外す。  
- Squish（潰し）挙動はゲームデザイン次第：破壊、ダメージ、押し戻しなど用途に応じて差し替える。  
- Unity なら Rigidbody を使わず独自ループでこれを再現する方が細かいフィール調整はしやすい（特にドット物理の場合）。

短く言えば、Celeste/TowerFall の物理は「単純なルールの積み重ねで非常に直感的な結果」を出している。細部（remainder、1ピクセル移動、押す／運ぶの優先）は模倣するだけで手触りが大きく良くなるため、まずは小さな実験ステージでこのパターンを試すことを推奨する。
