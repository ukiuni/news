---
layout: post
title: "Collaborative editing with AI is really, really hard - AIと共同編集は本当に難しい"
date: 2026-01-20T22:41:28.312Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.moment.dev/blog/collab-with-ai-is-hard"
source_title: "Collaborative editing with AI is really, really hard / Moment devlog"
source_id: 421802696
excerpt: "Markdown→ProseMirrorでAI編集を実装する際の落とし穴と回避法"
image: "https://docs.moment.dev/default_opengraph.png"
---

# Collaborative editing with AI is really, really hard - AIと共同編集は本当に難しい
AIを「もう一人の共同編集者」にするのは本当に可能か？Momentの失敗と工夫から学ぶリアルな実装ガイド

## 要約
Momentチームは「AIがリッチテキストエディタをライブで編集する」体験を目指し、Markdownを通してAIの変更をEditorStateに反映するアプローチで多数の実装課題に直面しました。設計の要点は「.mdでやり取り → ProseMirrorで差分をステップ化 → ユーザー側に“提案”として提示する」ことです。

## この記事を読むべき理由
日本でもNotionやGoogle Docsのような共同編集機能を持つサービスは増えています。AIをリアルタイム共同編集者として組み込む試みは製品差別化や生産性向上につながる一方、見た目以上に難易度が高く、実運用の落とし穴が多いので、実装方針と回避策を早めに知っておく価値があります。

## 詳細解説
- なぜMarkdownに落とすのか  
  LLMは文字列入出力に強く、学習データもMarkdownに豊富に含まれるため、まずドキュメントをMarkdownにシリアライズしてAIに編集させるのが実用的という判断。完全に忠実な変換は難しい（ロスが出る）が、現状では有力なトレードオフです。

- エディタ側はProseMirrorを使う理由  
  リッチテキストの状態をリアルタイムで扱うには、セマンティックなEditorStateとトランザクション（Step）を扱えるProseMirrorが最も現実的。React統合には状態の“裂け目”（state tearing）を避ける専用ラッパーが必要とされています。

- AIの編集は.mdファイルを直接編集させる  
  AI（claude/amp/copilot等）に.mdを編集させ、ファイル変更を検知してそのMarkdownをEditorStateに「復元（hydrate）」します。AIはテキスト処理が得意なので、.patchやJSON化したCRDT/OT操作を直接生成させるより堅実です。

- 差分検出→提案化の流れ  
  1) AIが編集した.mdをProseMirrorのEditorStateに変換  
  2) ユーザーのEditorStateと比較して、変化箇所を一連のStepに変換  
  3) Stepを「suggested change」へ変える（削除箇所を赤、挿入箇所を緑で表示するようなUI）  
  単純なブロック単位置換は実装が容易だが、連続するAI編集や同時入力に弱い。

- 同時編集とマージの難しさ  
  リアルタイムでユーザーとAIが同時編集すると競合が生じる。回避策は（a）AI作業中はAIに見せる状態を凍結してユーザーの変更をAIへ戻さない、（b）受信したAI変更を3ウェイマージかProseMirror向けのコラボライブラリ（例: prosemirror-collab-commit相当）の再ベース処理で適用する、など。ただし実装は複雑で「残りの仕上げ」は高度な工学課題になります。

- ファイルシステムと同期の落とし穴  
  ローカルファイルを介する場合、書き込み競合（TOCTOU）や監視の遅延が問題になる。Momentは端的に「組み込み端末でAI実行中は書き込みを一時停止」する運用的対処を採っていますが、根本解決はAIとアプリの協調プロトコル設計です。

- パフォーマンス面  
  EditorStateの差分計算はレンダースレッドをブロックし得るため、ワーカー分離やバッチ処理などの工夫が必要。Momentは簡素化のためレンダースレッド上で処理しているが、規模によっては別プロセスやスレッド移譲が現実的です。

## 実践ポイント
- ドキュメント保存はMarkdown中心に設計する（フロントマターやHTML相当タグで拡張）。  
- エディタ実装はProseMirrorを第一候補に。React統合は専用ラッパー（react-prosemirror等）を検討。  
- AIには.mdを直接編集させ、その出力をProseMirror EditorStateにhydrateして差分を生成するワークフローを採る。  
- 単純なブロック置換は早く試せるが、連続編集や同時編集に耐えるには3ウェイマージやコラボライブラリで再ベースを行う設計が必要。  
- ファイル同期はTOCTOU対策を入れるか、AIとの同期プロトコル（状態フラグ／ロック）を設計する。  
- 差分計算はユーザー体感に影響するため、必要ならワーカー化や処理のデグレード戦略を用意する。  
- UIは「提案を受け入れる／却下する」インタラクションを用意し、ユーザーが編集主体であることを明示する。

以上の考え方は、日本のプロダクトでもAIを共同編集機能として導入する際の実務的なチェックリストになります。実装はトレードオフの連続なので、まずは簡易プロトタイプで運用上の問題点を洗い出すことを勧めます。
