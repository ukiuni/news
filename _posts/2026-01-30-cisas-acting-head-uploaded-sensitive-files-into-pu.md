---
layout: post
title: "CISA’s acting head uploaded sensitive files into public version of ChatGPT - CISA臨時長官が公開版ChatGPTに機密ファイルをアップロード"
date: 2026-01-30T04:07:51.770Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.politico.com/news/2026/01/27/cisa-madhu-gottumukkala-chatgpt-00749361"
source_title: "CISA’s acting head uploaded sensitive files into public version of ChatGPT"
source_id: 46786672
excerpt: "公開版ChatGPTへCISA臨時長官が機密契約書を投入、ガバナンス崩壊の危険性露呈"
---

# CISA’s acting head uploaded sensitive files into public version of ChatGPT - CISA臨時長官が公開版ChatGPTに機密ファイルをアップロード
破滅的とは言えないが見過ごせない誤り：米CISAトップが「公開AI」に機密文書を突っ込んだ理由と教訓

## 要約
米国のサイバー防衛機関CISAの臨時長官が、外部にデータを送る公開版ChatGPTへ「for official use only」指定の契約文書をアップロードし、内部のセンサーが警告、DHSレベルの被害評価につながった。

## この記事を読むべき理由
政府や重要インフラを扱う組織で働く日本のエンジニア／管理者にとって、AIツール利用の運用リスクとガバナンスの不備が具体的に示された実例だから。ポリシーと技術の両面で即応できる知見が得られる。

## 詳細解説
- 何が起きたか：臨時長官は公開版ChatGPTに機密扱い（非機密だが公開不可の「for official use only」）の契約関連ファイルを入力。OpenAIにデータが共有され得るため、情報が外部で再利用される可能性が生じた。  
- 既存の制御と例外：CISAではChatGPTのデフォルトアクセスは遮断されており、長官は一時的例外を得て使用していた。例外運用の管理と監査が不十分だった点が問題となる。  
- 検知と対応：内部のサイバーセンサーが複数回警告を発生させ、DHSは被害評価と内部監査を実施。法務・CIOレベルも調査に関与した。結論は公表されていない。  
- 技術的リスク：公開AIに投入したテキストはサービス提供者側で学習や応答に使われる可能性があり、機密ではない文書でも攻撃者の手がかり（契約情報、サプライチェーン情報など）を与えかねない。対策済みの自社／閉域AIはデータの外部流出を防げる設計が可能。

## 実践ポイント
- 組織ポリシーを明確化：どの級の情報をどのAIで扱えるか（公開版は禁止／承認制／オンプレ限定）を定める。  
- 技術的ガードレール：DLP、APIホワイトリスト、ネットワーク分離、ログ＆監査、モデル出力遮断を導入する。  
- 例外運用の厳格化：一時例外は最小限・記録必須・自動期限付きにし、使用ログを監査する。  
- 教育と演習：全職員に「AIに入力してはいけない情報」の具体例を示す訓練を行う。  
- 国内制度との照合：総務省／NISCのガイドラインや契約上の守秘義務に照らして、行政機関・インフラ事業者は同様の運用見直しを行う。  

短く言えば、「誰でも使えるAI」に機微な公的情報を投入する行為は想定以上に危険。技術的制御と組織ルールを同時に整備することが最重要です。
