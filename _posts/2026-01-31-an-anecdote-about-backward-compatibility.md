---
layout: post
title: "An anecdote about backward compatibility - 後方互換性にまつわる逸話"
date: 2026-01-31T08:35:07.508Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://blog.plover.com/2026/01/26/#wrterm"
source_title: "The Universe of Discourse : An anecdote about backward compatibility"
source_id: 46768260
excerpt: "旧IBM端末の色設定がBLACK固定で罠、マニュアル不足が招く互換性と運用の教訓"
image: "https://pic.blog.plover.com/prog/wrterm/ribbon.png"
---

# An anecdote about backward compatibility - 後方互換性にまつわる逸話
カラフルにしたかったらまずマニュアルを読む。意外すぎる「互換性」の落とし穴。

## 要約
古いIBM端末向けデバッガをカラフルにしようとしたら、WRTERMマクロのCOLOR引数が既定でBLACKで、許されるもう一つの値はRED（「二色リボン」搭載端末のみ）だった──という実体験から、後方互換性とレガシー制約の教訓を描いた話。

## この記事を読むべき理由
レガシー環境や既存APIと向き合う日本の現場でも同じような「当たり前の破綻」が起きるため、実務で遭遇するトラブル回避や設計の注意点が学べる。

## 詳細解説
- 背景: 著者はIBM System/370上で動くデバッガを扱い、3270 CRT端末の色を使って視認性を上げようとした。  
- 技術的要点: デバッガはWRTERMというマクロで端末へ出力していた。マニュアルを読むとWRTERMはCOLORというオプション引数を取り、省略時のデフォルトがBLACK。ホワイトではなくBLACKが既定で、もう一つ許される値はREDだけ。REDが使えるのは端末に「二色リボン」がある場合のみ。  
- 文書・運用の問題: 当時は紙の分厚いマニュアルが社内に散在し、入手や共有のコストが高かった（同僚がマニュアルを独占するエピソードなど）。この物理的摩擦が情報伝達の障害になっていた。  
- 本質: ハードウェアや歴史的制約がAPI設計やデフォルト値に残る。見た目の「普通」や自分の常識に頼ると罠にはまる。

## 実践ポイント
- マニュアルをまず確認する。特にレガシーAPIは暗黙の制約が多い。  
- 既定値に注意する。デフォルトが期待と逆の場合がある（例: BLACK ≠ white）。  
- レガシー環境は実機で検証する（エミュレータと実機で差が出ることがある）。  
- ドキュメントを社内で共有・アーカイブし、単独保有を防ぐ。  
- 互換性を保つ設計では、明示的なパラメータと移行パスを用意する。
