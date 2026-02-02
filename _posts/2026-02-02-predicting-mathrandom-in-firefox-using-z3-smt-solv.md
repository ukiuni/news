---
layout: post
title: "Predicting Math.random() in Firefox using Z3 SMT-solver - Firefox の Math.random() を Z3 SMT ソルバーで予測する"
date: 2026-02-02T22:31:49.938Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://yurichev.com/blog/xorshift/"
source_title: "Predicting Math.random() in Firefox using Z3 SMT-solver"
source_id: 412048115
excerpt: "FirefoxのMath.randomが数回の出力で復元・予測できるとZ3で実証、対策も解説"
---

# Predicting Math.random() in Firefox using Z3 SMT-solver - Firefox の Math.random() を Z3 SMT ソルバーで予測する
FirefoxのMath.random()が読み解かれる：Z3で乱数の“正体”を暴く実例

## 要約
Firefox が内部で使う擬似乱数生成器 Xorshift128+ を Z3（SMT ソルバー）でモデル化すると、わずか数個の Math.random() 出力から内部状態を復元し、その先の乱数列を正確に予測できることを示す実験。

## この記事を読むべき理由
ブラウザの乱数を起点にした攻撃やプライバシー侵害は現実的なリスク。日本のウェブサービス／ゲーム事業者やフロントエンド開発者が「Math.random() の危険性」と「現実的な対策」を理解しておくべきだから。

## 詳細解説
- アルゴリズム: Firefox は Xorshift128+（64ビット 2 ステート a,b）を用いる。基本ステップはビットシフトと XOR による状態更新を行い、出力は t+s（64ビット）を返す。JavaScript の Math.random() はその出力の下位 53 ビットを取り出し、$2^{-53}$ を掛けて [0,1) の倍精度浮動小数点に変換する。
- モデル化と逆解析: Z3Py で a,b を 64 ビットの BitVec として定義し、Xorshift の状態遷移をそのまま再現する。観測値（例えば最初の 3 個の Math.random()）は 53 ビットのマンティッサに対応する整数に変換できるので、それを制約としてソルバーに与えると内部状態が一意に復元される。マスクは $2^{53}-1$（下位 53 ビット）で表現する。
- 結果: 実験では最初の 3 個の出力で一意な初期状態が得られ、その後の 20 個の出力を完全に再現できた。別の実験では「ほぼゼロに近い連続出力」が生じる初期状態も Z3 で見つけられることを示している。
- 意味合い: Math.random() は設計上暗号用途向けではないが、ブラウザが採用した PRNG の内部仕様（出力形式）が分かると、公開された連続出力から容易に状態復元が可能になる。これはオンラインゲームの乱数、クライアント側くじ・判定、トークン生成などで悪用され得る。

## 実践ポイント
- 開発者向け: セキュリティや公平性が問題になる用途（抽選、セッションID、トークン生成 等）では絶対に Math.random() を使わず、crypto.getRandomValues などの CSPRNG を使うこと。
- 調査者向け: 再現は Z3 + Python（Z3Py）で可能。観測値を 53 ビット整数に変換し、BitVec で状態遷移を実装して制約を与えると状態が得られる。
- 運用/方針: ブラウザ実装の変更や仕様公開によるリスクを評価し、重要処理はサーバ側で安全な乱数を生成する。日本のオンラインサービス企画者は利用規約や監査プロセスで乱数ソースの安全性を確認すべし。
- 追加対策: ユーザ側でブラウザを最新化、開発者はライブラリやフレームワークの乱数扱いポリシーを明確化。

元記事は Z3 による具体的なスクリプトと実験データを公開しており、再現や深掘りはそれらを参照すると良い。
