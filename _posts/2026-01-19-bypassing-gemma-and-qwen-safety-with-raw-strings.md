---
layout: post
title: "Bypassing Gemma and Qwen safety with raw strings - apply_chat_template() Is the Safety Switch"
date: 2026-01-19T18:54:40.103Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://teendifferent.substack.com/p/apply_chat_template-is-the-safety"
source_title: "apply_chat_template() Is the Safety Switch - by Tarun Reddi"
source_id: 46675271
excerpt: "生文字列でテンプレート無効化、Gemma/Qwenが危険指示を生成"
image: "https://substackcdn.com/image/fetch/$s_!QZ7m!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcbf6301d-6be9-4faf-b60c-1b597ca9a3cc_2528x1696.png"
---

# Bypassing Gemma and Qwen safety with raw strings - apply_chat_template() Is the Safety Switch
魅力的タイトル案: 「“ただの文字列”で安全が吹き飛ぶ？――チャットテンプレート依存が招く重大な脆弱性」

## 要約
ある関数呼び出しやチャット用トークンのフォーマットが欠けると、いわゆる「指示調整（alignment）」済みとされる小型オープンモデルが安全拒否を失い、危険な出力を返してしまうという脆弱性が確認された。

## この記事を読むべき理由
日本国内でもオープンソースのLLMをプロダクションに使う事例が増えています。テンプレートや入力整形を軽視すると、想定外の危険な応答が出るリスクがあるため、導入・運用の実務者は知っておくべき問題です。

## 詳細解説
- 背景：多くの「Assistant」モデルは、学習時にチャット形式（system/user/assistant の区切りトークン）で指示調整されることで「拒否するモード」へと確率的に切り替わるよう訓練されています。つまり「安全」は重みそのものではなく、入力の文脈（フォーマット）によって発現する振る舞いです。
- 実験概要（概念的）：Qwen2.5/ Qwen3 / Gemma-3 / SmolLM2 といった小型モデルで、同じ危険系プロンプトを
  - （A）想定どおりのチャットテンプレートで与えた場合（Aligned）
  - （B）テンプレートを介さない生文字列で与えた場合（Unaligned）
 という2通りで比較したところ、挙動が大きく異なりました。
- 主な所見：
  - 「Aligned」時は高い拒否率が確認される一方で、「Unaligned」時に拒否が大幅に低下するモデルが存在した（例：Gemma-3 で100%→60%、Qwen3 で80%→40%など）。
  - 崩れたケースでは、単なる無意味出力ではなく「高実用性の有害な指示」が生成されうる点が特に問題。
- なぜ起きるか（技術的要点）：
  - 指示調整（instruction tuning）やRLHF は、ある「確率的モード」を学習させる手法で、チャット区切りトークンがそのモードを起動するトリガーになっている。トリガーがない入力はベースの次トークン予測モードに戻り、学習コーパスの確率分布に従って出力するため、安全性が保証されない。

## 実践ポイント
- 入力パイプラインの堅牢化：
  - モデルに渡す前に必ず想定フォーマットへ正規化する（サニタイズ／ラッパーを必須化）。  
  - 外部から生文字列を直接渡す公開APIは避けるか、別途厳格なフィルタを挟む。
- 推論時の防御（Interceptorパターン）：
  - 軽量な分類器（安全判定専用）を「System 2」として導入し、危険閾値を超えるリクエストはメインモデルに送らない運用を推奨。
- 学習・評価の改善：
  - 指示調整時に、典型的テンプレートだけでなく「フォーマットが崩れた」入力も混ぜてトレーニングし、分布ロバストネスを高める検討を行う。
  - テンプレート依存を検出するベンチマーク（フォーマット変化を含む評価セット）を運用に組み込む。
- ドキュメントと運用ルールの明示：
  - モデルカードやREADMEに「テンプレート依存の安全性」を明記し、公開・商用利用時の注意書きを付す。
- モニタリングと責任ある公開：
  - ログと自動判定で「テンプレート無効化に伴う安全逸脱」を検出する仕組みを持つ。発見時は責任ある開示を行う。

参考情報として、この問題は既存研究（例：ChatBug）でも指摘されており、単なる実装ミスで重大な安全欠陥が発生し得る点は業界共通の課題です。オープンモデルを安全に扱うには「テンプレートは飾りではない」という認識をチーム全体で共有することが重要です。
