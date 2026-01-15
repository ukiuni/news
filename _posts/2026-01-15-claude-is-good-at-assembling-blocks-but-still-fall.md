---
layout: post
title: "Claude is good at assembling blocks, but still falls apart at creating them - Claudeは“レゴの組み立て”は得意、だが“ブロック作り”は苦手"
date: 2026-01-15T19:17:15.170Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.approachwithalacrity.com/claude-ne/"
source_title: "Claude is not a senior engineer (yet)"
source_id: 46618042
excerpt: "Claudeは繰り返し作業を高速化する一方、設計抽象化は不得手で危険"
image: "https://www.approachwithalacrity.com/content/images/size/w1200/2026/01/Screenshot-2026-01-11-at-10.26.29---PM.png"
---

# Claude is good at assembling blocks, but still falls apart at creating them - Claudeは“レゴの組み立て”は得意、だが“ブロック作り”は苦手
レゴは得意でも設計図なしに庭を整えることはできない — Claude（Opus 4.5）の強みと限界を実例で読み解く

## 要約
OpenAI系の大規模言語モデル（この記事ではClaude/Opus 4.5）は、既存の良い抽象（Sentry、Terraform、Playwrightなど）を与えると自律的に作業を終わらせられるが、新しい設計や洗練された抽象を「自分で作る」ことは不得手、という話。

## この記事を読むべき理由
- 日本の現場でもよくある「面倒な繰り返し作業」をAIで短時間に片付けられる可能性を具体例で理解できる。  
- 一方で、AIに任せると設計が劣化するリスク（特にレガシーなフロントエンドやアーキテクチャ周り）も明確に示されており、安全な運用方針が学べる。

## 詳細解説
- 成功例1：Sentryのデバッグループ  
  著者はSentry導入で動作確認がうまくいかず、ログが不十分で手作業の推測と試行錯誤が必要だった。ClaudeにPlaywrightでの自動テストスクリプトとSentryのドキュメントを与え、失敗→修正→再実行のループを任せたところ、約90分で原因を特定し解決した。原因はFastAPIのStreamingResponseでは自動トランザクションが作られない点で、明示的にトランザクションを作る修正で解決した。
- 成功例2：ModalからAWS ECSへの移行  
  著者はKubernetes/ECS未経験だったが、Terraformとaws CLIの操作権限を与えると、ClaudeはDockerfile作成、イメージをECRへプッシュ、必要なIAM/権限設定、ECS用のTerraform設定を短時間で生成し、一晩で稼働させた。ここでは「TerraformやCLIという良い抽象（＝レゴブロック）」があったため、Claudeは上手く組み立てられた。
- 失敗例：Reactのリファクタ提案  
  複雑で手入れされていないReactコードベースでは、Claudeが「線形スキャンでIDを探す」ような非効率な実装を提案した。正しい設計は上流からidを渡して高速に参照することだが、Claudeはコードのコンテキスト（設計意図や上流の可変性）を読み切れず、局所最適なhackを推奨してしまった。  
  ここから導かれる本質：LLMは「良いブロック」を組み合わせるのは得意だが、抽象化レイヤーを新しく設計してコードベース全体を整える（＝庭を手入れする）能力は限定的。

- 人間エンジニアの価値  
  著者は「上手いエンジニアは庭師のようにコードを剪定する」と表現する。長期的な維持性や抽象設計を考え抜くことは、人間の経験と意図（＝“魂”）が必要で、現状のLLMだけでは代替できない。

## 実践ポイント
- まずは“良いブロック”を用意する  
  Terraform、CIスクリプト、明確なAPI仕様、テストスイートなど抽象が整理されていると、LLMは短時間で有用な成果を出しやすい。
- デバッグループを自動化してLLMに回す  
  PlaywrightやE2Eの自動化＋観測ツール（Sentry等）を組めば、AIに「試行→観測→修正」のループを任せて労力を節約できる。
- アーキテクチャ変更は慎重に  
  LLMが出した実装提案は「局所解」になりがち。設計方針や上流データの流れを明示し、レビュー・テスト・負荷検証を必須にする。
- 最小実行単位で試す  
  フルリファクタは避け、まずはコンパートメント化した小さな変更をLLMに任せて結果を検証する。
- セキュリティと権限管理を厳格に  
  aws CLIやレジストリ操作をAIに許すときは、権限範囲を最小化し、ログとロールバック手順を整備する。
- 日本の現場での応用例  
  - レガシーな社内サービスのクラウド移行（Terraform＋ECS/EKSのテンプレ化）  
  - 繰り返し発生する導入作業（監視・ログ設定・デプロイ設定）の自動化  
  - フロントエンドの単純なバグ修正やフォームの自動テスト作成（設計変更は人が判断）

結論：ClaudeのようなLLMは「時間のかかる雑作業」を大幅に削れるが、「設計」と「抽象化」を生み出す人間の価値を脅かすことはない。むしろ、良い抽象を整える重要性が高まり、エンジニアの役割はより重要かつ創造的になる。

---  
元記事：Claude is good at assembling blocks, but still falls apart at creating them (Approach with Alacrity)
