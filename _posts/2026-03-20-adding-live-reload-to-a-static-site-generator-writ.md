---
layout: post
title: "Adding Live Reload to a Static Site Generator Written in Go - Go製静的サイトジェネレータにライブリロードを追加する"
date: 2026-03-20T19:24:36.217Z
categories: [tech, world-news]
tags: [tech-news, japan]
source_url: "https://jon.chrt.dev/2026/03/20/adding-live-reload-to-a-static-site-generator-written-in-go.html"
source_title: "Adding Live Reload to a Static Site Generator Written in Go"
source_id: 1107491035
excerpt: "編集→自動再ビルド→ブラウザ即再読み込みをGo製静的サイトに簡単追加"
---

# Adding Live Reload to a Static Site Generator Written in Go - Go製静的サイトジェネレータにライブリロードを追加する
Goで作ったシンプルな静的サイトジェネレータに、編集→自動再ビルド→ブラウザリロードを自動化する「ライブリロード」を手早く組み込む方法

## 要約
ローカル開発でファイル変更を検知してビルドをデバウンスし、SSEでブラウザへ通知、HTMLに開発用スクリプトを注入することで即時リロードを実現する手順を解説します。

## この記事を読むべき理由
ローカルでの高速フィードバックは生産性に直結します。特に日本の個人ブロガーや技術ドキュメントの運用（GitHub Pagesや自前ホスティング）では、軽量なdevサーバにライブリロードを足すだけで編集体験が劇的に改善します。

## 詳細解説
- ファイル監視（fsnotify）
  - Goのfsnotifyでディレクトリを再帰的に追加してイベントを受け取る。新規ディレクトリは作成時にwatcherへ追加する必要あり。
  - 監視対象イベントは Create / Remove / Rename / Write のような実際に意味があるものだけを対象にする。

```go
// Go
watcher, _ := fsnotify.NewWatcher()
filepath.WalkDir(root, func(path string, d os.DirEntry, err error) error {
  if d.IsDir() { watcher.Add(path) }
  return nil
})
for {
  select {
  case event := <-watcher.Events:
    if event.Has(fsnotify.Write) { /* handle */ }
  case err := <-watcher.Errors:
    _ = err
  }
}
```

- デバウンス（なぜ必要か）
  - 多くのエディタは一連のファイル操作（tmp作成→リネーム→削除）を行うため、保存で複数イベントが発生する。短い遅延（例：200ms）でイベントをまとめてからビルドするのが実務的。

```go
// Go
timer := time.NewTimer(time.Hour); timer.Stop()
case event := <-watcher.Events:
  if isRelevant(event) { timer.Reset(200 * time.Millisecond) }
case <-timer.C:
  builder.Build()
  broker.Broadcast("reload")
```

- 通知方法：SSE（Server-Sent Events）
  - WebSocketより軽量でサーバ→クライアント一方通行の用途に最適。ローカルのdevサーバにはSSEが簡潔で実装も容易。
  - ブローカーを用意して複数タブからの接続を管理（Subscribe/Unsubscribe/Broadcast）。

```go
// Go
type SSEBroker struct {
  mu sync.Mutex
  clients map[chan string]struct{}
}
func (b *SSEBroker) ServeHTTP(w http.ResponseWriter, r *http.Request) {
  flusher, ok := w.(http.Flusher); if !ok { http.Error(w,"",500); return }
  w.Header().Set("Content-Type","text/event-stream")
  ch := b.Subscribe(); defer b.Unsubscribe(ch)
  for {
    select {
    case msg := <-ch:
      fmt.Fprintf(w, "data: %s\n\n", msg); flusher.Flush()
    case <-r.Context().Done():
      return
    }
  }
}
```

- HTML注入ミドルウェア
  - 本番に影響を与えないために、開発サーバ経由で配信するときだけHTMLに短いスクリプトを挿入する。レスポンスを一旦バッファして、Content-Typeがtext/htmlなら</body>直前に注入する方法が簡単。

```go
// Go
script := `<script>new EventSource("/events").onmessage = () => location.reload();</script>`
body = strings.Replace(body, "</body>", script+"</body>", 1)
```

## 実践ポイント
- 実装の優先順：fsnotifyで監視 → デバウンス（150–300msの範囲で調整）→ SSEブローカー → HTML注入ミドルウェア。
- SSEはHTTP/1.1で十分。プロキシ/CDN越しの場合はCache-ControlやCORSを適切に設定する。
- 複数タブ対応は簡単だが、チャンネルのバッファ（例：10）を設けて遅いクライアントによるボトルネックを回避する。
- VSCode等を使っているなら、ローカルでの開発ワークフローが劇的に向上するのでまずは最小構成で導入してみる（distフォルダの自動反映など）。

短くまとめると、fsnotify＋デバウンス＋SSE＋HTML注入の組合せで、軽量なGo製静的サイトジェネレータに安全にライブリロードを追加できます。
