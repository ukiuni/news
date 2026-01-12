---
layout: post
title: "Moving Scratch generation to Python on browser - Scratch生成をブラウザ上のPythonへ移す"
date: 2026-01-12T03:07:05.578Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://kushaldas.in/posts/introducing-ektupy.html"
source_title: "Kushal Das"
source_id: 46551352
excerpt: "ブラウザでScratch風の操作感のままPythonを実行でき、授業導入が簡単なEktuPy"
---

# Moving Scratch generation to Python on browser - Scratch生成をブラウザ上のPythonへ移す
ブロックの楽しさをそのままに、ブラウザでPythonを書いて動かせる新しい学習体験「EktuPy」

## 要約
EktuPyは、Scratchライクなビジュアル体験を保ちながらブラウザ上でPythonコードを書いて実行できる教育向けプラットフォームです。PyScript／Pyodideでユーザーのブラウザ内のみで動作し、RuffやtyをWebAssembly経由で組み込んだエディタ支援を提供します。

## この記事を読むべき理由
日本でも小学校でのプログラミング教育が進む中、ブロック→テキストへの自然な移行は重要なテーマです。EktuPyはセットアップ不要で端末（学校のタブレットや家庭のPC）だけで動き、教材作成や授業導入の敷居を下げる可能性があります。

## 詳細解説
- 実行基盤：PyScript／Pyodideを使い、PythonをWebAssemblyとしてブラウザ内で動作させるため、サーバー側で処理を走らせる必要がありません。これによりプライバシーやオフライン演習の利点がありますが、WASMの起動時間やメモリは考慮が必要です。
- エディタと支援機能：CodeMirrorベースのエディタに、Astral経由でRuff（フォーマッタ／リンタ）とty（型チェック）を組み込み、LSP風の補助をブラウザ内で実現しています。これもWebAssemblyを活用した工夫です。
- Scratch互換のUX：画面はコードエリアとCanvas／ステージを併置し、Scratchでできるアニメーションや入力処理を同様に表現可能。子ども向けには非同期処理の複雑さを隠すため、wait()やplay_sound_until_done()など同期的に見えるAPIを用意し、裏側でAST変換によりasync/awaitを付与する仕組みを採っています。
- 共有と保存：アカウントで作品を保存・公開でき、Exploreページから他人の作品を実行／リミックス可能。将来的にDjangoベースでコード公開予定とのことです。
- 開発背景：既存のScratch、CodeMirror、PyScriptコミュニティの上に成り立っており、TypeScript/JSの支援も受けています。

## 実践ポイント
- 教師・保護者向け：まずはブラウザで試してみて、子どもにURLを共有して簡単なプロジェクト（キャラクターを動かす／音を鳴らす）を遊ばせるとよい。インストール不要が授業導入の強み。
- 教材作り：短いチュートリアルを用意して、ブロック操作から「同じことをPythonでどう書くか」を対比させると移行がスムーズ。
- 開発者向け：PyScript/Pyodideの組み込みや、WebAssemblyでのLSP／リンタ統合に興味があるならリポジトリ公開後にソースを追ってみると学びが大きい。AST変換はPythonのastモジュールやLibCSTなどで実装可能。
- 注意点：ブラウザ実行は環境依存（起動時間・メモリ）なので、学校の端末スペックを確認してからクラス導入を計画すること。

EktuPyは「ブロック感覚はそのままに、テキストへ自然に移れる」ことを目指した試みです。公開されたら、実際に触って教材や授業で使えるか検証してみる価値があります。
