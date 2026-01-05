---
  layout: post
  title: "How to integrate Next.js server components and server actions with FastAPI backend - Next.jsのサーバーコンポーネントとサーバーアクションをFastAPIバックエンドと統合する方法"
  date: 2026-01-05T09:11:15.256Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://nemanjamitic.com/blog/2026-01-03-nextjs-server-actions-fastapi-openapi"
  source_title: "Next.js server actions with FastAPI backend and OpenAPI client - Nemanja Mitic"
  source_id: 470675931
  excerpt: "Next.jsのサーバーコンポーネントをFastAPIとHttpOnlyクッキーで安全統合"
  image: "https://nemanjamitic.com/api/open-graph/blog/2026-01-03-nextjs-server-actions-fastapi-openapi.png"
---

# How to integrate Next.js server components and server actions with FastAPI backend - Next.jsのサーバーコンポーネントとサーバーアクションをFastAPIバックエンドと統合する方法

魅力的な日本語タイトル: Next.jsの最新サーバー側ワークフローをPythonで完結させる──FastAPI＋HttpOnlyクッキーで実現する安全なSSRとサーバーアクション統合

## 要約
Next.js 16のサーバーコンポーネント／サーバーアクションを維持しつつ、バックエンドをPythonのFastAPIに任せる手法を解説。認証をHttpOnlyクッキーに移行してサーバーサイドでユーザーを特定し、OpenAPIから生成したクライアントでNext.jsサーバー→FastAPIを安全に呼び出す流れを示す。

## この記事を読むべき理由
- 日本のプロダクトでPython（機械学習や既存ライブラリ）を生かしたい場合に、Next.jsの最新機能を犠牲にせず統合できる実践手法が得られる。
- ブラウザ側localStorageのトークン運用を止め、HttpOnlyクッキーでSSR時に認証情報を安全に扱う方法が学べる。
- OpenAPIクライアントを活用することで型付きかつ運用しやすいフロントエンド/バックエンド連携が可能になる。

## 詳細解説
1) 背景と課題  
Next.jsのサーバーコンポーネントはサーバーで実行されるため、認証情報をブラウザ側のlocalStorageに置くとSSR時にユーザー情報が取れない。そこで「トークンをHttpOnlyクッキーに入れてサーバーで読み取る」アプローチが適切。

2) FastAPI側での変更点（要点）
- ログイン時にJWTを発行してレスポンスのSet-CookieヘッダでHttpOnlyクッキーをセットする。cookieは httponly, secure, samesite を適切に設定する（プロダクションでは samesite="none" と domain 指定が必要な場合がある）。
- ログアウトは同じキーで期限切れ or delete_cookie を返す。
- Cookieを読み取り、JWTを復号してユーザーを返す依存関係（Dependency）を用意し、各エンドポイントで CurrentUser を注入して保護する。

例（要点を抜き出したPython）:
```python
# python
def set_auth_cookie(subject: str, expires_delta: timedelta, response: Response) -> Response:
    expires_in_seconds = int(expires_delta.total_seconds())
    access_token = create_access_token(subject, expires_delta)
    samesite = "lax"
    domain = None
    if is_prod:
        samesite = "none"
        parsed = urlparse(settings.SITE_URL)
        domain = parsed.hostname
        host_segments = domain.split(".")
        if len(host_segments) > 2:
            domain = ".".join(host_segments[1:])
    response.set_cookie(
        key=settings.AUTH_COOKIE,
        value=access_token,
        httponly=True,
        max_age=expires_in_seconds,
        expires=expires_in_seconds,
        samesite=samesite,
        secure=is_prod,
        domain=domain,
    )
    return response
```

Cookieからユーザーを取り出す依存関係の要点:
```python
# python
cookie_scheme = APIKeyCookie(name=settings.AUTH_COOKIE)
CookieDep = Annotated[str, Depends(cookie_scheme)]

def get_current_user(session: SessionDep, cookie: CookieDep) -> User:
    if not cookie:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(cookie, settings.JWT_SECRET_KEY, algorithms=[security.ALGORITHM])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    user = session.get(User, token_data.sub)
    # ...check user existence/active...
    return user
```

3) Next.js側の設計ポイント
- フローはブラウザ → Next.jsサーバー → FastAPI。HttpOnlyクッキーはブラウザからNext.jsサーバーに自動で送られるため、Next.jsのサーバーコンポーネントやサーバーアクションは、サーバー実行コンテキストでそのクッキーを読み取りFastAPIへ中継・照会できる。
- FastAPIのOpenAPI（自動生成）から型付きクライアントを生成すると、Next.js内で安全かつ補完の効く呼び出しができる。生成したクライアントはサーバーからのリクエストにCookieを含める設定が必須（fetchの credentials/options やヘッダの受け渡し）。
- データフェッチは可能な限りサーバーコンポーネントで行い、フォームやミューテーションはNext.jsのサーバーアクションで実装する。これによりUIはクライアントで軽く保ちつつ、一貫した型／状態管理を実現できる。

Next.jsのサーバーアクション例（概念例）:
```ts
// typescript
export async function loginAction(formData: FormData) {
  const res = await fetch(`${API_BASE}/login/access-token`, {
    method: "POST",
    body: formData,
    // ブラウザ→Next.jsにはCookieが自動で送られる。Next.js→FastAPIは同一サーバー間通信なのでクッキーを明示する場合も。
    credentials: "include",
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
}
```

4) クロスサイト／デプロイの注意
- フロントEND と API が異なるドメインの場合、cookie.domain や samesite を正しく設定しないとブラウザがCookieを拒絶する。サブドメイン構成（api.example.com と app.example.com）では domain=".example.com"、samesite="none"、secure=true が典型的。
- ローカル開発や特殊なリバースプロキシ（例: Traefik）を使う場合は独自のドメインルールやセットアップが必要になる。

## 実践ポイント
- まずFastAPIの既存認証で「レスポンス→JSON body」から「レスポンスヘッダ→Set-Cookie(HttpOnly)」へ移行することを優先する。これでSSRでユーザーが使える。
- OpenAPIから型付きクライアントを生成し、Next.jsサーバーコードで使う。クライアントはサーバー実行環境でCookieを正しく送受信するよう設定する（credentials: "include" など）。
- Next.jsではデータ取得はserver components、フォームや副作用はserver actionsで設計して責務を分離する。クライアントは最小限の状態管理に留める。
- 本番ドメインでのsamesite/domain/secure設定を検証すること。ブラウザのCookieポリシーが厳しいため、本番ドメインで必ず動作確認する。
- セキュリティ：JWTの期限やリフレッシュ設計、CSRF対策（必要ならDouble Submit CookieやSameSite設定の検討）も合わせて検討する。

参考になる流れ（短いチェックリスト）
- FastAPI: set_auth_cookie / delete_auth_cookie 実装
- FastAPI: get_current_user 依存関係でエンドポイント保護
- OpenAPI → 型付きクライアント生成 (@hey-api/openapi-ts 等)
- Next.js: server components での認証付きフェッチ、server actions でのミューテーション実装
- デプロイ環境でCookieのdomain/samesite/secureを調整して確認

以上を踏まえれば、Next.jsの最新サーバー機能とPython製FastAPIを組み合わせ、型安全かつSSRに強いフルスタック構成を実現できます。
