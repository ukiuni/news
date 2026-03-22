---
layout: post
title: "Brute-Forcing My Algorithmic Ignorance with an LLM in 7 Days - LLMで7日間、アルゴリズム無知を力押しで克服した話"
date: 2026-03-22T14:44:47.209Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "http://blog.dominikrudnik.pl/my-google-recruitment-journey-part-1"
source_title: "Qikcik Blog"
source_id: 47476776
excerpt: "LLMを“先生”に1週間でGoogle面接向けアルゴリズムのパターンを習得する実践プロトコル"
---

# Brute-Forcing My Algorithmic Ignorance with an LLM in 7 Days - LLMで7日間、アルゴリズム無知を力押しで克服した話
1週間で“AIを先生”にしてアルゴリズム面接を乗り切るための実録と再現可能な学習プロトコル

## 要約
著者はGoogle面接まで1週間という状況で、Gemini ProなどのLLMを教師役にして短期集中でLeetCodeパターンを学び、配列・ハッシュ・ツリー・グラフ・二分探索・バックトラッキング等の「パターン認識」を身につけた。

## この記事を読むべき理由
短期間でアルゴリズム面接の勝ち筋を作る実践的なプロトコルが示されており、LLMを学習補助に使う具体的手順は日本の転職・選考対策や若手エンジニアの学習計画にすぐ役立つため。

## 詳細解説
- 学習方針：数学的定義に時間を使わず「問題パターンを識別→攻め方を知る」ことに注力。LLMに「コードは出さないで概念と攻め方だけ教えて」と指示し、作者は自分で実装→LLMに添削させるという反復プロセスを採用。
- 時間管理：問題ごとに10–30分のタイムボックスを設定し、短時間で多くのパターンに触れることで「パターンの引き出し」を増やした。
- 学んだ主要パターン：
  - 配列／ループ／ハッシュ（Contains Duplicate, Valid Anagram, Product of Array Except Self）
  - Two pointers（Container With Most Water、双方向収束）
  - スタック／キュー／BFS・DFS（ツリー／グラフ遍歴、Number of Islands、Find if Path Exists）
  - リスト操作（Reverse Linked List、Merge Two Sorted Lists）
  - バックトラッキング（Combination Sum）
  - 二分探索（Find Minimum in Rotated Sorted Array）
  - 動的計画法は最初は難解と判断（Climbing Stairsは抵抗感あり）
- 学習運用の工夫：
  - 自分スタイルでコードを書く→LLMに最適化案を求め→自分の変数名・流儀で再実装（「腑に落ちる」学習）
  - LLMのコンテキスト劣化対策で、問題選定用と実装用でチャットを分ける
  - 面接ではコンパイラでの確認ができないことを想定し、ナレーションで誤りを補う戦略を想定
- 限界と気づき：短期で得られるのは「パターン認識」と設計的直感で、深い理論（DPの本質など）は別途時間を取る必要あり。LLMに頼り過ぎると自分の理解が薄くなるリスクもある。

## 実践ポイント
- LLMに与えるプロトコル例：
  - 目的：概念ヒントだけ、コードは最初出さない
  - 制約：10–15分で次の概念を提示、問題リストはEasy→Mediumの順
- 初日〜短期でやること（優先順位）：
  1. 配列＋ハッシュ（Two Sum等）で自信を作る
  2. BFS／DFS（ツリー・グラフ問題）を反復で体に入れる
  3. Two pointers・二分探索・マージ系の典型を練習
  4. 余力があればバックトラッキング、DPは基礎概念だけ押さえる
- 学習ルール：
  - 自分で必ず実装してからLLMに見せ、改善点を問う
  - 問題ごとにタイムボックスを設定（10–30分）
  - LLMの回答が長時間続く場合はチャットを分割してコンテキスト劣化を防ぐ
- 日本の読者へ：日常業務が忙しい場合は「パターン習得」を目標に短時間反復するのが現実的。企業面接だけでなく、社内設計・デバッグでも同じパターンが頻出するため即効性が高い。

以上。
