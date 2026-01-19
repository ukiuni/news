---
layout: post
title: "Please, Stop Redirecting to Login on 401 Errors 🛑 - 401エラーで即ログインへリダイレクトするのはやめてください"
date: 2026-01-19T17:52:49.356Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://dev.to/aragossa/please-stop-redirecting-to-login-on-401-errors-3c0l"
source_title: "Please, Stop Redirecting to Login on 401 Errors 🛑 - DEV Community"
source_id: 3175142
excerpt: "401で即リダイレクトせず、トークン自動更新で入力消失を防ぐ実装法"
image: "https://media2.dev.to/dynamic/image/width=1000,height=500,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Frveyzsj5ftrgtn6fj9id.png"
---

# Please, Stop Redirecting to Login on 401 Errors 🛑 - 401エラーで即ログインへリダイレクトするのはやめてください
保存中の入力が消える前に知っておくべき「401で即リダイレクト」問題の直し方

## 要約
アクセストークンが切れてバックエンドが401を返したときに、ページ丸ごとログイン画面へ飛ばすのはUX上の重大な欠陥。静かにトークンを更新してリトライする「回復可能なエラー処理」が正解です。

## この記事を読むべき理由
日本の業務系アプリや設定フォームが多いサービスでは、ユーザーの未保存データ喪失が致命的な体験を生みます。セキュリティとUXを両立する実装パターンと、それを確かめるテスト手法（Playwrightによる「意図的な401発生」）を学べます。

## 詳細解説
なぜまずいのか
- 多くのフロント実装は401を受けると即 window.location.href = '/login' のように全体をリロードしてしまう。結果、入力中のフォームや編集中の状態が失われる。
- 開発者は「セッションが切れた＝安全のためリロード」が必要だと考えがちだが、実際は「ログイン状態を回復して失われた操作を再試行」できる場面がほとんど。

よくある（ダメな）実装例 — やらないでください:
```javascript
// javascript
axios.interceptors.response.use(null, error => {
  if (error.response && error.response.status === 401) {
    window.location.href = '/login'; // NG: ページ状態を破壊する
  }
  return Promise.reject(error);
});
```

正しい考え方（回復可能エラー）
- Intercept: 401を検知してただちにリダイレクトしない。
- Queue: 失敗したリクエストをキューに入れて待機させる。
- Refresh: バックグラウンドでリフレッシュトークンを使って新しいアクセストークンを取得する（またはパスワード再入力のモーダルを出す）。
- Retry: トークン取得後、キューにあるリクエストを新トークンで再送する。

注意点（実装上の落とし穴）
- 同時に多数のリクエストが401になるとリフレッシュが多重発生するので、単一のリフレッシュ処理を共有する仕組み（mutex / single-flight）を入れること。
- リフレッシュ失敗時のフォールバック（明示的なログアウト/UIでの警告）を必ず実装すること。

実際の改善イメージ（単一のリフレッシュを共有する例）:
```javascript
// javascript
let refreshing = null; // Promise or null
axios.interceptors.response.use(null, async error => {
  if (error.response?.status !== 401) return Promise.reject(error);

  if (!refreshing) {
    refreshing = refreshToken() // refreshToken は Promise を返す
      .finally(() => { refreshing = null; });
  }
  await refreshing;
  // 新しいトークンがあれば元のリクエストを再試行
  error.config.headers['Authorization'] = `Bearer ${getAccessToken()}`;
  return axios(error.config);
});
```

テストの難しさと対策
- アクセストークンの有効期間は本番で数十分〜1時間が一般的。QAで「トークンが切れるのを待つ」テストは現実的でない。
- 代替として、E2Eでリクエスト送信直前にAuthorizationヘッダを除去するか、ネットワークプロキシでヘッダを剥ぐことで即座に401を発生させ、回復ロジックを検証できる。

Playwrightを使った実証テスト例（要求のヘッダを削る）:
```python
# python
def test_chaos_silent_logout(page):
    # 1. ログインしてフォームへ
    page.goto("/login")
    # ...ログイン処理...
    page.goto("/settings/profile")
    page.fill("#bio", "大事な下書き")

    # 2. CHAOS: 保存リクエストから Authorization を削る
    def kill_token(route, request):
        headers = dict(request.headers)
        headers.pop("authorization", None)
        route.continue_(headers=headers)
    page.route("**/api/profile/save", kill_token)

    # 3. 保存をクリックして回復を確認
    page.click("#save-btn")
    assert page.url != "/login"  # 悪い実装ならログインに飛ぶ
    assert page.locator("#bio").input_value() == "大事な下書き"
```

## 実践ポイント
1. まずは401で全体リダイレクトしている箇所を洗い出す（axios/Fetchのグローバルハンドラなど）。
2. リフレッシュ処理を単一化（single-flight）して、失敗時はユーザーに明示的な再認証UIを表示する。
3. 重要なフォームはドラフトをローカルに保存（localStorage/IndexedDB）して保険をかける。
4. E2Eで確実に検証するため、Playwrightのルート操作やネットワークプロキシで「即401」を発生させるテストを組み込む。
5. モバイルや実機での検証はChaos Proxyのようなネットワークレイヤーでのヘッダ操作を利用する。

短くまとめると：401は「致命的クラッシュ」ではなく「回復可能なイベント」に設計を変えれば、ユーザーの作業を守れて品質が格段に上がります。
