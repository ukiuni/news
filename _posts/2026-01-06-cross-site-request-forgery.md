---
  layout: post
  title: "Cross-Site Request Forgery - クロスサイトリクエストフォージェリ（CSRF）"
  date: 2026-01-06T12:33:05.487Z
  categories: [tech, world-news]
  tags: [tech-news, japan]
  source_url: "https://medium.com/@aravindcsebe/understanding-csrf-protection-in-spring-boot-a-complete-guide-b23e2ecc32af"
  source_title: "Cross-Site Request Forgery"
  source_id: 469765150
  excerpt: "Spring BootでCSRF対策の実践設定と実例で管理画面乗っ取りを防ぐ方法を解説"
---

# Cross-Site Request Forgery - クロスサイトリクエストフォージェリ（CSRF）
Spring Bootで絶対に知っておきたいCSRF対策 — ワンクリックで管理画面が乗っ取られる前に

## 要約
CSRFは「ユーザーのブラウザの信頼」を悪用して意図しない操作を実行させる攻撃。Spring Securityはデフォルトで同期トークン方式によるCSRF対策を提供しており、フォーム・AJAX・テストでの扱い方を正しく理解すれば実運用での被害を防げる。

## この記事を読むべき理由
日本のSaaSやEC、社内管理ツールはセッション認証を使うことが多く、CSRFのリスクは現実的。公開サービスや既存Spring Bootアプリを安全に運用するための具体的な設定とベストプラクティスがすぐに使える形でまとまっている。

## 詳細解説
- 攻撃の本質  
  CSRFは被害者が既に認証済みの状態で、攻撃者が仕込んだ外部ページから「ユーザーのブラウザが自動的に送る」クッキーを利用して不正な状態変更（POST/PUT/DELETE等）を行わせる。攻撃者はユーザーのセッションを直接盗む必要はない。

- Spring Bootの防御方針（同期トークンパターン）  
  サーバーがセッションごとにランダムなトークンを発行し、フォームやAJAXにそのトークンを含めさせる。サーバーは状態変更リクエストに対してトークン検証を行い、トークンが無い／不正なら拒否する。Spring Securityはデフォルトで有効。

- Springでの実装ポイント
  - Spring MVCのフォームタグやThymeleafを使うとCSRFトークンは自動挿入される。
  - プレーンHTMLの場合はサーバーから渡されたトークンをhiddenで入れる必要がある。
  - AJAXではトークンをヘッダに含めるのが一般的（metaタグ経由で取得してヘッダにセット）。

- いつ無効化してよいか  
  ステートレスなREST APIでCookieセッションを使わず、Authorizationヘッダ（例：Bearer JWT）のみを使う場合はCSRFを無効化して問題ないことが多い。ただしその判断は慎重に。

- 追加の防御策  
  SameSite属性、HTTPS、CSP、失敗ログの監視、トークンリポジトリ（Cookieベースなど）の調整などを併用する。

コード例（主要箇所のみ）

```java
// java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
  @Bean
  public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
      .authorizeHttpRequests(auth -> auth
        .requestMatchers("/public/**").permitAll()
        .anyRequest().authenticated()
      )
      .formLogin(Customizer.withDefaults())
      .csrf(Customizer.withDefaults()); // デフォルトで有効
    return http.build();
  }
}
```

プレーンHTMLでの手動挿入例（Thymeleafでトークンを渡す想定）:

```html
<!-- html -->
<form action="/update-price" method="POST">
  <input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}" />
  <input type="text" name="productId" placeholder="Product ID" />
  <input type="number" name="newPrice" placeholder="New Price" />
  <button type="submit">Update Price</button>
</form>
```

AJAX（fetch）でヘッダに含める例:

```javascript
// javascript
const token = document.querySelector('meta[name="_csrf"]').content;
const header = document.querySelector('meta[name="_csrf_header"]').content;

fetch('/update-price', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    [header]: token
  },
  body: JSON.stringify({ productId: '12345', newPrice: 99.99 })
});
```

テスト（MockMvc）での検証例:

```java
// java
@Test
@WithMockUser
public void testUpdatePrice_WithValidCsrfToken_Success() throws Exception {
  mockMvc.perform(post("/update-price").with(csrf())
      .param("productId", "12345")
      .param("newPrice", "99.99"))
    .andExpect(status().isOk());
}
```

## 実践ポイント
- まずは“そのまま”放置せずにデフォルトのCSRF有効設定を確認する（Spring Bootは有効がデフォルト）。
- フロントはThymeleafやSpringフォームタグを使えば自動でトークンが入る。既存のプレーンHTMLや外部フロント（SPA）の場合は必ずトークンをメタタグ経由で渡し、AJAXヘッダにセットする。
- APIを公開する場合は認証方式を見直す（CookieベースならCSRF必須、トークンヘッダ中心ならステートレス設計を徹底）。
- SameSite=Strict/ Lax を検討し、HTTPS化・CSP・不審メール教育で多層防御を構築する。
- CI環境やユニットテストでCSRFの成功/失敗ケースを必ずカバーする（MockMvcのcsrf()ヘルパー等を活用）。

短くまとめると：Spring BootではCSRF対策が用意されているが、フロント実装やAPI設計次第で漏れが生じる。すぐ使える設定・実装チェックリストを社内で共有して、ワンクリックで起こる被害を未然に防ごう。
