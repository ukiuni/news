---
layout: post
title: "Rethinking Java Web UIs with Jakarta Faces and Quarkus - Jakarta Faces と Quarkus で再考する Java Web UI"
date: 2026-02-15T16:13:03.560Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://www.simplex-software.fr/posts-archive/quarkuspf/"
source_title: "Rethinking Java Web UIs with Jakarta Faces and Quarkus  - Simplex Software"
source_id: 441233746
excerpt: "Quarkus×Jakarta FacesでJS削減＆高速化するJavaだけUI"
---

# Rethinking Java Web UIs with Jakarta Faces and Quarkus - Jakarta Faces と Quarkus で再考する Java Web UI

もうフロントに大量のJavaScriptは要らない？Quarkus×Jakarta Facesで「Javaだけ」のエンタープライズUIを取り戻す

## 要約
QuarkusがJakarta Faces（旧JSF）をサポートすることで、サーバーサイド描画による安定したUI構築がモダンなマイクロサービス環境でも現実的になった、という話です。

## この記事を読むべき理由
多くの企業がReact/Vue/Angularを標準にしていますが、サーバーサイドレンダリングの利点（初期表示速度、総JS量削減、セキュリティや運用の単純化）は未だ有効です。日本の金融／公共系や保守性重視の開発現場では特に刺さる選択肢です。

## 詳細解説
- 歴史背景：Jakarta Faces（旧JSF）は2000年代から続くJavaの標準UIフレームワークで、多数の実装（PrimeFaces 等）と豊富なコンポーネント群を持ちます。かつてはアプリサーバー上で動くのが前提でした。  
- 移行理由：Oracle時代〜MicroProfileの台頭、マイクロサービス化に伴い軽量ランタイム（Spring Boot、Quarkus、Micronaut 等）やフロント分離（SPA）が広まり、JSF系は影を潜めました。  
- 描画の議論：クライアントサイドレンダリング（CSR）は複雑化すると大量のJSを必要とし、TBTや初期応答に悪影響を与える一方、サーバーサイドレンダリング（SSR）はHTMLを返すため初動が速く、送るJSを減らせます。ビジネス系アプリではSSRの利点が大きい場合が多いです。  
- Quarkusの役割：Quarkusは高速な開発モード、クラウドネイティブな性能、ネイティブコンパイルなどを提供し、Jakarta Faces（PrimeFaces拡張含む）を軽量ランタイム上で実行可能にします。つまり「昔のJSFの良さ」をマイクロサービス時代に持ち込めます。  
- アーキテクチャ上の利点：単一言語（Java）でフロントとバックを扱えるため、チーム編成の負荷が下がり、保守性やセキュリティ管理も容易になります。

## 実践ポイント
- まずQuarkusプロジェクトを作成し、Jakarta Faces（Mojarra）とPrimeFaces拡張を追加して動かしてみる。  
- PrimeFacesのQuarkus向けショーケースをローカルでビルドしてコンポーネント群を確認する。  
- 実アプリで比較測定を行う：TTFB、LCP、TBT、初期バンド幅、ビルド/デプロイ速度をCSR版と比較する。  
- チーム運用面では「フロント専任」を減らしてJavaフルスタックへシフトすることで採用・保守コストを下げられるか検討する。  
- レガシー移行なら、既存のJSベースSPAと並行稼働させつつ、部分的にJakarta Facesへ戻すハイブリッド戦略も有効。

短期間で試作して指標を取れば、業務要件に応じてCSR／SSRのどちらが適切か合理的に判断できます。
