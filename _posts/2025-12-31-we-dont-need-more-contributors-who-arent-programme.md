---
layout: post
title: "We don't need more contributors who aren't programmers to contribute code - プログラマでない寄稿者によるコード貢献は必要ない"
date: 2025-12-31T04:36:48.029Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159"
source_title: "We don't need more contributors who aren't programmers to contribute code"
source_id: 46440833
excerpt: "AI生成を自分で検証し提出するLLVMのhuman-in-the-loop方針、メンテ負担を防ぐ"
---

# We don't need more contributors who aren't programmers to contribute code - プログラマでない寄稿者によるコード貢献は必要ない
LLVMが示す「AI時代の寄稿ルール」：メンテナの時間を守る“human-in-the-loop”とは何か

## 要約
LLVMはAI支援で生成した成果物をそのまま投げることを禁じ、寄稿者自身が生成物を理解・レビューして答えられる状態で提出する「human-in-the-loop」方針を提案している。

## この記事を読むべき理由
AIコーディング支援が普及する今、日本のOSSコミュニティや企業でのコラボレーションにも同様の摩擦が出始めている。メンテナの時間を守りつつAIを生産性向上に活かす実務的なルール設計は、すぐに参考にできる知見だ。

## 詳細解説
- 方針の核心：寄稿者はLLMなどツールで生成したコードや文章を必ず自分で読み、正確さを担保した上で提出すること。提出時点で「誰が作者で、誰が責任を負うか」が明確であることを求める。
- 理由：未検証のAI出力をそのまま保守側に投げると、レビュー負担が受け手側に移り「抽出的（extractive）」な貢献になってしまう。レビューにかかるコストが貢献の価値を上回る場合、プロジェクト全体の持続性を損なう。
- 具体的要件例：
  - PRやコミットにツール使用の明示（例：commit メッセージに Assisted-by: を付ける等）。
  - 完全自動でリポジトリ上の操作を行うエージェントは禁止。人の承認が入らない自動コメントや自動PRは不可。
  - 新規寄稿者には小さく理解可能な変更から始めることを推奨し、成長を促す文化を維持。
- 運用面：メンテナが「抽出的だ」と判断した場合の定型返答やラベリング運用を用意し、不要なやり取りを減らす。同時に例外的に許可する自動化ツールの運用は別途RFCなどで審査する道を残す。
- 著作権の留意点：AIが生成した内容に既存著作物が含まれる可能性は寄稿者の責任。権利がない素材は送らないこと。

## 実践ポイント
- 寄稿者（日本の開発者向け）
  - AIで下書きを作るのは可。ただし必ず自分で読み、動作・設計意図を説明できるようにする。
  - PRは小さく、レビューしやすい単位に分ける。大規模な一発PRは避ける。
  - PR/コミットにツール使用の注記（例：Assisted-by: llm-name）を入れる。
  - 長い出力（“壁のようなテキスト”）は要点要約を付けてレビュー時間を節約する。
- メンテナ/プロジェクト運営者（日本のOSSリポジトリ向け）
  - 「human-in-the-loop」を明文化し、抽出的貢献への対応テンプレを用意する。
  - 自動エージェントは原則禁止、例外はRFCやパイロットで審査するプロセスを作る。
  - 新規寄稿者を歓迎しつつ、小さな成功体験を積ませるレビュー文化を保つ。
- 企業内運用
  - 社内でAI支援を使う場合もOSS寄稿時の明記ルールを作り、法務・著作権チェックを組み込む。

## 引用元
- タイトル: We don't need more contributors who aren't programmers to contribute code
- URL: https://discourse.llvm.org/t/rfc-llvm-ai-tool-policy-human-in-the-loop/89159
