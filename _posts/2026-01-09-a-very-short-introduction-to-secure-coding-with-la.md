---
layout: post
title: "A very short introduction to secure coding - with lab examples on fixing IDOR, insecure file uploading, and SQL injections - セキュアコーディング超入門：IDOR・危険なファイルアップロード・SQLインジェクションの実践対策ラボ"
date: 2026-01-09T23:12:45.077Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://levelup.gitconnected.com/advent-of-cyber-4-writeup-a-very-short-introduction-to-secure-coding-a258135bf13a?sk=b28759fa4f070221cf296cd1b4a00106"
source_title: "Advent of Cyber 4 writeup: A very short introduction to secure coding | by Aleksey | Level Up Coding"
source_id: 466846039
excerpt: "IDOR・危険ファイル・SQLiを実践ラボで即修正法を学ぶ—現場対応手順付き"
image: "https://miro.medium.com/v2/resize:fit:1081/1*WmJTNkpSrsRyOv-94Cs6MQ.png"
---

# A very short introduction to secure coding - with lab examples on fixing IDOR, insecure file uploading, and SQL injections - セキュアコーディング超入門：IDOR・危険なファイルアップロード・SQLインジェクションの実践対策ラボ
今すぐ直せる！現場で役立つセキュアコーディングの超短期集中ガイド

## 要約
Webアプリで頻出する脆弱性（IDOR、危ないファイルアップロード、SQLインジェクション）をラボ形式で学び、攻撃の仕組みと防御コードの書き方を短く解説します。

## この記事を読むべき理由
これらの脆弱性は小さな実装ミスで発生し、個人情報漏洩や不正侵入に直結します。日本のサービスでもクラウド化や外部公開によりリスクは高まり、早めに修正できるスキルは現場での価値が高いからです。

## 詳細解説
- IDOR（Insecure Direct Object Reference）
  - 概要：ユーザーがアクセスするオブジェクトを直接識別子（例: /user/12345）で指定し、サーバ側でアクセス権チェックがないと他ユーザーのデータにアクセスできる。
  - 攻撃例：URLやAPIのパラメータを変更して別ユーザーのリソースを取得する。
  - 対策：
    - サーバ側で必ず「認可チェック（ownership/role）」を行う。
    - 可能なら内部IDを外部に直接晒さない（UUIDやランダムトークン、参照マッピング）。
    - ルールベースでなく属性ベースのアクセス制御を用いる（例：resource.ownerId === currentUser.id）。
  - 実装例（Node.js/Express、擬似コード）:
    ```javascript
    // Node.js
    app.get('/notes/:id', async (req, res) => {
      const note = await db.findNoteById(req.params.id);
      if (!note) return res.status(404).send();
      if (note.ownerId !== req.user.id) return res.status(403).send();
      res.json(note);
    });
    ```

- 危険なファイルアップロード
  - 問題点：拡張子だけで信頼すると、スクリプト実行ファイルやマルウェアがアップされる。webrootに置くと即実行される危険が高い。
  - 対策：
    - 拡張子＋MIMEタイプ＋ファイルヘッダで検証する。
    - アップロード先はwebroot外、またはオブジェクトストレージ（S3等）に保存し、直接実行不可にする。
    - ファイル名はランダム化し、ユーザー提供の名前は別フィールドで保持。
    - 必要ならウイルススキャンやサンドボックスを導入。
  - 実装ヒント：
    - レスポンスで Content-Disposition: attachment を付ける。
    - 実行可能ビットは付けない、公開は署名付きURLやプロキシ経由にする。

- SQLインジェクション
  - 概要：不適切な文字列連結でクエリを作ると、攻撃者がSQLを挿入してDBを操作できる。
  - 対策：
    - パラメータ化されたクエリ（Prepared Statements）を使う。
    - ORMを利用しても生SQLを直接組み立てない。
    - 最小権限のDBユーザーを使い、エラーメッセージで内部情報を漏らさない。
  - 実装例（Python psycopg2）:
    ```python
    # Python
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    ```

ラボ学習の価値：攻撃側の視点で検証すると、どのバリデーションが抜けているかが分かりやすい。元記事も攻撃＋防御で学ぶラボを紹介しています。

## 日本市場との関連
- 個人情報保護（APPI）やMy Numberの扱いに敏感な日本では、漏洩コストが高い。スタートアップ〜大手まで脆弱性対策は必須。
- オフショア開発やパッケージ利用が多い環境では、実装レベルでのセキュリティチェック（コードレビュー、SAST、DRIの明確化）が特に重要。
- 日本国内でもバグバウンティやセキュリティ需要が増えており、セキュアコーディングは差別化要素になる。

## 実践ポイント
- すぐやること（優先度高）
  - 全てのリソースアクセスでサーバ側の認可チェックを入れる（IDOR対策）。
  - DBアクセスは必ずパラメータ化／プリペアドステートメントにする。
  - ファイルアップロードはwebrootに直置きしない、拡張子だけで許可しない。
- 継続的に行うこと
  - CIにSAST/依存関係スキャンを組み込む。
  - OWASP Top 10 に基づくテストを定期実行（DAST）。
  - 開発者に簡易ラボ（OWASP Juice Shop、DVWAなど）で攻撃側の基礎を体験させる。
- チェックリスト（3分で確認）
  - すべての入力を信頼していないか？
  - DBクエリに直接ユーザ入力を連結していないか？
  - アップロードされたファイルはどこに置かれているか？実行可能か？

元記事は短いラボ解説を通じて「なぜ」ミスが起きるかと「どう直すか」を示しています。まずはこれらの基本を自分のコードベースでチェックリストとして回してみてください。
