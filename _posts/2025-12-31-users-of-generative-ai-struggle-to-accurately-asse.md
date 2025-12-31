---
layout: post
title: "Users of generative AI struggle to accurately assess their own competence - 生成AI利用者は自分の能力を正確に評価できない"
date: 2025-12-31T06:36:52.536Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.psypost.org/users-of-generative-ai-struggle-to-accurately-assess-their-own-competence/"
source_title: "Users of generative AI struggle to accurately assess their own competence"
source_id: 475912117
excerpt: "生成AIで正答率は上がるが利用者は自己評価を過大視し誤判断を招く危険と対策"
---

# Users of generative AI struggle to accurately assess their own competence - 生成AI利用者は自分の能力を正確に評価できない
AIに頼るほど「できる気」になる？生成AIが実力認知を歪めるメカニズムと実務での対処法

## 要約
生成AI（例：ChatGPT）は論理問題の正答率を上げる一方で、利用者の自己評価を過大にし、実際の成績と自己認知が乖離することが実証された。

## この記事を読むべき理由
日本の教育現場や企業で生成AIの利用が急速に進む中、ツールが生産性を上げる一方で「過信」がもたらす誤判断や品質低下のリスクを早期に把握し、運用ルールやUI設計で対策を取る必要があるため。

## 詳細解説
- 研究デザイン：LSATの論理問題20問を題材に2件の実験を実施。第1研究は米国参加者246名でChatGPTと共に解答、第2研究は452名をAIあり／なしに分けモチベーションを高める金銭インセンティブを導入して再検証。
- 主な結果：
  - AI利用者は平均点が非利用者より高く（第1研究で約3点向上）実際の正答率は改善された。
  - ただし自己推定は著しく過大：参加者は平均で「20問中約17問正解」と推定したが、実際は約13問で約4点のギャップ。
  - Dunning–Kruger効果の「傾き」はAI利用で消失し、低得点者も高得点者も同程度に過大評価する「均一化」が観察された。
  - AI単体（モデルのみ）が最も高得点であり、人＋AIはAI単体の性能に届かないケースが多かった（人が誤った助言を受容したり、正しい助言を不採用にするため）。
  - AIリテラシーが高い参加者ほど自信は高まるが、自己評価の精度は悪化するという逆相関が確認された。
  - 金銭的インセンティブでも過大評価は解消されず、AUC（メタ認知感度）も低い：正答時と誤答時の信頼差が小さい。
- 行動観察：多くの参加者が質問をコピペしてAIの出力をそのまま受け入れる「受動的利用」。真の共同作業（反論・検証）は少数。
- 理論的説明：説明の流暢さや即時性が「理解している感覚（illusion of explanatory depth）」を生み、誤りに気づく内部シグナルを弱める可能性。
- 制約：タスクはLSAT論理問題に限定、使用したのは特定バージョンのChatGPT、第1研究は歴史的対照との比較。タスク領域やモデル更新で結果は変わる可能性あり。

## 実践ポイント
- 検証を必須化するUI：AIの回答を受け入れる前に「自分の言葉で要約」「逆尋問（反例を出す）」を必須にする。
- チェックリスト運用：AI出力に対する最小限の検証手順（ソース、論拠、反例）を標準化する。
- 「AIを批評する」ワークフロー：生成結果に対して別のAIやヒューマンレビューを導入してシステム間で突き合わせる。
- キャリブレーショントレーニング：信頼度と実際の正答率を定期的に可視化し、個人の信頼度キャリブレーションを促す。
- モデルの不確実性表示：出力に不確実性や根拠の有無を示すメタ情報を付与するよう設定または依頼する。
- 組織ポリシー：重要判断（契約書、審査、採点など）はAI単独に依存しないガバナンスを設ける。

## 引用元
- タイトル: Users of generative AI struggle to accurately assess their own competence
- URL: https://www.psypost.org/users-of-generative-ai-struggle-to-accurately-assess-their-own-competence/
