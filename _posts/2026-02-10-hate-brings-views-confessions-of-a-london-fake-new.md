---
layout: post
title: "\"Hate brings views\": Confessions of a London fake news TikToker - 「憎悪は再生を生む」：ロンドンの偽情報TikTokerの告白"
date: 2026-02-10T17:41:15.851Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.londoncentric.media/p/london-tiktok-fake-news-creator-hate-immigrants"
source_title: "&quot;Hate brings views&quot;: Confessions of a London fake news TikToker"
source_id: 46962924
excerpt: "AI音声と家ツアーで反移民デマを拡散し広告収入を稼ぐTikTokerの手口とアルゴリズムの裏側"
image: "https://substackcdn.com/image/fetch/$s_!EHJR!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7dd2a1c7-a179-4daa-b9a2-8f12eb9a4900_1500x1000.png"
---

# "Hate brings views": Confessions of a London fake news TikToker - 「憎悪は再生を生む」：ロンドンの偽情報TikTokerの告白
魅力的タイトル: クリックを稼ぐために作られた“家ツアー”──AI音声とアルゴリズムが生む偽情報ビジネスの裏側

## 要約
ロンドンを舞台に、物件内を撮影してAI音声で反移民デマを流し「再生数」を稼いだTikTokアカウントの内部告白。動機は広告収入やクリエイター報酬を狙った“収益化”だった。

## この記事を読むべき理由
アルゴリズム報酬が憎悪やデマをマネタイズする構造は日本のSNS環境にも当てはまる。技術的仕組みを知れば、個人・企業・開発者それぞれが対策を取れる。

## 詳細解説
- 手法：不動産の内覧中にスマホで撮影、AI合成音声を乗せて「不法移民に無料で渡された」などと虚偽の説明を付ける。ブランドや政治団体名も無断で使用して拡散力を高めた。  
- アルゴリズムの作用：炎上や強い感情表現はエンゲージメントを高め、TikTokの推薦が暴発的に再生を押し上げる。プラットフォーム側の自動検知と人力の限界が悪用される。  
- 技術的検出ポイント：動画の音声がTTS（AI音声）かどうかはスペクトル特徴や合成音特有の周期性で判別可能。映像の背景（ゴミ箱・標識）からジオロケーション推定、フレームのメタデータや撮影日時の一致で同一撮影者を特定できる。  
- モラルと法的影響：被写体のプライバシー侵害や名誉毀損のリスク、事業者の実務対応（解雇・警察通報・協力）が発生。

## 実践ポイント
- 一般ユーザー：気になる動画は拡散前に逆画像検索／コメント確認。顔や住所が映る動画は通報する。  
- プロダクト担当者：TTS検出、急増するビューの異常検知、ブランドロゴの無断使用検出を独自に組み込む。  
- 開発者／データサイエンティスト：音声スペクトル解析、フレーム単位のメタ情報抽出、ネットワークグラフでアカウント群をクラスタリングして「収益化目的の悪意ある連鎖」を検出するルールを設計する。  
- 法務／運用：撮影許諾チェックの運用強化、テナント/利用者への告知・対応フローを整備する。

短く言えば：アルゴリズムは「感情」を報酬化する。技術で検出し、運用で抑止することが求められている。
