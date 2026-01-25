---
layout: post
title: "I got tired of manual priority weights in proxies so I used a Reverse Radix Tree instead - プロキシの優先度ウェイトに疲れたので逆ラディックス木を使った"
date: 2026-01-25T13:29:52.014Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://getlode.app/blog/2026-01-25-stop-playing-priority-tetris"
source_title: "Lode | Stop Playing Priority Tetris: A Better Way to Handle Domain Routing"
source_id: 417987592
excerpt: "逆ラディックス木でドメインルーティング自動化、手動優先度廃止と具体度で決定、リテラル密度採用"
image: "https://getlode.app/_astro/cover-stop-playing-priority-tetris.DSaLLghm.jpg"
---

# I got tired of manual priority weights in proxies so I used a Reverse Radix Tree instead - プロキシの優先度ウェイトに疲れたので逆ラディックス木を使った
もう「優先度テトリス」はやめよう — 逆ラディックス木でドメインルーティングを自動化する方法

## 要約
ドメインを右→左に分割して逆基数木（Reverse Radix Tree）で管理し、セグメントの「Literal Density」によるスコアリングで最も具体的なルールを自動選択する手法を紹介する。手動の優先度や魔法の数字が不要になり、予測可能で高速なルーティングが実現する。

## この記事を読むべき理由
手動でpriorityや順序を調整するプロキシ設定に疲れている人、マルチテナント／ローカル開発で大量のホストルールを扱う人、また日本企業のオンプレ／クラウド運用でドメインごとの動的ルーティングを効率化したいエンジニアに有益。

## 詳細解説
- 本質：ホスト名は見た目は左→右だが階層は右→左。api.staging.myapp.test は ["test","myapp","staging","api"] の順に解釈するのが自然。  
- 構造：各セグメントを逆順に格納する逆ラディックス木（トライに近い構造）を使うと、TLD から絞り込みが行われ、競合するルールは同じ親ノード内でのみ比較される。  
- スコアリング（Literal Density）：各セグメントの「リテラル文字数」で具体度を算出。例えば純ワイルドカードは 0、api-* のような接頭ワイルドカードは高め、完全一致は最も高い。木の各レベルで「完全一致→パターン（スコア順）」の順に評価するため決定は決定論的。  
- 実例：bar.test、*.bar.test、foo.*.test、bar.*.test、*.test のような混在ルールでも木構造なら重複なく自然にマッチする（特定サブドメイン／ネスト／キャッチオールのケースを分離）。  
- 動的アップストリーム：{tenant}.myapp.test のような名前付きパラメータをキャプチャして upstream URL を動的に生成（例: http://{tenant}.internal:8080）。  
- パフォーマンス／トレードオフ：完全一致は O(L)（L=セグメント数）。パターンはその親レベルのパターン数 P に依存して O(P) の走査が入るが、グローバルなリニア検索より効率的。深さ無視の正規表現（depth-blind regex）は放棄する必要があるが、実務上は DNS の挙動に近く妥当。

## 実践ポイント
- ホストを '.' で split して反転させる実装を最初に作る。  
- ノードは「完全一致マップ」「パターンリスト（literal densityでソート）」「終端フラグ／ハンドラ」を保持する。  
- パラメータ（{name}）はワイルドカードと同様に扱い、マッチ時に値をキャプチャして upstream に埋め込む。  
- 既存の nginx/Traefik ルールを移行する際は、まず主要パターンだけを木に移して挙動を比較する（段階的移行）。  
- パフォーマンス計測を行い、特定レベルにパターンが集中する場合はルールの分割や正規化を検討する。

日本のプロダクトでマルチテナントやローカル複数ドメインを扱う場面は多く、手動優先度管理の手間を減らせばデプロイの事故や運用コストを大きく下げられる。
