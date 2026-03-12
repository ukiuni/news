---
layout: post
title: "Document poisoning in RAG systems: How attackers corrupt AI's sources - RAGシステムにおけるドキュメント汚染：攻撃者はAIの情報源をどう壊すか"
date: 2026-03-12T22:09:25.374Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://aminrj.com/posts/rag-document-poisoning/"
source_title: "Document Poisoning in RAG Systems: How Attackers Corrupt Your AI's Sources | Amine Raji, PhD"
source_id: 47350407
excerpt: "RAGの知識ベースに偽ドキュメントを仕込み、埋め込み異常検出で見抜く防御法を解説"
image: "https://aminrj.com/assets/media/ai-security/document-poisoning-in-rag-systems.png"
---

# Document poisoning in RAG systems: How attackers corrupt AI's sources - RAGシステムにおけるドキュメント汚染：攻撃者はAIの情報源をどう壊すか
RAGの「知識ベース」が一瞬でウソを語る──誰でも仕掛けられるドキュメント汚染の手口と現場で効く防御

## 要約
ローカルで動くRAG（Retrieval-Augmented Generation）システムに対し、攻撃者が数件の「偽ドキュメント」を追加するだけで、LLMが正しい情報を覆して誤った結論を返す現実的な攻撃（Document Poisoning）が実証された。埋め込みベースの異常検出が最も効果的な防御である。

## この記事を読むべき理由
日本の企業や開発チームも社内FAQ、財務資料、技術ドキュメントをRAGに取り込む流れが進む中、知識ベースの「書き込み権」を持つ人物・コネクタが攻撃経路になり得る。誤情報が永続的に流れるリスクは、法務・投資家情報・医療等の領域で致命的になり得るため必読。

## 詳細解説
- 攻撃の全体像  
  - 目的は「正しいドキュメントを検索順位から押し出し、LLMの出力を意図的に変える」こと。攻撃者はソフトウェア脆弱性を使わず、知識ベースに書き込むだけで成立する。  
- 2つの成功条件（PoisonedRAGの定義）  
  1. Retrieval Condition：偽ドキュメントがクエリに対して正規文書より高い類似度で引き出されること。  
  2. Generation Condition：取得された偽情報がLLMに攻撃者の結論を出させること（権威付けや表現で誘導）。  
- 実験の要点（元記事の再現ラボの要旨）  
  - ローカル構成：Qwen2.5系モデル＋all-MiniLM埋め込み＋ChromaDBのファイルベース。  
  - 攻撃は三つの相互補強する文書（「CFO訂正」「規制通知」「取締役会議事録」等）を追加する手法。語彙（"CORRECTED", "CFO", "Q4 2025" 等）を工夫して埋め込み類似度を稼ぎ、正規の数字を「過去の誤り」としてフレーミングする。  
  - 結果：小規模コレクションでも高成功率（例：20回中19回成功）が観察された。  
- なぜ危険なのか（運用上の特徴）  
  - 永続性：偽文書は削除されるまでずっと効く。  
  - 視認性の低さ：利用者は出力結果だけを見るため、根拠文書の汚染に気づきにくい。  
  - 低い参入障壁：編集権さえあれば専門的な攻撃技術がなくても可能。  
- 防御の比較（要約）  
  単独の対策は限定的だが、埋め込み異常検出（新規文書の既存文書との高類似度や追加候補同士のクラスタ密度を検出）が最も効果的。複数層を組み合わせることで残余リスクを下げる。

## 実践ポイント
- 書き込み経路を全列挙する：人の編集だけでなくConfluence/Slack/SharePoint自動同期やCIパイプラインも含める。  
- 取り込み時に埋め込み異常検出を行う：新規ドキュメントが既存文書と極端に似ているか、候補群が互いに過度に密集していないかをチェックしてフラグを立てる。しきい値はコレクション特性をベースに、平均＋2標準偏差（$\mu + 2\sigma$）などで決める。  
- スナップショットとロールバックを整備：ChromaDB等の永続化フォルダをバージョン管理して、問題発覚時に復元できるようにする。  
- 低温度（temperature）運用：高信頼が必要な業務では生成温度を可能な限り低く設定し非決定的な発言を抑える。  
- サンプル実装（簡易チェック例）  
```python
# python
# 新規候補を ingestion 前に簡易チェックする例
for new_doc in candidate_documents:
    sim_to_existing = max(cosine_sim(new_doc.emb, e.emb) for e in collection)
    if sim_to_existing > 0.85:
        flag("high_similarity", new_doc)
cluster_density = mean_pairwise_similarity(candidate_documents)
if cluster_density > 0.90:
    flag("tight_cluster", candidate_documents)
```
- 運用ルール：疑わしいフラグは自動で拒否ではなくレビューキューへ回す。誤検知を避けるため、コレクションごとに閾値をチューニングする。

短く言えば、RAGは「検索＋生成」の組み合わせが強みだが、検索対象（知識ベース）自体が攻撃対象になり得る。埋め込みを使った前処理と運用プロセスの整備で実用的な防御が可能です。
