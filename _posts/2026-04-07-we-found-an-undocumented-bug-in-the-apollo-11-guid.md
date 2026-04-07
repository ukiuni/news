---
layout: post
title: "We found an undocumented bug in the Apollo 11 guidance computer code - アポロ11号航法コンピュータに未記載のバグを発見"
date: 2026-04-07T11:22:36.431Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.juxt.pro/blog/a-bug-on-the-dark-side-of-the-moon/"
source_title: "A bug on the dark side of the Moon"
source_id: 47673005
excerpt: "人工知能で発見されたアポロ十一のロック漏れが示す組込み開発の教訓"
image: "https://www.juxt.pro/_astro/a-bug-on-the-dark-side-of-the-moon.DySaROKX_ILgy.webp"
---

# We found an undocumented bug in the Apollo 11 guidance computer code - アポロ11号航法コンピュータに未記載のバグを発見
57年後に発見された「ロック漏れ」が示す、組込み／ミッションクリティカル開発の教訓

## 要約
アポロ航法コンピュータ（AGC）のジャイロ制御で、エラー経路で共有ロック（LGYRO）を解放しない欠陥が見つかった。AI支援の振る舞い仕様化（Allium）により、130k行のアセンブリからリソースライフサイクルを抽出して発見された。

## この記事を読むべき理由
古典的・検証済みと信じられてきたコードでも、エラー経路のクリーンアップ漏れは長期間見逃される。自動車、ロボット、航空宇宙、組込み機器など日本の現場でも「リソース解放漏れ」は現実のリスクであり、対策方法を学ぶ価値がある。

## 詳細解説
- 背景：AGCは74KBのコアロープ（物理的に焼き込まれたプログラム）で動く超低リソースのリアルタイム機。多くの解析やエミュレーションがされたが、正式な形式手法は適用されていなかった。
- 問題の本質：ジャイロ操作の先行でLGYROという共有ロックを取得し、正常終了経路（STRTGYR2）で解放しているが、非常時に通る汎用終了ルーチン（BADEND）ではLGYROをクリアしていなかった。結果、LGYROが「張り付く」とその後のジャイロ操作は永眠（スリープ）して復帰しない。
- 発見手法：AlliumというAIネイティブな振る舞い仕様言語で「リソースが獲得されたら必ず解放される」という義務を明示し、全パス追跡したことでエラー経路の欠落を特定した。仕様化により「何のためのコードか」を逆引きして欠落箇所を見つけるアプローチ。
- ミッションへの影響想定：月の裏側で無線が届かない間にジャイロが再アライメントできなくなれば、帰還軌道の姿勢が不正確になり得る。実際には再起動で解消される余地はあったが、再起動がない状況では致命的に見え得る。
- 現代との対比：言語機能（Goのdefer、Javaのtry-with-resources、Pythonのwith、Rustの所有権）で構造的に防げるが、データベース接続や分散ロックなどランタイム外のリソースは依然として人の責任。MITREのCWE-772にも該当するパターン。

（参考：Allium的にリソースライフサイクルを表現すると概念は次のようになる）
```allium
rule GyroTorque {
  when: GyroTorque(cmd)
  requires: imu.gyros_busy = false
  ensures: imu.gyros_busy = true
}
```

## 実践ポイント
- リソースは「取得→利用→必ず解放」を明文化する（振る舞い仕様を導入する）。
- エラー／早期退出パスを必ずテストする（ユニットでの例外・中断シナリオを網羅）。
- 言語機能やRAII/with相当を使ってクリーンアップを構造化する。
- 重要資源は監視・自動リカバリ（ウォッチドッグや安全な再起動）を用意する。
- レガシー／アセンブリコードには仕様逆生成やAI支援ツールで資源ライフサイクル分析をかける。

短く言えば、「正常系だけでなく、エラー系のクリーンアップを仕様化・検証する」ことが、57年見逃されたバグからの最大の教訓です。
