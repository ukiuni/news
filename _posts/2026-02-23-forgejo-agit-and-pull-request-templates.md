---
layout: post
title: "Forgejo, AGit, and Pull Request Templates - Forgejo、AGit、プルリクエストテンプレート"
date: 2026-02-23T12:53:40.387Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://carlo.zancanaro.id.au/posts/forgejo-agit-and-pull-request-templates.html"
source_title: "Forgejo, AGit, and Pull Request Templates"
source_id: 1281595234
excerpt: "Emacs/MagitからForgejoのPRテンプレを対話的に読み込み編集して自動反映する実践的ワークフローを紹介"
---

# Forgejo, AGit, and Pull Request Templates - Forgejo、AGit、プルリクエストテンプレート
魅せるPRをEmacsから一発で。AgitフローでPRテンプレを無視せずに送るMagit拡張

## 要約
Forgejo（Codeberg等）向けのagitフローでEmacs/MagitからPRを作る際、既定のプルリクテンプレートを飛ばしてしまう問題を、テンプレートを読み込んでタイトル／本文を対話的に編集・Base64で渡すことで解決する手法を紹介します。

## この記事を読むべき理由
Emacs＋Magitで日常的にPR作成する開発者（特にOSSやGuixユーザー）は、テンプレートを無視すると礼儀やレビュープロセスに影響します。本稿はテンプレートを尊重しつつワークフローを止めない実用的な改善策を提示します。

## 詳細解説
問題点
- ForgejoのagitフローではPR作成時に最後のコミットメッセージだけが使われ、リポジトリの `.forgejo/pull_request_template.md` を反映できない。
- Magitの既存アクションだと、PRを開いて手動で説明を編集する手間が残る。

解決の要点
- magit-push の transient にカスタムサフィックス（例: magit-push-current-agit）を追加し、agit向けの refspec（/refs/for/{branch}）を用いる。
- 新規PR作成時（forceではないpush）にテンプレートファイルを読み込み、専用バッファでタイトルと本文を対話的に編集させる（recursive-edit を使用）。
- 編集結果のタイトル／本文を Base64 エンコードして、git push に -o title={base64} -o description={base64} として渡す。force push の場合は既存PRの更新なので何もしない。

実装の核（要旨）
```emacs-lisp
;; 新規PR時にテンプレートを読み、title/descriptionをbase64で渡す部分（要約）
(let ((info (cz/read-pull-request-from-buffer (concat (magit-gitdir) "../.forgejo/pull_request_template.md"))))
  `("-o" ,(concat "title={base64}" (base64-encode-string (car info) t))
    "-o" ,(concat "description={base64}" (base64-encode-string (cdr info) t))))
```

補助機能
- cz/read-pull-request-from-buffer: テンプレートを読み込み、新しいバッファで編集。C-c C-cで確定してタイトル（1行目）と本文（残り）を返す。
- 専用モード（cz/agit-pull-request-mode）でキーbind（C-c C-c／C-c C-k）を定義し、途中キャンセルや確定が可能。

注意点
- force push（--force/--force-with-lease）時は既存PRのコミット差し替えなのでテンプレート編集を行わない。
- テンプレートの構造に厳密に従う実装ではなく、シンプルに1行目をタイトル、それ以降を本文とする方式。

## 実践ポイント
- .forgejo/pull_request_template.md をリポジトリに置く（プロジェクトのテンプレート運用を統一）。
- 上記の補助関数を Emacs 設定に追加して magit-push のメニューに項目を挿入するだけで即利用可能。
- テストは非forceの新規pushで行い、Base64で送ったtitle/descriptionがForgejo上で正しく表示されるか確認する。
- 日本のOSS運営や社内リポジトリでもテンプレート遵守はレビュー円滑化に直結するので導入推奨。必要ならこの機能をパッケージ化して配布すると再利用性が高まる。
