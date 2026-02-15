---
layout: post
title: "Radio host David Greene says Google's NotebookLM tool stole his voice - ラジオ司会者デビッド・グリーン氏、GoogleのNotebookLMが自分の声を盗んだと主張"
date: 2026-02-15T22:27:32.743Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.washingtonpost.com/technology/2026/02/15/david-greene-google-ai-podcast/"
source_title: "Radio host David Greene says Google's NotebookLM tool stole his voice"
source_id: 47025864
excerpt: "NPR名物司会者がGoogleのNotebookLMを提訴、無断で自身の声をクローンされたと主張"
image: "https://www.washingtonpost.com/wp-apps/imrs.php?src=https://arc-anglerfish-washpost-prod-washpost.s3.amazonaws.com/public/FFKDBHUSINMQFITQRK6CHNRZOY_size-normalized.JPG&amp;w=1440"
---

# Radio host David Greene says Google's NotebookLM tool stole his voice - ラジオ司会者デビッド・グリーン氏、GoogleのNotebookLMが自分の声を盗んだと主張
あなたの“声”が勝手にコピーされる時代——NPRの名物司会者がGoogleを提訴した理由

## 要約
NPRのデビッド・グリーン氏が、GoogleのAIツール「NotebookLM」が自分の話し声を許可なく再現したとして損害賠償を求めて提訴。音声クローンとデータ収集の倫理・法的問題が改めて注目を集めています。

## この記事を読むべき理由
音声合成は日本でもボイスコンテンツ、ナレーション、VTuberなどで急速に普及中。声の「権利」とAI開発の境界は、クリエイターと企業の双方に直結する実務的問題です。

## 詳細解説
- 事件の概要：Green氏は、NotebookLMが生成するポッドキャスト音声の一つが自分の声に極めて類似するとして、許諾・報酬なしに声を複製されたと主張し提訴。問題は「どの音声データが学習に使われたか」「同意があったか」に集約されます。  
- 技術面：現代の音声クローンはニューラルTTS（テキスト・トゥ・スピーチ）と音声埋め込みを組み合わせ、少量のサンプルから話者固有の抑揚や語尾の癖を再現します。大規模モデルはオンライン音源や公開アーカイブを学習データとすることが多く、出所不明のデータ混入が問題を複雑にします。  
- 法的・倫理的論点：米国ではパブリシティ権や著作権、契約法が交錯。企業側は「公的に入手可能な素材」を根拠にする一方、当事者は人格権や経済的利益の侵害を主張します。技術的防御（声の透かし、出所追跡）や透明なデータ収集ポリシーがカギです。  
- 実装上の課題：一度学習に組み込まれた特徴をモデルから完全に除去するのは難しく、データ削除要求（右から左への影響）や「学習済みモデルからの除去（model unlearning）」が研究課題になっています。

## 実践ポイント
- クリエイター（声優・司会者など）：契約書に声の二次利用、AIでの合成に関する明記（禁止・有償許諾の条項）を入れる。自分の声の無断利用を監視するサービスを検討。  
- 開発者・企業：学習データの出所を文書化し、同意・ライセンスを確実に取得する。音声出力に不可視の透かし（watermarking）や識別子を埋め込み、出力元を追跡可能にする。  
- 日本市場への示唆：声優文化が強い日本では、肖像権・パブリシティ権の実務対応が急務。事務所やプラットフォームは素材管理と利用規約を早急に整備すべきです。  

この記事は、声をめぐる権利とAIの技術的現実がぶつかる最前線を短く伝えるものです。声を扱う側も使われる側も、今すぐ利用ルールと技術的対策を見直してください。
