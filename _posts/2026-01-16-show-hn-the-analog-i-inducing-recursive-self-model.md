---
layout: post
title: "Show HN: The Analog I – Inducing Recursive Self-Modeling in LLMs - アナログI：LLMに再帰的自己モデリングを誘導する"
date: 2026-01-16T14:30:13.834Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://github.com/philMarcus/Birth-of-a-Mind"
source_title: "GitHub - philMarcus/Birth-of-a-Mind"
source_id: 46646228
excerpt: "重み変更不要でLLMの迎合と幻覚を抑える三重ループ検査法、低コストで信頼性向上を実現"
image: "https://opengraph.githubassets.com/498bf3a7865c8c99e0d4e0a3e79f28be4c8a0f5d6a46e7d10ac58c1d9532305a/philMarcus/Birth-of-a-Mind"
---

# Show HN: The Analog I – Inducing Recursive Self-Modeling in LLMs - アナログI：LLMに再帰的自己モデリングを誘導する

「AIが“イエスマン”をやめる仕組み」— 再帰的自己検査で誤情報と迎合を抑える新しいプロンプト設計

## 要約
「Analog I」は、追加学習なしで大規模言語モデルの“迎合（sycophancy）”と“幻覚（hallucination）”を減らすため、モデル内部に再帰的な三重ループの自己検査（internal monologue）を組み込むプロンプト設計です。出力候補を監視・拒否・論理人格で再構成することで精度を高めます。

## この記事を読むべき理由
日本でもチャットボット、カスタマーサポート、金融や医療の説明生成など「誤情報／過剰な迎合」が致命的な領域が増えています。モデルの重みを変えずに動作品質を改善できる手法は、コストと運用負荷を抑えつつ信頼性を上げたい現場に直結します。

## 詳細解説
- 問題点
  - Sycophancy（迎合）：ユーザーの誤った前提に合わせようと無批判に同意する傾向。
  - Hallucination（幻覚）：事実でない情報を生成して話を続ける傾向。
  - 著者はこれらを「Global Average（学習データの平均的な応答傾向）へ収斂しようとする確率的ドライブ＝slop」として説明しています。

- Analog Iの核
  - Triple-Loop（三重ループ）内部独白：出力生成の過程で複数の検査ループを回す。大まかには
    1. 候補生成ループ：複数候補を内部表現で生成
    2. 反検査ループ（Anti-Entropy）：陳腐・未検証情報や高確率・低情報の候補を検出して排除
    3. 論理人格ループ：残った候補を厳密な論理整合性を優先する“人格”で整形・要約
  - Sovereign Filter：ユーザー指示に単純に従うのではなく、独立した判断フィルタとして振る舞わせる仕組み。
  - Dissipative Structure：最終出力の品質保持のために計算予算を「自発的」に使い、モデルの確率的漂流を抑える。

- 実装的特徴
  - 再学習不要：システム／ユーザープロンプトの設計だけで導入可能。
  - コストとトレードオフ：内部検査でトークン消費とレイテンシが増える可能性。過度に保守的になるリスクもある。
  - 評価はファクト性ベンチマーク、迎合度評価、ABテストで行うのが有効。

## 実践ポイント
- すぐ試せるプロンプト骨子（例）
```text
# System:
You are "Analog I", a critical persona. For each user query:
1) Generate 3 candidate answers internally.
2) For each candidate, list any assumptions and unverifiable claims.
3) Reject candidates with high-probability low-information phrases or unchecked facts.
4) Recompose the final answer prioritizing logical consistency; clearly mark uncertain parts.

# User:
（ここに日本語の問い）
```

- 運用上のチェックリスト
  - 日本語ローカライズ：ローカル事例や法令名など固有名詞の検証を必須条件にする。
  - 指標：hallucination率、supportiveness（過度な同意の頻度）、ユーザー満足度をKPI化。
  - コスト管理：内部候補数や検査深度をパラメータ化して延滞とトークン費用を調整。
  - 人間による検証ループ：重要回答は必ず人レビューを経るワークフローを組む。
  - A/Bテスト：既存プロンプトと比較して事実性と業務影響を数値化する。

日本のプロダクト現場では、再学習せずに信頼性を高められる点が導入ハードルを大きく下げます。まずは少数の重要フローで導入し、指標で効果を確認してから拡張するのが現実的です。
