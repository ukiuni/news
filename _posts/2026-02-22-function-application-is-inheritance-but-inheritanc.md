---
layout: post
title: "Function application is inheritance, but inheritance is not function application - 関数適用は継承だが、継承は関数適用ではない"
date: 2026-02-22T11:25:28.039Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://overlaylanguage.readthedocs.io/"
source_title: "Overlay Language &#8212; Overlay Language  documentation"
source_id: 399494541
excerpt: "オーバーレイ言語で業務ロジックを設定へ移し、非同期移行とテストを劇的に簡素化する手法"
---

# Function application is inheritance, but inheritance is not function application - 関数適用は継承だが、継承は関数適用ではない
クリックしたくなるタイトル: 「ビジネスロジックを設定ファイルへ移す新常識——Overlay Languageでテストも非同期移行もラクにする」

## 要約
Overlay Languageは、pytest風のfixture文法を持つPython向けの依存性注入（DI）デコレータAPIと、.oyaml/.ojson/.otomlで書く宣言的な“Overlay”構成言語を組み合わせたフレームワークで、ビジネスロジックの分離・再利用・移植を強力に支援します。

## この記事を読むべき理由
- レガシーなI/Oとビジネスロジックが絡んだコードを分離したい人  
- 同期実装から asyncio への移行やプロバイダ差し替えで苦労しているチーム  
- テスト容易性（モック／差替え）を高めつつ、コードの可搬性を確保したい日本の開発者に有益

## 詳細解説
- 2つの柱  
  1) PythonデコレータAPI（@scope, @extern, @resource）  
     - pytestのfixtureライクに「関数が何を必要とするか」を宣言すると、フレームワークが自動で依存解決する。  
     - アプリ全体のシングルトン（app-scoped）とリクエストごとのリソースを自然に共存させられる。  
     - @patchで既存コードに手を入れずに横断的な振る舞いを差し込める。  
  2) Overlay言語（.oyaml/.ojson/.otoml）  
     - SQLやフォーマット文字列、URLパターンなど「動かない」ビジネス判断をコードから切り離して宣言的に記述。  
     - モジュールごとに同名で深くマージされ、接着コード不要で拡張できる（Expression Problem の解消を目指す設計）。  
     - 単なる設定ファイルに見えるが、静的型付けを持つOverlay-Calculusに基づく“言語”であり、λ計算より表現力が高い設計でビジネスロジック自体を記述可能。  
- 効果  
  - I/O側は薄いアダプタに集約され、モックや差替えが楽になる。  
  - 同期→非同期（function color問題）の移行時に、ビジネスロジックを変えずに実行基盤だけ切替え可能。  
  - テストではpytestライクな記法で依存解決できるため学習コストが低い。

簡単なイメージ（Pythonのデコレータ使用例）:
```python
# python
from overlay import scope, extern, resource

@scope
def app_scope():
    ...

@extern
def db_client():
    ...

@resource
def user_service(db_client):
    return UserService(db_client)
```

## 実践ポイント
- まずはデコレータAPIで既存モジュールを少しずつ注入対応にする（@scope/@extern/@resource）。  
- ビジネスルール（SQL、フォーマット、URL）をOverlayファイルへ移すことでテストが単純化する。  
- @patchを使ってクロスカッティングな変更を元コードに触れずに追加する。  
- 同期→非同期移行前にビジネスロジックをOverlay側に置けば、移行コストが大幅に下がる。  
- ドキュメントは公式のGetting Started（デコレータ／Overlay言語）から始める（PyPIからインストール可能）。

— 元記事: Function application is inheritance, but inheritance is not function application（Overlay Languageドキュメント）
